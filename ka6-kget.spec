#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.04.3
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		kget
Summary:	kget
Name:		ka6-%{kaname}
Version:	25.04.3
Release:	2
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	af2eab932ffccfb8dced68561d1a60f6
URL:		http://www.kde.org/
Patch0:		GPGME-2.0.patch
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel
BuildRequires:	Qt6Gui-devel
BuildRequires:	Qt6Network-devel
BuildRequires:	Qt6PrintSupport-devel
BuildRequires:	Qt6Sql-devel
BuildRequires:	Qt6Test-devel
BuildRequires:	Qt6Widgets-devel
BuildRequires:	Qt6Xml-devel
BuildRequires:	boost-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	gpgmepp-devel >= 1.7.0
BuildRequires:	ka6-dolphin-devel >= %{kdeappsver}
BuildRequires:	ka6-libktorrent-devel >= %{kdeappsver}
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-karchive-devel >= %{kframever}
BuildRequires:	kf6-kcmutils-devel >= %{kframever}
BuildRequires:	kf6-kcompletion-devel >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kconfigwidgets-devel >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf6-kdoctools-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kiconthemes-devel >= %{kframever}
BuildRequires:	kf6-kio-devel >= %{kframever}
BuildRequires:	kf6-kitemviews-devel >= %{kframever}
BuildRequires:	kf6-knotifications-devel >= %{kframever}
BuildRequires:	kf6-knotifyconfig-devel >= %{kframever}
BuildRequires:	kf6-kparts-devel >= %{kframever}
BuildRequires:	kf6-kservice-devel >= %{kframever}
BuildRequires:	kf6-ktextwidgets-devel >= %{kframever}
BuildRequires:	kf6-kwallet-devel >= %{kframever}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	kf6-kwindowsystem-devel >= %{kframever}
BuildRequires:	kf6-kxmlgui-devel >= %{kframever}
BuildRequires:	kf6-solid-devel >= %{kframever}
BuildRequires:	libmms-devel
BuildRequires:	ninja
BuildRequires:	qca-qt6-devel >= 2.1.0
BuildRequires:	qgpgme-qt6-devel
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-data = %{version}-%{release}
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KGet is a versatile and user-friendly download manager.. Features.
Downloading files from FTP and HTTP(S) sources. Pausing and resuming
of downloading files, as well as the ability to restart a download.

%description -l pl.UTF-8
KGet jest wszechstronnym i łatwym w użyciu menadżerem pobierania.
Cechy: pobiera plików przez FTP i HTTP(S). Wstrzymywanie i wznawianie
pobierania plików, a także możliwość zrestartowania downloadu.

%package data
Summary:	Data files for %{kaname}
Summary(pl.UTF-8):	Dane dla %{kaname}
Group:		X11/Applications
Requires(post,postun):	desktop-file-utils
Obsoletes:	ka5-%{kaname}-data < %{version}
BuildArch:	noarch

%description data
Data files for %{kaname}.

%description data -l pl.UTF-8
Dane dla %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}
%patch -P0 -p1

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

rm -rf $RPM_BUILD_ROOT%{_kdedocdir}/sr
%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post data
%update_desktop_database_post

%postun data
%update_desktop_database_postun

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kget
%{_libdir}/libkgetcore.so
%ghost %{_libdir}/libkgetcore.so.6
%attr(755,root,root) %{_libdir}/libkgetcore.so.*.*
%dir %{_libdir}/qt6/plugins/kget
%attr(755,root,root) %{_libdir}/qt6/plugins/kget/kget_bittorrent.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kget/kget_checksumsearchfactory.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kget/kget_kio.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kget/kget_metalinkfactory.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kget/kget_mirrorsearchfactory.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kget/kget_mmsfactory.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kget/kget_multisegkiofactory.so
%dir %{_libdir}/qt6/plugins/kget_kcms
%attr(755,root,root) %{_libdir}/qt6/plugins/kget_kcms/kcm_kget_bittorrentfactory.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kget_kcms/kcm_kget_checksumsearchfactory.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kget_kcms/kcm_kget_metalinkfactory.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kget_kcms/kcm_kget_mirrorsearchfactory.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kget_kcms/kcm_kget_mmsfactory.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kget_kcms/kcm_kget_multisegkiofactory.so

%files data -f %{kaname}.lang
%defattr(644,root,root,755)
%{_desktopdir}/org.kde.kget.desktop
%{_datadir}/config.kcfg/kget.kcfg
%{_datadir}/config.kcfg/kget_checksumsearchfactory.kcfg
%{_datadir}/config.kcfg/kget_mirrorsearchfactory.kcfg
%{_datadir}/config.kcfg/kget_mmsfactory.kcfg
%{_datadir}/config.kcfg/kget_multisegkiofactory.kcfg
%{_datadir}/dbus-1/services/org.kde.kget.service
%{_datadir}/kget
%{_datadir}/knotifications6/kget.notifyrc
%{_datadir}/metainfo/org.kde.kget.appdata.xml
%{_datadir}/qlogging-categories6/kget.categories
%{_datadir}/kio/servicemenus/kget_download.desktop
%{_iconsdir}/hicolor/scalable/apps/org.kde.kget.svg
