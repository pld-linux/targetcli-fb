Summary:	Command shell for managing Linux LIO kernel target
Name:		targetcli-fb
Version:	2.1.fb49
Release:	1
License:	Apache v2.0
Group:		Applications/System
URL:		https://github.com/agrover/targetcli-fb
Source0:	https://codeload.github.com/agrover/targetcli-fb/tar.gz/v%{version}
# Source0-md5:	416eeda8f7ddeb7f00fe98dc1a6245b3
Source1:	targetcli.service
Source2:	targetcli.init
BuildRequires:	rpmbuild(macros) >= 1.647
Requires:	python-configshell-fb
Requires:	python-rtslib-fb
Requires(post,preun,postun):	systemd-units >= 38
Requires:	systemd-units >= 208-8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
targetcli-fb is a command-line interface for configuring the LIO
generic SCSI target, present in 3.x Linux kernel versions.

%prep
%setup -q

%build
%py_build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mandir}/man8,/etc/target/backup} \
	$RPM_BUILD_ROOT{%{systemdunitdir},/etc/rc.d/init.d}

%py_install
%py_postclean

install targetcli.8 $RPM_BUILD_ROOT%{_mandir}/man8/

install %{SOURCE1} $RPM_BUILD_ROOT%{systemdunitdir}/targetcli.service
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/targetcli

# empty JSON file
echo "{}" > $RPM_BUILD_ROOT/etc/target/saveconfig.json

%post
/sbin/chkconfig --add targetcli
%service targetcli restart
%systemd_post .service

%preun
if [ "$1" = "0" ]; then
	%service -q targetcli stop
	/sbin/chkconfig --del targetcli
fi
%systemd_preun targetcli.service

%postun
%systemd_reload

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
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,root) /etc/target/saveconfig.json
%attr(754,root,root) /etc/rc.d/init.d/targetcli
%{systemdunitdir}/targetcli.service
