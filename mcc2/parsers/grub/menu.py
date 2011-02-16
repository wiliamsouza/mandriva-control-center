# -*- coding: utf-8 -*-
# Copyright (c) 2007 Jimmy Rönnholm
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import shutil
import re
from subprocess import Popen, PIPE

import utils

class GrubLegacy:

    """Represent the Grub configuration."""

    def __init__(self):
        self.menu = '/tmp/augeas-sandbox/etc/grub.conf'
        self.fstab = '/etc/fstab'
        self.mounted_splashdir = '/boot/grub/splashimages/'
        if self.__has_separate_boot_partition():
            self.splashdir = '/grub/splashimages/'
        else:
            self.splashdir = '/boot/grub/splashimages/'
        self.update_grub_command = '/usr/sbin/update-grub'
        self.grub_install_command = '/usr/sbin/grub-install'
        self.titles = []
        self.title_blocks = {}
        self.default_boot = 0
        self.separator = -1
        self.use_timeout = False
        self.timeout = 0
        self.vga = 769
        self.show_text = False
        self.show_menu = True
        self.use_colors = False
        self.normal_background = "black"
        self.highlighted_background = "black"
        self.normal_foreground = "black"
        self.highlighted_foreground = "black"
        self.normal_blink = False
        self.highlighted_blink = False
        self.groot = ""
        self.use_image = False
        self.grub_images = []
        self.default_image = ""
        self.show_splash = True
        self.password_protect = False
        self.protect_rescuemode = False
        self.protect_oldmode = False
        self.kernel_limit = "all"
        self.memtest = True
        self.update_default = True
        self.update_grub = False
        self.create_alternative = True
        self.has_advanced_options = True
        self.user_edited_file = False
        if os.system('convert -version') == 0:
            self.convert_exist = True
            self.image_formats = ["png", "jpeg", "gif", "tif", "bmp", 
                                  "svg" ,"xcf", "xpm", "xpm.gz"]
        else:
            self.convert_exist = False
            self.image_formats = ["xpm", "xpm.gz"]
            

        if not os.path.isfile(self.grub_install_command):
            self.grub_install_command = '/sbin/grub-install'

        if not os.path.isfile(self.update_grub_command):
            self.update_grub_command = '/sbin/update-grub'

        if not os.path.isfile(self.update_grub_command):
            self.has_advanced_options = False

        #self.menu = self.__find_config_file()

        if self.has_advanced_options:
            communication = Popen([self.update_grub_command], 
                                  stdin=PIPE, close_fds=True)
            communication.communicate("y\n")

        #We do this again, in case update-grub has created a new file.
        #self.menu = self.__find_config_file()

        if not self.menu:
            raise SystemExit('Fatal error. Can not find '
                             'the bootloader configuration file')

        self.__try_backup_config_file()

        if not os.path.isdir(self.mounted_splashdir):
            os.mkdir(self.mounted_splashdir)

        self.__fix_menu_lst_bug()
        self.__read_config()
        self.__check_themes()

    def __find_config_file(self):
        """Search for the Grub config file.
        If it cannot be found, return False
        """
        menu = '/boot/grub/menu.lst'

        if not os.path.isfile(menu):
            menu = '/boot/grub/grub.conf'

        if not os.path.isfile(menu):
            menu = '/etc/grub.conf'

        if not os.path.isfile(menu):
            return False

        return menu

    def __try_backup_config_file(self):
        """Make a backup of the Grub config file, if it does not exist"""
        if not os.path.isfile(self.menu + ".backup"):
            shutil.copy(self.menu, self.menu + ".backup")

    def __strip_line(self, line, start_slice, end_slice, remove_sharp):
        """Return slice of line with leading and trailing spaces removed,
        remove leading # if remove_sharp is True
        """
        line = line.strip()
        if remove_sharp and len(line) > 0 and line[0] == "#":
            line = line[1:]
            line = line.strip()
        elif len(line) > 0 and line[0] == "#":
            line = line[1:]
            line = line.strip()
            line = "#" + line
        line = line[start_slice:end_slice]
        line = line.strip()
        return line

    def __evaluate(self, line):
        """Extract info from line to class variables."""
        number_filter = re.compile('[0-9]+')
        if self.__strip_line(line, None, 7, True) == "default":
            if self.__strip_line(line, 7, None, True).find("saved") != -1:
                self.default_boot = -1
            else:
                match = number_filter.search(self.__strip_line(
                                             line, 7, None, True))
                if match:
                    self.default_boot = int(match.group())

        if self.__strip_line(line, None, 5, False) == "title":
            self.titles.append(self.__strip_line(line, 5, None, False))

        if self.__strip_line(line, None, 7, True) == "timeout":
            match = number_filter.search(self.__strip_line(
                                         line, 7, None, True))
            if match:
                self.timeout = int(match.group())
            if self.__strip_line(line, None, 7, False) == "timeout":
                self.use_timeout = True

        if self.__strip_line(line, None, 10, False) == "hiddenmenu":
            self.show_menu = False

        if self.__strip_line(line, None, 10, True) == "defoptions":
            if line.find("quiet") == -1:
                self.show_text = True

            if line.find("splash") == -1:
                self.show_splash = False

            if line.find("vga=") != -1:
                place = line.find("vga=") + 4
                if line[place:place + 2] == "0x":
                    self.vga = int(line[place:place + 5],16)
                else:
                    self.vga = int(line[place:place + 3])

        if self.__strip_line(line, None, 5, True) == "color":
            hidden = line.strip()[:1]
            if hidden != "#":
                self.use_colors = True
            color_line = line.replace("#","").replace("color","")\
                             .replace("=","").strip()
            first_slash = color_line.find("/")
            last_slash = color_line.rfind("/")
            if first_slash == last_slash:
                if color_line.find("blink-") != -1:
                    self.normal_blink = True
                    blinkplace = color_line.find("blink-")
                    color_line = color_line[:blinkplace] + \
                                 color_line[blinkplace + 6:]
                first_slash = color_line.find("/")
                last_slash = color_line.rfind("/")
                self.normal_foreground = color_line[:first_slash]
                self.normal_background = color_line[first_slash + 1:]
                self.highlighted_foreground = "white"
                self.highlighted_background = "blue"
            else:
                first_blinkplace = color_line.find("blink-")
                last_blinkplace = color_line.rfind("blink-")
                space = color_line.find(" ")
                if first_blinkplace != -1:
                    if first_blinkplace != last_blinkplace:
                        self.normal_blink = True
                        self.highlighted_blink = True
                        color_line = color_line[:first_blinkplace] + \
                                     color_line[first_blinkplace + 
                                                6:last_blinkplace] + \
                                     color_line[last_blinkplace + 6:]
                    else:
                        if first_blinkplace > space:
                            self.highlighted_blink = True
                        else:
                            self.normal_blink = True
                        color_line = color_line[:first_blinkplace] + \
                                     color_line[first_blinkplace + 6:]
                space = color_line.find(" ")
                first_slash = color_line.find("/")
                last_slash = color_line.rfind("/")
                self.normal_foreground = color_line[:first_slash]
                self.normal_background = color_line[first_slash + 1:space]
                self.highlighted_foreground = color_line[space + 1:last_slash]
                self.highlighted_background = color_line[last_slash + 1:]

        if self.__strip_line(line, None, 5, True) == "groot":
            self.groot = line[line.find("hd") - 1:line.find(")") + 1]

        if self.__strip_line(line, None, 11, False) == "splashimage":
            self.use_image = True

        if self.__strip_line(line, None, 8, False) == "password":
            self.password_protect = True

        if self.__strip_line(line, None, 15, True) == "lockalternative":
            if line.find("true") != -1:
                self.protect_rescuemode = True

        if self.__strip_line(line, None, 7, True) == "lockold":
            if line.find("true") != -1:
                self.protect_oldmode = True

        if self.__strip_line(line, None, 7, True) == "howmany":
            if line.find("all") != -1:
                self.kernel_limit = "all"
            else:
                match = number_filter.search(self.__strip_line(line, 7, 
                                                               None, True))
                if match:
                    self.kernel_limit = int(match.group())

        if self.__strip_line(line, None, 9, True) == "memtest86":
            if line.find("true") == -1:
                self.memtest = False

        if self.__strip_line(line, None, 18, True) == "updatedefaultentry":
            if line.find("true") == -1:
                self.update_default = False

        if self.__strip_line(line, None, 11, True) == "alternative":
            if line.find("true") == -1:
                self.create_alternative = False

    def __read_config(self):
        """Read grub configuration file, pass lines to __evaluate()."""
        grub_lines = utils.read_lines_from_file(self.menu)
        for line in grub_lines:
            self.__evaluate(line)
        self.__find_separator()

    def __check_themes(self):
        """Check for installed themes, send info to class variables."""
        self.grub_images = []
        if self.__get_line_number("splash") != -1:
            grub_lines = utils.read_lines_from_file(self.menu)
            location = self.__get_line_number("splash")
            splash_line = grub_lines[location].strip()
            correct_path = splash_line.find(self.groot + 
                                            self.mounted_splashdir)
            if correct_path != -1:
                location = splash_line.rfind('/')
                file_name = splash_line[location + 1:].replace('\\', '')
                suffix = file_name.find(".xpm.gz")
                if suffix != -1:
                    name = file_name[:suffix]
                    for dirfile in os.listdir(self.mounted_splashdir):
                        if file_name == dirfile:
                            self.default_image = name

        grub_files = os.listdir(self.mounted_splashdir)
        for grub_file in grub_files:
            end = grub_file[grub_file[:-3].rfind("."):]
            if end == ".xpm.gz":
                self.grub_images.append(grub_file[:-7])

    def __update_grub_colors(self):
        """Update Grub color line based on the class variables."""
        first_blink = ""
        last_blink = ""
        if self.normal_blink:
            first_blink = "blink-"
        if self.highlighted_blink:
            last_blink = "blink-"
        color_line = "color " + first_blink + self.normal_foreground + "/" + \
                     self.normal_background + " " + last_blink + \
                     self.highlighted_foreground + "/" + \
                     self.highlighted_background + "\n"
        if not self.use_colors:
            color_line = "#" + color_line
        self.__change_config("color", None, color_line)

    def __get_line_number(self, identifier):
        """Return the number of the line that 
        begin with the string identifier.
        """
        lines = utils.read_lines_from_file(self.menu)
        length = len(identifier)
        tracker = 0
        for line in lines:
            if line.strip()[:1] == "#":
                line = line.strip()[1:]
            line = line.strip()[:length].strip()
            if line == identifier:
                return tracker
            tracker += 1
        return -1

    def __change_config(self, identifier, old_value, new_value):
        """Change the configuration file based on the passed values."""
        line_number = self.__get_line_number(identifier)
        lines = utils.read_lines_from_file(self.menu)
        if line_number == -1:
            line_number = 0
            lines.insert(0,"\n")
        line = lines[line_number]
        if old_value == None:
            lines[line_number] = new_value
        elif old_value == "vga=":
            place = line.find(old_value)
            end = line.find(" ", place)
            if place != -1:
                if end != -1:
                    line = line[:place] + new_value + line[end:]
                else:
                    line = line[:place] + new_value + "\n"
            else:
                line = line[:-1] + " " + new_value + "\n"
            lines[line_number] = line
        else:
            if old_value[0] != "#" and line.find(" " + old_value) != -1:
                old_value = " " + old_value

            if old_value[0] == "#" and line.find("# " + old_value[1:]) != -1:
                old_value = "# " + old_value[1:]

            line = line.replace(old_value, new_value)
            lines[line_number] = line

        utils.write_lines_to_file(self.menu, lines)

    def __find_separator(self):
        """Find the separator line, update variable."""
        title_number = 0
        for title in self.titles:
            if title == "Other operating systems:":
                self.separator = title_number
            title_number += 1

    def __fix_menu_lst_bug(self):
        """Take care of an annoying thing in menu.lst."""
        grub_lines = utils.read_lines_from_file(self.menu)
        password_lines = []
        for line in grub_lines:
            line.strip()
            if line[0] == "#":
                line = line[1:].strip()
            if line[:8] == "password":
                password_lines.append(line)
        if len(password_lines) == 2:
            self.__change_config(password_lines[0], None, "## " + 
                                 password_lines[0] + "\n")

    def __has_separate_boot_partition(self):
        """Try to find out if there is a separate boot partition.
        Return True if it is likely(If /etc/fstab
        has a line containing '/boot', that is)
        """
        for line in utils.read_lines_from_file(self.fstab):
            if line.find("/boot") != -1:
                return True
        return False

    def has_update_grub(self):
        """Returns True if update-grub exists.
        If not, we can only do simple things like changing timeout 
        and default boot options, menu password protection and managing themes
        """
        return self.has_advanced_options

    def get_default_boot(self):
        """Return the name of the default booted option.
        
        Return -1 if it is savedefault.
        
        """
        default_boot = self.default_boot
        titles = self.titles
        if default_boot != -1:
            if default_boot < len(titles):
                return titles[default_boot]
            return titles[0]
        return -1

    def get_titles(self):
        """Return names of the boot options, as a list"""
        titles = self.titles[:]
        if self.separator != -1:
            del titles[self.separator]
        return titles

    def set_default_boot(self, name):
        """Set the default booted option to name.
        
        -1 set it to savedefault.
        Return 0 if successful.
        Return 1 if failed.
        
        """
        if name == -1:
            self.default_boot = name
            self.__change_config("default", None, "default\t\t" + "saved\n")
        else:
            try:
                entries = self.titles
                default = entries.index(name)
                self.default_boot = default
                self.__change_config("default", None, "default\t\t" + str(default) + "\n")
            except:
                return 1
        return 0

    def get_timeout(self):
        """Return the timeout in seconds used for Grub menu"""
        return self.timeout

    def set_timeout(self, timeout):
        """Set the timeout in seconds used in the Grub menu.
        active = bool whether timeout is used
        timeout = number of seconds
        """
        active = self.use_timeout
        self.timeout = timeout
        if active:
            self.__change_config("timeout", None, "timeout\t\t" + str(timeout) + "\n")
        else:
            self.__change_config("timeout", None, "#timeout\t\t" + str(timeout) + "\n")

    def get_timeout_used(self):
        """Return True if timeout is used in Grub menu"""
        return self.use_timeout

    def set_timeout_used(self, active):
        """Return True if timeout is used in Grub menu"""
        timeout = self.timeout
        if active:
            self.__change_config("timeout", None, "timeout\t\t" + str(timeout) + "\n")
        else:
            self.__change_config("timeout", None, "#timeout\t\t" + str(timeout) + "\n")
        self.use_timeout = active

    def get_vga_code(self):
        """Return the Grub vga code used, as integer"""
        return self.vga

    def set_vga_code(self, vga):
        """Set the resolution based on Grub vga code
        vga = integer, grub vga code
        """
        self.vga = vga
        self.__change_config("defoptions", "vga=", "vga=" + str(vga))
        self.update_grub = True

    def get_boot_text_visible(self):
        """Boolean, returns whether a verbose boot is enabled"""
        return self.show_text

    def set_boot_text_visible(self, active):
        """Set whether a verbose boot is enabled
        active = boolean
        """
        self.show_text = active
        if active:
            self.__change_config( "defoptions", "quiet", "")
        else:
            self.__change_config( "defoptions", "\n", " quiet\n")
        self.update_grub = True

    def get_menu_visible(self):
        """Boolean, returns whether the grub menu is shown at boot"""
        return self.show_menu

    def set_menu_visible(self, active):
        """Set whether the grub menu is shown at boot
        active = boolean
        """
        self.show_menu = active
        if active:
            self.__change_config("hiddenmenu", None, "#hiddenmenu\n")
        else:
            self.__change_config("hiddenmenu", None, "hiddenmenu\n")

    def get_use_colors(self):
        """Boolean, returns whether colors are shown in the grub menu"""
        return self.use_colors

    def set_use_colors(self, active):
        """Set whether colors are shown in the grub menu
        active = boolean
        """
        self.use_colors = active
        self.__update_grub_colors()

    def get_color_normal_bg(self):
        """Get the name of the color used for non-highlighted background"""
        return self.normal_background

    def get_color_highlighted_bg(self):
        """Get the name of the color used for highlighted background"""
        return self.highlighted_background

    def get_color_normal_fg(self):
        """Get the name of the color used for non-highlighted foreground"""
        return self.normal_foreground

    def get_color_highlighted_fg(self):
        """Get the name of the color used for highlighted foreground"""
        return self.highlighted_foreground

    def get_color_blink_normal(self):
        """Boolean, returns whether non-highlighted entries blink"""
        return self.normal_blink

    def get_color_blink_highlight(self):
        """Boolean, returns whether highlighted entries blink"""
        return  self.highlighted_blink

    def set_color_normal_bg(self, color):
        """Set the name of the color used for non-highlighted background
        color = string, name of color
        """
        self.normal_background = color
        self.__update_grub_colors()

    def set_color_highlighted_bg(self, color):
        """Set the name of the color used for highlighted background
        color = string, name of color
        """
        self.highlighted_background = color
        self.__update_grub_colors()

    def set_color_normal_fg(self, color):
        """Set the name of the color used for non-highlighted foreground
        color = string, name of color
        """
        self.normal_foreground = color
        self.__update_grub_colors()

    def set_color_highlighted_fg(self, color):
        """Set the name of the color used for highlighted foreground
        color = string, name of color
        """
        self.highlighted_foreground = color
        self.__update_grub_colors()

    def set_color_blink_normal(self, active):
        """Set whether non-highlighted entries blink
        active = boolean
        """
        self.normal_blink = active
        self.__update_grub_colors()

    def set_color_blink_highlight(self, active):
        """Set whether highlighted entries blink
        active = boolean
        """
        self.highlighted_blink = active
        self.__update_grub_colors()

    def get_splash_visible(self):
        """Boolean, returns whether the Grub splash is visible"""
        return self.use_image

    def get_splash(self):
        """Returns the name of the currently active Grub splash"""
        return self.default_image

    def set_splash(self, active, image_name):
        """Set the name of the currently active Grub splash
        active = boolean, whether the grub splash should be shown
        """
        self.default_image = image_name
        self.show_splash = active
        image_name = image_name + ".xpm.gz"
        text = "\n#A splash image for the menu\n"
        if self.__get_line_number("splashimage") != -1:
            image_name = utils.fix_filename_spaces(image_name)
            if active:
                text = "splashimage=" + self.groot + self.splashdir
            else:
                text = "#splashimage=" + self.groot + self.splashdir
            self.__change_config("splashimage", None, text + image_name + "\n")
        else:
            for splash_file in os.listdir(self.mounted_splashdir):
                if image_name == splash_file:
                    image_name = utils.fix_filename_spaces(image_name)
                    if active:
                        text = text + "splashimage=" + \
                               self.groot + self.splashdir
                    else:
                        text = text + "#splashimage=" + \
                               self.groot + self.splashdir
                    self.__change_config("color", "\n", "\n" + 
                                         text + image_name + "\n")

    def get_images(self):
        """Return a list of names of the Grub splash images available"""
        return self.grub_images

    def add_image(self, filename):
        """Convert filename to correct format and add as a splashimage
        Return False if the image format is not supported.
        True if it was added successfully.
        Note that any spaces in the filename itself(not in the path) will be 
        removed since Grub does not appear to support them at this time.
        """
        pathless = filename[filename.rfind("/") + 1:]
        pathless = pathless.replace(' ', '')
        fixed_filename = utils.fix_filename_spaces(filename)
        end = filename.rfind(".")
        if not end == -1:
            if filename[end:] == ".gz":
                end = filename[:-3].rfind(".")
            if filename[end:] == ".xpm.gz":
                shutil.copy(filename, self.mounted_splashdir + pathless)
                self.__check_themes()
            elif filename[end:] == ".xpm":
                os.system("gzip -c " + fixed_filename + " > " + 
                          self.mounted_splashdir + pathless + ".gz")
                self.__check_themes()
            elif self.convert_exist and os.system('file ' + fixed_filename + 
                           ' | grep -oE "image|bitmap"') == 0:
                end = pathless.rfind(".")
                os.system("convert " + fixed_filename +
                          " -resize 640x480 -colors 14 " +
                          pathless[:end] + ".xpm")
                os.system("gzip -c " + pathless[:end] + ".xpm" + " > " +
                          self.mounted_splashdir + pathless[:end] + ".xpm.gz")
                os.system("rm -f " + pathless[:end] + ".xpm")
                self.__check_themes()
            else:
                return False
            return True

    def remove_image(self, name):
        """Removes Grub splash image
        name = string, name of image
        """
        filename = self.mounted_splashdir + name + ".xpm.gz"
        os.remove(filename)
        self.__check_themes()

    def get_splash_active(self):
        """Boolean, returns whether a boot splash is shown"""
        return self.show_splash

    def set_splash_active(self, active):
        """Set whether a boot splash is shown
        active = boolean
        """
        self.show_splash = active
        if active:
            self.__change_config("defoptions", "\n", " splash\n")
        else:
            self.__change_config("defoptions", "splash", "")
        self.update_grub = True

    def get_password_protection(self):
        """Boolean, returns whether the Grub menu is password protected"""
        return self.password_protect

    def set_password_protection(self, active):
        """Set whether the Grub menu is password protected
        active = boolean
        """
        self.password_protect = active
        if active:
            self.__change_config("password", "#password", "password")
        else:
            self.__change_config("password", "password", "#password")

    def get_protect_rescuemode(self):
        """Boolean, returns whether the alternate boot option
        is password protected
        """
        return self.protect_rescuemode

    def set_protect_rescuemode(self, active):
        """Set whether the alternate boot option is password protected
        active = boolean
        """
        self.protect_rescuemode = active
        if active:
            self.__change_config("lockalternative", None, 
                                 "# lockalternative=true\n")
        else:
            self.__change_config("lockalternative", None, 
                                 "# lockalternative=false\n")
        self.update_grub = True

    def get_protect_oldmode(self):
        """Boolean, returns whether old boot options are password protected"""
        return self.protect_oldmode

    def set_protect_oldmode(self, active):
        """Set whether old boot options are password protected
        active = boolean
        """
        self.protect_oldmode = active
        if active:
            self.__change_config("lockold", None, "# lockold=true\n")
        else:
            self.__change_config("lockold", None, "# lockold=false\n")
        self.update_grub = True

    def update_password(self, password, active=False):
        """Set password for grub menu, and whether
        password protection is active
        
        active = boolean
        password = string, must be at least four characters
        """
        self.password_protect = active
        if len(password) > 3:
            communication = Popen(['grub-md5-crypt'], stdin=PIPE, 
                                  stdout=PIPE, close_fds=True)
            password = communication.communicate(password + "\n" + password + 
                                                 "\n")[0].rsplit('\n')[2]
            password = "password --md5 " + password
            if not active:
                password = "#" + password

            self.__change_config("password", None, password)

        else:
            if len(password) < 4:
                raise SystemExit('Password must be at least 4 characters')
            else:
                raise SystemExit('Passwords do not match')

    def get_limit_kernel(self):
        """Boolean, returns whether the number of kernels stored is limited"""
        if type(self.kernel_limit) == type(""):
            return False
        else:
            return True

    def get_kernel_limit(self):
        """Returns the maximum number of kernels stored as an integer.
        If there is no limit, return False"""
        if type(self.kernel_limit) == type(""):
            return False
        else:
            return self.kernel_limit

    def set_kernel_limit(self, active, number):
        """Set the limit of kernels stored.
        active = boolean, whether there is a limit
        number = integer, number of kernels
        """
        if not active:
            number = "all"
        self.__change_config("howmany", None, "# howmany=" +
                             str(number) + "\n")
        self.kernel_limit = number
        self.update_grub = True

    def get_memtest(self):
        """Boolean, returns whether memtest86 is shown in the boot menu"""
        return self.memtest

    def set_memtest(self, active):
        """Set whether memtest86 is shown in the boot menu
        active = boolean
        """
        self.memtest = active
        if active:
            self.__change_config("memtest86", None, "# memtest86=true\n")
        else:
            self.__change_config("memtest86", None, "# memtest86=false\n")
        self.update_grub = True

    def get_update_default(self):
        """Boolean, returns whether the default entry is updated"""
        return self.update_default

    def set_update_default(self, active):
        """Set whether the default entry is updated
        active = boolean
        """
        self.update_default = active
        if active:
            self.__change_config("updatedefaultentry", None, 
                                 "# updatedefaultentry=true\n")
        else:
            self.__change_config("updatedefaultentry", None, 
                                 "# updatedefaultentry=false\n")
        self.update_grub = True

    def get_create_alternative(self):
        """Boolean, returns whether an alternate boot option is created"""
        return self.create_alternative

    def set_create_alternative(self, active):
        """Set whether an alternate boot option is created
        active = boolean
        """
        self.create_alternative = active
        if active:
            self.__change_config("alternative", None, "# alternative=true\n")
        else:
            self.__change_config("alternative", None, "# alternative=false\n")
        self.update_grub = True

    def get_image_formats(self):
        """Get a list of the image formats that can be used
        for the grub splash"""
        return self.image_formats

    def format_floppy(self):
        """Formats a floppy
        returns 0 if it was successful
        returns 1 if a floppy was not found
        returns 3 if there was an OSError
        returns a code < 0 or > 3 for other errors
        """
        return utils.format_floppy()

    def make_floppy(self):
        """Writes a Grub boot floppy.
        Returns 0 if it was successful.
        Returns 1 if there was an OSError
        returns a code < 0 or > 1 for other errors
        """
        return utils.make_floppy(self.grub_install_command, self.menu)

    def restore_config(self):
        """Copy back the grub config file that was backed up
        the first time this program was run
        Returns False if the backup file does not exist."""

        if os.path.isfile(self.menu + ".backup"):
            shutil.copy(self.menu + ".backup", self.menu)
            return True
        else:
            return False

    def do_shutdown_tasks(self):
        """Does any post-config tasks nessecary"""
        if self.update_grub:
            os.system(self.update_grub_command)

    def get_user_edited_file(self):
        """Returns True if it is likely the user has edited the config file.
        ie, some comments used by update-grub are missing"""
        return self.user_edited_file

