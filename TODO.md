====
TODO
====

This is todo file for Mandriva Control Center 2

CODE
====

Backend
-------

 * [DONE] Add a common policykit authentication for privileged method execution
   then user can't enter the root passwors for each privileged task for
   a sort period of time. By now the user may enter the root password for
   stop, restar and start services we should change that.

 * [DONE] Add an exception handler to dbus connection in all classes.

 * [DONE] Add backends dbus interface method stop.

 * Add support to rpm stop dbus interfaces when updating or removing packages.

 * Merge sshd key options because it's only used in sshd_config to ensure
   line not be more than 80 characters.

 * Rename sshd HostKey protocol version 2 to HostKeyRSA and HostKeyDSA to avoid
   confusion.

 * Check if d-bus interface is running before start to avoid have two instance
   running.

 * [DONE] Make policykit authorization type be configurable for all methods that use it.

Frontend
--------

 * Add support to change users avatar.
 * add i18n to Users and Services.
 * [DONE]Solve qt-components-desktop ChoiceList bug.
 * Change the UI rosa mockups.

RPM
---

 *

TESTS
=====

 *
