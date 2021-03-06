Name:       xkeyboard-config-geminipda

Summary:    Alternative xkb data files
Version:    2.10.1
Release:    2
Group:      System/X11
License:    MIT
BuildArch:  noarch
URL:        http://www.freedesktop.org/wiki/Software/XKeyboardConfig#Releases
Source0:    http://xorg.freedesktop.org/archive/individual/data/%{name}-%{version}.tar.bz2
BuildRequires:  perl(XML::Parser)
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  fdupes
Provides:   xkbdata xkeyboard-config
Obsoletes:   xorg-x11-xkbdata xkeyboard-config

%description
Alternative xkb data files.

%package devel
Summary:    Devel package for alternative xkb data files
Group:      System/X11
Requires:   %{name} = %{version}-%{release}

%description devel
Development files for %{name}.


%prep
%setup -q -n %{name}-%{version}/%{name}

%build

%autogen --disable-static \
    --enable-compat-rules \
    --with-xkb-base=%{_datadir}/X11/xkb \
    --disable-xkbcomp-symlink \
    --with-xkb-rules-symlink=xorg \
    --disable-runtime-deps

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

# Remove unnecessary symlink
rm -f $RPM_BUILD_ROOT%{_datadir}/X11/xkb/compiled

# Bernie: remove locale stuff
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale

# Create filelist
{
FILESLIST=${PWD}/files.list
pushd $RPM_BUILD_ROOT
find ./usr/share/X11 -type d | sed -e "s/^\./%dir /g" > $FILESLIST
find ./usr/share/X11 -type f | sed -e "s/^\.//g" >> $FILESLIST
popd
}

%fdupes  %{buildroot}//usr/share/X11

%files -f files.list
%defattr(-,root,root,-)
%{_datadir}/X11/xkb/rules/xorg
%{_datadir}/X11/xkb/rules/xorg.lst
%{_datadir}/X11/xkb/rules/xorg.xml

%files devel
%defattr(-,root,root,-)
%{_datadir}/pkgconfig/xkeyboard-config.pc
