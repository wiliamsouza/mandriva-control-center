Name:           mandriva-control-center
Version:        0.1
Release:        %mkrel 1
Summary:        Mandriva control enter
Group:          Development/Python
License:        Apache License
URL:            http://www.mandriva.com
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
#BuildArch:	noarch
Requires:	systemd
Requires:	libuser
Requires:	libuser-python
Requires:	python-qt4
Requires:	python-dbus
%py_requires -d

%description
Mandriva control center preview

%prep
%setup -q -n %{name}-%{version}

%build
unset PYTHONDONTWRITEBYTECODE
%{__python} setup.py build

%install
unset PYTHONDONTWRITEBYTECODE
rm -rf %{buildroot}
%{__python} setup.py install --install-lib=/usr/share/mandriva  --install-data=/usr/share/mandriva -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/mcc2-users
%{_bindir}/mcc2-services
%{_sysconfdir}/dbus-1/system.d/org.mandrivalinux.mcc2.Services.conf
%{_sysconfdir}/dbus-1/system.d/org.mandrivalinux.mcc2.Sshd.conf
%{_sysconfdir}/dbus-1/system.d/org.mandrivalinux.mcc2.Users.conf
%{_sysconfdir}/dbus-1/system.d/org.mandrivalinux.mcc2.Grub.conf
%{_datadir}/dbus-1/system-services/org.mandrivalinux.mcc2.Services.service
%{_datadir}/dbus-1/system-services/org.mandrivalinux.mcc2.Sshd.service
%{_datadir}/dbus-1/system-services/org.mandrivalinux.mcc2.Users.service
%{_datadir}/dbus-1/system-services/org.mandrivalinux.mcc2.Grub.service
%{_datadir}/polkit-1/actions/org.mandrivalinux.mcc2.policy
%{_datadir}/polkit-1/actions/org.mandrivalinux.mcc2.services.policy
%{_datadir}/polkit-1/actions/org.mandrivalinux.mcc2.sshd.policy
%{_datadir}/polkit-1/actions/org.mandrivalinux.mcc2.grub.policy
%{_datadir}/polkit-1/actions/org.mandrivalinux.mcc2.users.policy
%{_datadir}/kde4/services/settings-mandriva.desktop
%{_datadir}/apps/mandriva-control-center/*
%{_datadir}/applications/kde4/mcc2-services.desktop
%{_datadir}/applications/kde4/mcc2-users.desktop
%{_datadir}/mandriva/*
