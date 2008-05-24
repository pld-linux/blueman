Summary:	Blueman - bluetooth management utility for GNOME
Name:		blueman
Version:	0.5
Release:	0.1
License:	GPL
Group:		Applications
Source0:	http://download.tuxfamily.org/blueman/%{name}_%{version}.tar.gz
# Source0-md5:	f66861ce1d3c2162dc6682c0b67b8397
URL:		http://blueman.tuxfamily.org/
BuildRequires:	bluez-libs-devel
BuildRequires:	gnome-bluetooth-devel
BuildRequires:	python-Pyrex
BuildRequires:	python-devel
BuildRequires:	python-devel >= 2.5
BuildRequires:	python-distutils-extra
BuildRequires:	rpm-pythonprov
Requires:	bluez-libs >= 2.20
Requires:	bluez-utils
Requires:	gtk+2 >= 2.12
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Blueman is a GTK+ bluetooth management utility for GNOME using bluez
dbus backend. The aim is to create a full featured graphical bluetooth
manager for Linux.

Features:

- Easy to use interface
- Storing Favourite devices
- Send files
- Browse files on devices
- List all seen devices
- View Local/Remote Device information
- View transfer speeds and link quality
- Configure local devices
- Manage Pairing (Bonding)
- Host/Connect to Personal Area Networks
- Bind services to /dev/rfcomm ports, for eg. connecting via gprs
- Connect and receive connections from: audio, network, input and
  serial devices

%prep
%setup -q -n %{name}_%{version}

%build
%{__sed} -e 's,lib/,%{_lib}/,g' setup.py
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT

%{__python} setup.py install \
	--root=$RPM_BUILD_ROOT

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README
#%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bluetooth/network.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dbus-1/system.d/org.blueman.Mechanism.conf
%attr(755,root,root) %{_libdir}/%{name}
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/dbus-1/system-services/org.blueman.Mechanism.service
%{_iconsdir}/hicolor/scalable/apps/*.svg
%{_iconsdir}/hicolor/*/apps/*.png
%{_datadir}/PolicyKit/policy/org.blueman.policy
%{_desktopdir}/blueman.desktop
%{py_sitedir}/%{name}
%{py_sitedir}/%{name}-%{version}-py*.egg-info
