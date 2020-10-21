# Conditional build:
%bcond_without	cinnamon	# build without nemo support
%bcond_without	gnome		# build without nautilus support
%bcond_without	mate		# build without caja support
%bcond_without	xfce		# build without Thunar support

Summary:	Blueman - bluetooth management utility for GNOME
Name:		blueman
Version:	2.1.3
Release:	2
License:	GPL
Group:		X11/Applications
Source0:	https://github.com/blueman-project/blueman/releases/download/%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	b341822c8362bf9619fbbc22c957b00c
URL:		https://github.com/blueman-project/blueman
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
BuildRequires:	bluez-libs-devel >= 5.0
%{?with_mate:BuildRequires:	caja-python-devel}
%{?with_cinnamon:BuildRequires:	cinnamon-nemo-python-devel}
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.32
BuildRequires:	gtk+3-devel >= 3.12
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libtool
%{?with_gnome:BuildRequires:	nautilus-python-devel}
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	polkit-devel
BuildRequires:	python-pygobject3-common-devel >= 3.27.2
BuildRequires:	python3-Cython
BuildRequires:	python3-devel >= 3.3
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.527
BuildRequires:	systemd-units
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires(post,preun,postun):	systemd-units >= 38
Requires:	bluez-libs >= 5.0
Requires:	bluez-utils >= 5.0
Requires:	glib2 >= 1:2.32
Requires:	gtk+3 >= 3.12
Requires:	python3 >= %py3_ver
Requires:	python3-pygobject3 >= 3.27.2
Suggests:	libappindicator-gtk3
Suggests:	pulseaudio-bluetooth
Suggests:	pulseaudio-hal
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

%package caja
Summary:	Blueman plugin for Caja
Summary(pl.UTF-8):	Wtyczka Blueman-a dla managera plików Caja
Group:		X11/Applications
Requires:	%{name} = %{version}
Requires:	caja-python

%description caja
Blueman plugin for Caja.

%description caja -l pl.UTF-8
Wtyczka Blueman-a dla managera plików Caja.

%package nautilus
Summary:	Blueman plugin for Nautilus
Summary(pl.UTF-8):	Wtyczka Blueman-a dla Nautilus-a
Group:		X11/Applications
Requires:	%{name} = %{version}
Requires:	nautilus-python

%description nautilus
Blueman plugin for Nautilus.

%description nautilus -l pl.UTF-8
Wtyczka Blueman-a dla Nautilus-a.

%package nemo
Summary:	Blueman plugin for Nemo
Summary(pl.UTF-8):	Wtyczka Blueman-a dla managera plików Nemo.
Group:		X11/Applications
Requires:	%{name} = %{version}
Requires:	cinnamon-nemo-python

%description nemo
Blueman plugin for Nautilus.

%description nemo -l pl.UTF-8
Wtyczka Blueman-a dla managera plików Nemo.

%package thunar
Summary:	Blueman plugin for Thunar
Summary(pl.UTF-8):	Wtyczka Blueman-a dla Thunar-a
Group:		X11/Applications
Requires:	%{name} = %{version}

%description thunar
Blueman plugin for Thunar.

%description thunar -l pl.UTF-8
Wtyczka Blueman-a dla Thunar-a.

%prep
%setup -q

%build
%configure \
	CYTHONEXEC=/usr/bin/cython3 \
	NETWORKTOOLS=/sbin/ip \
	--disable-static \
	--disable-schemas-compile \
	--enable-polkit \
	%{__enable_disable mate caja-sendto} \
	%{__enable_disable cinnamon nemo-sendto} \
	%{__enable_disable gnome nautilus-sendto} \
	%{__enable_disable xfce thunar-sendto} \
	--enable-settings-integration

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/python3.8/site-packages/_blueman.la

# DO NOT RUN py_postclean - breaks plugins and everything

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
glib-compile-schemas %{_datadir}/glib-2.0/schemas
%service %{name}-mechanism restart
%systemd_post %{name}-mechanism.service

%preun
if [ "$1" = "0" ]; then
        %service -q %{name}-mechanism stop
fi
%systemd_preun %{name}-mechanism.service

%postun
%update_icon_cache hicolor
glib-compile-schemas %{_datadir}/glib-2.0/schemas
%systemd_reload

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.md CHANGELOG.md COPYING FAQ
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/system.d/org.blueman.Mechanism.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xdg/autostart/blueman.desktop
%attr(755,root,root) %{_bindir}/blueman-adapters
%attr(755,root,root) %{_bindir}/blueman-applet
%attr(755,root,root) %{_bindir}/blueman-assistant
%attr(755,root,root) %{_bindir}/blueman-manager
%attr(755,root,root) %{_bindir}/blueman-report
%attr(755,root,root) %{_bindir}/blueman-sendto
%attr(755,root,root) %{_bindir}/blueman-services
%attr(755,root,root) %{_bindir}/blueman-tray
%{_mandir}/man1/blueman-adapters.1*
%{_mandir}/man1/blueman-applet.1*
%{_mandir}/man1/blueman-assistant.1*
%{_mandir}/man1/blueman-manager.1*
%{_mandir}/man1/blueman-report.1
%{_mandir}/man1/blueman-sendto.1*
%{_mandir}/man1/blueman-services.1*
%{_mandir}/man1/blueman-tray.1*
%attr(755,root,root) %{_libexecdir}/%{name}-mechanism
%attr(755,root,root) %{_libexecdir}/%{name}-rfcomm-watcher
%{_datadir}/%{name}
%{_datadir}/dbus-1/system-services/org.blueman.Mechanism.service
%{_desktopdir}/blueman-manager.desktop
%{_desktopdir}/blueman-adapters.desktop
%{_iconsdir}/hicolor/scalable/*/*.svg
%{_iconsdir}/hicolor/*/*/*.png
%dir %{_pixmapsdir}/blueman
%{_pixmapsdir}/blueman/blueman-*.png
%{_datadir}/glib-2.0/schemas/org.blueman.gschema.xml
%{systemdunitdir}/blueman-mechanism.service
%{systemduserunitdir}/blueman-applet.service
%{_datadir}/dbus-1/services/org.blueman.Applet.service
%{_datadir}/polkit-1/actions/org.blueman.policy
%{_datadir}/polkit-1/rules.d/blueman.rules
%attr(755,root,root) %{_libdir}/python3.8/site-packages/_blueman.so
%{_libdir}/python3.8/site-packages/%{name}

%if %{with mate}
%files caja
%defattr(644,root,root,755)
%{_datadir}/caja-python/extensions/caja_blueman_sendto.py
%endif

%if %{with gnome}
%files nautilus
%defattr(644,root,root,755)
%{_datadir}/nautilus-python/extensions/nautilus_blueman_sendto.py
%endif

%if %{with cinnamon}
%files nemo
%defattr(644,root,root,755)
%{_datadir}/nemo-python/extensions/nemo_blueman_sendto.py
%endif

%if %{with xfce}
%files thunar
%defattr(644,root,root,755)
%{_datadir}/Thunar/sendto/thunar-sendto-blueman.desktop
%endif
