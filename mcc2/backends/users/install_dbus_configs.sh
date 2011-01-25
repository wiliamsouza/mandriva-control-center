#!/bin/sh

echo 'com.mandriva.mcc2.Users.service'
cp com.mandriva.mcc2.Users.service /usr/share/dbus-1/system-services/

echo 'com.mandriva.mcc2.users.policy'
cp com.mandriva.mcc2.users.policy /usr/share/polkit-1/actions/

echo 'com.mandriva.mcc2.Users.conf'
cp com.mandriva.mcc2.Users.conf /etc/dbus-1/system.d/
