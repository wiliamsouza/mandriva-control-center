import dbus
bus = dbus.SystemBus()
proxy = bus.get_object(
    'org.mandrivalinux.mcc2.Users',
    '/org/mandrivalinux/mcc2/Users')
interface = dbus.Interface(proxy, 'org.mandrivalinux.mcc2.Users')
result = interface.GroupDetails('paula')
print result
#print type(result)
#d = dict(result)
#print type(d)
#print d
#print dir(result)
new_dict = {}
for key, value in result.items():
    if key == 'members':
        new_list = []
        for list_value in value:
            new_list.append(str(list_value))
        new_dict[str(key)] = new_list
        break
    new_dict[str(key)] = str(value)
print new_dict