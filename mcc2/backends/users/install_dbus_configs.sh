#!/bin/sh

SERVICE_DIR='/usr/share/dbus-1/system-services/'
SERVICE_NAME='org.mandrivalinux.mcc2.Users.service'

POLICY_DIR='/usr/share/polkit-1/actions/'
POLICY_NAME='org.mandrivalinux.mcc2.users.policy'

CONFIG_DIR='/etc/dbus-1/system.d/'
CONFIG_NAME='org.mandrivalinux.mcc2.Users.conf'

echo $SERVICE_DIR$SERVICE_NAME
cp $SERVICE_NAME $SERVICE_DIR

echo $POLICY_DIR$POLICY_NAME
cp $POLICY_NAME $POLICY_DIR

echo $CONFIG_DIR$CONFIG_NAME
cp $CONFIG_NAME $CONFIG_DIR
