Summary:	Command shell for managing Linux LIO kernel target
Name:		targetcli-fb
Version:	2.1.fb33
Release:	1
License:	Apache v2.0
Group:		Applications/System
URL:		https://github.com/agrover/targetcli-fb
Source0:	https://codeload.github.com/agrover/targetcli-fb/tar.gz/v%{version}
# Source0-md5:	758f89dbc40ba54e7f9f901677031fa0
Requires:	python-configshell-fb
Requires:	python-rtslib-fb
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
targetcli-fb is a command-line interface for configuring the LIO
generic SCSI target, present in 3.x Linux kernel versions.

%prep
%setup -q

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mandir}/man8,/etc/target/backup}

%{__python} setup.py \
	install --skip-build \
	--root=$RPM_BUILD_ROOT \
	--optimize=2

%py_postclean

install targetcli.8 $RPM_BUILD_ROOT%{_mandir}/man8/

# empty JSON file
echo "{}" > $RPM_BUILD_ROOT/etc/target/saveconfig.json

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md THANKS
%attr(755,root,root) %{_bindir}/targetcli
%dir %{py_sitescriptdir}/targetcli
%{py_sitescriptdir}/targetcli/*.py[co]
%{py_sitescriptdir}/targetcli_fb-*.egg-info
%{_mandir}/man8/targetcli.8*
%attr(750,root,root) %dir /etc/target
%attr(750,root,root) %dir /etc/target/backup
%attr(640,root,root) /etc/target/saveconfig.json
