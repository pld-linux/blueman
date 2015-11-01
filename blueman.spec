Summary:	Blueman - bluetooth management utility for GNOME
Name:		blueman
Version:	2.0
Release:	2
License:	GPL
Group:		X11/Applications
Source0:	https://github.com/blueman-project/blueman/releases/download/%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	d95270145475ce41a33bf7390afe3428
URL:		https://github.com/blueman-project/blueman
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bluez-libs-devel >= 4.61
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 2.32
BuildRequires:	gtk+3-devel >= 3.12
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libtool
BuildRequires:	pkgconfig >= 0.9.0
BuildRequires:	python-Cython
BuildRequires:	python-dbus
BuildRequires:	python-devel >= 2.7
BuildRequires:	python-pygobject3-common-devel
BuildRequires:	rpm-pythonprov
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires:	bluez-libs >= 4.25
Requires:	bluez-utils >= 4.25
Requires:	gtk+3 >= 3.12
Requires:	python >= %py_ver
Requires:	python-appindicator-gtk2
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

%package thunar
Summary:	Blueman plugin for Thunar
Summary(pl.UTF-8):	Wtyczka Blueman-a dla Thunar-a
Group:		X11/Applications

%description thunar
Blueman plugin for Thunar.

%description thunar -l pl.UTF-8
Wtyczka Blueman-a dla Thunar-a.

%prep
%setup -q

%build
%{__aclocal}
%{__autoheader}
%{__libtoolize}
%{__intltoolize}
%{__automake}
%{__autoconf}
%configure \
	--enable-xfce-settings=yes \
	--disable-static \
	--disable-schemas-compile \

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/_blueman.la

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
glib-compile-schemas %{_datadir}/glib-2.0/schemas

%postun
%update_icon_cache hicolor
glib-compile-schemas %{_datadir}/glib-2.0/schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.md CHANGELOG.md COPYING FAQ
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/system.d/org.blueman.Mechanism.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xdg/autostart/blueman.desktop
%attr(755,root,root) %{_bindir}/blueman-adapters
%attr(755,root,root) %{_bindir}/blueman-applet
%attr(755,root,root) %{_bindir}/blueman-assistant
%attr(755,root,root) %{_bindir}/blueman-browse
%attr(755,root,root) %{_bindir}/blueman-manager
%attr(755,root,root) %{_bindir}/blueman-report
%attr(755,root,root) %{_bindir}/blueman-sendto
%attr(755,root,root) %{_bindir}/blueman-services
%{_mandir}/man1/blueman-adapters.1*
%{_mandir}/man1/blueman-applet.1*
%{_mandir}/man1/blueman-assistant.1*
%{_mandir}/man1/blueman-browse.1*
%{_mandir}/man1/blueman-manager.1*
%{_mandir}/man1/blueman-report.1
%{_mandir}/man1/blueman-sendto.1*
%{_mandir}/man1/blueman-services.1*
%attr(755,root,root) %{_libdir}/%{name}-mechanism
%attr(755,root,root) %{_libdir}/%{name}-rfcomm-watcher
%{_datadir}/%{name}
%{_datadir}/dbus-1/system-services/org.blueman.Mechanism.service
%{_desktopdir}/blueman-manager.desktop
%{_desktopdir}/blueman-adapters.desktop
%{_iconsdir}/hicolor/scalable/*/*.svg
%{_iconsdir}/hicolor/*/*/*.png
%dir %{_pixmapsdir}/blueman
%{_pixmapsdir}/blueman/blueman-*.png
%{_datadir}/glib-2.0/schemas/org.blueman.gschema.xml
%{_datadir}/dbus-1/services/blueman-applet.service
%{_datadir}/polkit-1/actions/org.blueman.policy
%attr(755,root,root) %{py_sitedir}/_blueman.so
%{py_sitescriptdir}/%{name}

%files thunar
%defattr(644,root,root,755)
%{_datadir}/Thunar/sendto/thunar-sendto-blueman.desktop
