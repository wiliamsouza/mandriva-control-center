#!/bin/sh

echo 'com.mandriva.mcc2.Services.service'
cp com.mandriva.mcc2.Services.service /usr/share/dbus-1/system-services/com.mandriva.mcc2.Services.service

echo 'com.mandriva.mcc2.services.policy'
cp com.mandriva.mcc2.services.policy /usr/share/polkit-1/actions/com.mandriva.mcc2.services.policy

echo 'com.mandriva.mcc2.Services.conf'
cp com.mandriva.mcc2.Services.conf /etc/dbus-1/system.d/com.mandriva.mcc2.Services.conf
