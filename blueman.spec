# TODO
# unpackaged
#   /usr/lib/nautilus-sendto/plugins/libnstblueman.a
#   /usr/lib/nautilus-sendto/plugins/libnstblueman.la
#   /usr/lib/nautilus-sendto/plugins/libnstblueman.so
Summary:	Blueman - bluetooth management utility for GNOME
Name:		blueman
Version:	1.23
Release:	3
License:	GPL
Group:		Applications
Source0:	http://download.tuxfamily.org/blueman/%{name}-%{version}.tar.gz
# Source0-md5:	f0bee59589f4c23e35bf08c2ef8acaef
Patch0:		missing-icons.patch
Patch1:		icon-active.patch
URL:		http://blueman.tuxfamily.org/
BuildRequires:	bluez-libs-devel
BuildRequires:	gettext-devel
BuildRequires:	gnome-bluetooth-devel
BuildRequires:	intltool
BuildRequires:	librsvg
BuildRequires:	pkgconfig
BuildRequires:	python-Pyrex
BuildRequires:	python-dbus-devel
BuildRequires:	python-devel >= 2.5
BuildRequires:	python-distutils-extra
BuildRequires:	python-pynotify-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	startup-notification-devel
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires:	bluez-libs >= 4.25
Requires:	bluez-utils >= 4.25
Requires:	gtk+2 >= 2.12
%pyrequires_eq	python = %py_ver
Requires:	python-bluetooth
Requires:	python-dbus
Requires:	python-pygtk-gtk
Requires:	python-pynotify
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
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure \
	--disable-hal

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

for s in 16 32 48 ; do
	install -d $RPM_BUILD_ROOT%{_iconsdir}/hicolor/${s}x${s}/status
	rsvg-convert -w $s -h $s -o $RPM_BUILD_ROOT%{_iconsdir}/hicolor/${s}x${s}/status/blueman-tray.png \
		data/icons/hicolor/scalable/status/blueman-tray.svg
	rsvg-convert -w $s -h $s -o $RPM_BUILD_ROOT%{_iconsdir}/hicolor/${s}x${s}/status/blueman-tray-active.png \
		data/icons/hicolor/scalable/status/blueman-tray-active.svg
	rsvg-convert -w $s -h $s -o $RPM_BUILD_ROOT%{_iconsdir}/hicolor/${s}x${s}/status/blueman-tray-disabled.png \
		data/icons/hicolor/scalable/status/blueman-tray-disabled.svg
done
install -d $RPM_BUILD_ROOT%{_iconsdir}/hicolor/scalable/status
install data/icons/hicolor/scalable/status/*.svg $RPM_BUILD_ROOT%{_iconsdir}/hicolor/scalable/status

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/system.d/org.blueman.Mechanism.conf
%attr(755,root,root) %{_libdir}/%{name}-mechanism
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/dbus-1/system-services/org.blueman.Mechanism.service
%{_iconsdir}/hicolor/scalable/*/*.svg
%{_iconsdir}/hicolor/*/*/*.png
%{_datadir}/polkit-1/actions/org.blueman.policy
%{_desktopdir}/blueman-manager.desktop
%{py_sitedir}/*.so
%{py_sitedir}/*.a
%{py_sitedir}/*.la
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xdg/autostart/blueman.desktop
%{_mandir}/man1/*.1*
%{_datadir}/dbus-1/services/blueman-applet.service
%{py_sitescriptdir}/%{name}
