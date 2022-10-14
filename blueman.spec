#
# Conditional build:
%bcond_without	cinnamon	# build without nemo support
%bcond_without	gnome		# build without nautilus support
%bcond_without	mate		# build without caja support
%bcond_without	xfce		# build without Thunar support

Summary:	Blueman - Bluetooth management utility for GNOME
Summary(pl.UTF-8):	Blueman - narzędzie do zarządzania łącznością Bluetooth dla GNOME
Name:		blueman
Version:	2.3.4
Release:	1
License:	GPL v3+
Group:		X11/Applications
Source0:	https://github.com/blueman-project/blueman/releases/download/%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	d611197e62129f3d89c6d3152ef5adf9
URL:		https://github.com/blueman-project/blueman
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1:1.16.3
BuildRequires:	bluez-libs-devel >= 5.48
%{?with_mate:BuildRequires:	caja-python-devel}
%{?with_cinnamon:BuildRequires:	cinnamon-nemo-python-devel}
BuildRequires:	gettext-tools >= 0.19.7
BuildRequires:	glib2-devel >= 1:2.32
BuildRequires:	libtool
%{?with_gnome:BuildRequires:	nautilus-python-devel}
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	polkit-devel
BuildRequires:	python-pygobject3-common-devel >= 3.27.2
BuildRequires:	python3-Cython
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.011
BuildRequires:	systemd-units
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires(post,preun,postun):	systemd-units >= 1:250.1
Requires:	bluez >= 5.48
Requires:	dbus >= 1.9.18
Requires:	glib2 >= 1:2.32
Requires:	gtk+3 >= 3.22
Requires:	pango
Requires:	python3 >= %py3_ver
Requires:	python3-pycairo
Requires:	python3-pygobject3 >= 3.27.2
Requires:	systemd-units >= 1:250.1
Suggests:	NetworkManager-libs
Suggests:	iproute2
Suggests:	pulseaudio-bluetooth
Suggests:	pulseaudio-hal
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Blueman is a GTK+ Bluetooth management utility for GNOME using bluez
DBus backend. The aim is to create a full featured graphical Bluetooth
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

%description -l pl.UTF-8
Blueman to opate na GTK+ narzędzie do zarządzania łącznością Bluetooth
dla GNOME, wykorzystujące backend DBus bluez. Celem jest stworzenie w
pełni funkcjonalnego graficznego zarządcy Bluetooth dla Linuksa.

Możliwości:
- łatwy w użyciu interfejs
- przechowywanie ulubionych urządzeń
- wysyłanie plików
- przeglądanie plików na urządzeniach
- wypisywanie wszystkich widocznych urządzeń
- informacje o lokalnych/zdalnych urządzeniach
- pokazywanie szybkości przesyłania i jakości połączenia
- konfigurowanie urządzeń lokalnych
- zarządzanie parowaniem
- hostowanie/łączenie się z sieciami prywatnymi
- podpinanie urządzeń do portów /dev/rfcomm, np. do połączeń GPRS
- nawiązywanie i odbieranie połączeń z urządzeń: dźwiękowych,
  sieciowych, wejściowych i szeregowych

%package caja
Summary:	Blueman plugin for Caja
Summary(pl.UTF-8):	Wtyczka Bluemana dla zarządcy plików Caja
Group:		X11/Applications
Requires:	%{name} = %{version}
Requires:	caja-python

%description caja
Blueman plugin for Caja.

%description caja -l pl.UTF-8
Wtyczka Bluemana dla zarządcy plików Caja.

%package nautilus
Summary:	Blueman plugin for Nautilus
Summary(pl.UTF-8):	Wtyczka Bluemana dla Nautilusa
Group:		X11/Applications
Requires:	%{name} = %{version}
Requires:	nautilus-python

%description nautilus
Blueman plugin for Nautilus.

%description nautilus -l pl.UTF-8
Wtyczka Bluemana dla Nautilusa.

%package nemo
Summary:	Blueman plugin for Nemo
Summary(pl.UTF-8):	Wtyczka Bluemana dla zarządcy plików Nemo
Group:		X11/Applications
Requires:	%{name} = %{version}
Requires:	cinnamon-nemo-python

%description nemo
Blueman plugin for Nautilus.

%description nemo -l pl.UTF-8
Wtyczka Bluemana dla zarządcy plików Nemo.

%package thunar
Summary:	Blueman plugin for Thunar
Summary(pl.UTF-8):	Wtyczka Bluemana dla Thunara
Group:		X11/Applications
Requires:	%{name} = %{version}

%description thunar
Blueman plugin for Thunar.

%description thunar -l pl.UTF-8
Wtyczka Bluemana dla Thunara.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	CYTHONEXEC=/usr/bin/cython3 \
	NETWORKTOOLS=/sbin/ip \
	--disable-runtime-deps-check \
	--disable-schemas-compile \
	--disable-static \
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
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/_blueman.la

# DO NOT RUN py_postclean - breaks plugins and everything

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
glib-compile-schemas %{_datadir}/glib-2.0/schemas
%service %{name}-mechanism restart
%systemd_post %{name}-mechanism.service
%systemd_user_post blueman-applet.service blueman-manager.service

%preun
if [ "$1" = "0" ]; then
        %service -q %{name}-mechanism stop
fi
%systemd_preun %{name}-mechanism.service
%systemd_user_preun blueman-applet.service blueman-manager.service

%postun
%update_icon_cache hicolor
glib-compile-schemas %{_datadir}/glib-2.0/schemas
%systemd_reload

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.md CHANGELOG.md COPYING FAQ
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xdg/autostart/blueman.desktop
%attr(755,root,root) %{_bindir}/blueman-adapters
%attr(755,root,root) %{_bindir}/blueman-applet
%attr(755,root,root) %{_bindir}/blueman-manager
%attr(755,root,root) %{_bindir}/blueman-sendto
%attr(755,root,root) %{_bindir}/blueman-services
%attr(755,root,root) %{_bindir}/blueman-tray
%{_mandir}/man1/blueman-adapters.1*
%{_mandir}/man1/blueman-applet.1*
%{_mandir}/man1/blueman-manager.1*
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
%{_datadir}/glib-2.0/schemas/org.blueman.gschema.xml
%{systemdunitdir}/blueman-mechanism.service
%{systemduserunitdir}/blueman-applet.service
%{systemduserunitdir}/blueman-manager.service
%{_datadir}/dbus-1/services/org.blueman.Applet.service
%{_datadir}/dbus-1/services/org.blueman.Manager.service
%{_datadir}/dbus-1/system.d/org.blueman.Mechanism.conf
%{_datadir}/polkit-1/actions/org.blueman.policy
%{_datadir}/polkit-1/rules.d/blueman.rules
%attr(755,root,root) %{py3_sitedir}/_blueman.so
%{py3_sitescriptdir}/%{name}

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
