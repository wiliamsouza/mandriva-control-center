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
import re
from subprocess import call

def fix_filename_spaces(filename):
    """Prepend spaces in filename with '\' if it is not already there"""
    filename = filename.strip()
    parts = filename.split(' ')
    filename = ''
    for part in parts:
        if part == '':
            part = '\ '
        elif part[-1] != '\\':
            part += '\ '
        filename += part
    filename = filename.strip()
    if filename[-1] == '\\':
        filename = filename[:-1]
    filename = filename.strip()
    return filename

def get_line_number(filename, identifier):
    """Return the number of the line in filename that begin with identifier.

    Return -1 if there is no match.

    """
    lines = read_lines_from_file(filename)
    length = len(identifier)
    for i, line in enumerate(lines):
        line = line.strip()[:length].strip()
        if line == identifier:
            return i
    return -1

def extract_number(line):
    """Extract a number from line.
    
    Return -1 if failed.
    
    """
    number_filter = re.compile('[0-9]+')
    match = number_filter.search(line)
    if match:
        return int(match.group())
    return -1

def get_and_trim_line(filename, identifier):
    """
    Read file, find line that begin with identifier, remove that from line.

    Return -1 if line cannot be found.

    """
    line_number = get_line_number(filename, identifier)
    if line_number == -1:
        return -1
    lines = read_lines_from_file(filename)
    line = lines[line_number]
    length = len(identifier)
    line = line[length:]
    return line.strip()

def read_lines_from_file(filename):
    """Read file filename, return list of lines in the file."""
    try:
        input_file = open(filename, 'r')
        lines = input_file.readlines()
        input_file.close()
        return lines
    except IOError:
        raise SystemExit('File %s does not exist.' % filename)

def write_lines_to_file(filename, lines):
    """Write the list lines to file filename."""
    output_file = open(filename, 'w')
    for out_line in lines:
        output_file.write(out_line)
    output_file.close()

def format_floppy():
    """Format a floppy.

    Return 0 if it was successful.
    Return 1 if a floppy was not found.
    Return 3 if there was an OSError.
    Return a code < 0 or > 3 for other errors.

    """
    try:
        retcode = call('/sbin/mke2fs /dev/fd0', shell=True)
        if retcode < 0:
            print 'Child was terminated by signal', -retcode
        return retcode
    except OSError, e:
        print 'Execution failed:', e
        return 3

def make_floppy(grub_install_command, config_file):
    """Write a Grub boot floppy.

    Return 0 if it was successful.
    Return 1 if there was an OSError.
    Return a code < 0 or > 1 for other errors.

    """
    dir_preexisting = True

    if not os.path.isdir('/mnt/floppysum'):
        os.mkdir('/mnt/floppysum')
        dir_preexisting = False

    commands = [
        'mount -t ext2 /dev/fd0 /mnt/floppysum',
        grub_install_command + ' --root-directory=/mnt/floppysum fd0',
        'cp ' + config_file + ' /mnt/floppysum/' + config_file,
        'umount /mnt/floppysum']
    try:
        for command in commands:
            retcode = call(command, shell=True)
            if not retcode == 0:
                print 'Child was terminated by signal', -retcode
                return retcode

    except OSError, e:
        print 'Execution failed:', e
        return 1

    if not dir_preexisting:
        os.rmdir('/mnt/floppysum')
    return 0
    
def get_resolution():
    pipe = os.popen('xrandr')
    data = pipe.read()
    pipe.close()
    matches = re.search('current (\d+) x (\d+)', data)
    return matches.group(1) + 'x' + matches.group(2)

def set_resolution(resolution):
    os.system('xrandr --size ' + resolution)
