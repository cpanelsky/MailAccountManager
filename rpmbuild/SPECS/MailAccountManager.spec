%define _unpackaged_files_terminate_build 0
%define        __spec_install_post %{nil}
%define          debug_package %{nil}
%define        __os_install_post %{_dbpath}/brp-compress
%define _missing_doc_files_terminate_build 0


Summary: A simple plugin to manage mail accounts on a cPanel server
Name: MailAccountManager
Version: 0.01
Release: 0.01
License: cPanel
Group: Development/Tools
SOURCE0 : %{name}-%{version}.tar.gz
URL: https://github.com/cpanelsky/MailAccountManager
AutoReq: no
BuildRoot: %{_tmppath}/%{name}-%{version}


%description
%{summary}

%prep
%setup -q

%build
%install
rm -rf  %{buildroot}
mkdir -p %{buildroot}
 if [ -d "/usr/local/cpanel/whostmgr/docroot/cgi/addons/MailAccountManager" ] ; then
   mv /usr/local/cpanel/whostmgr/docroot/cgi/addons/MailAccountManager /usr/local/cpanel/whostmgr/docroot/cgi/addons/MailAccountManager.$(date +%s)
 fi
rm -rf /usr/local/cpanel/whostmgr/docroot/cgi/addons/mam_install
mkdir -p /usr/local/cpanel/whostmgr/docroot/cgi/addons/mam_install
cp -ia * /usr/local/cpanel/whostmgr/docroot/cgi/addons/mam_install/
%post
cd /usr/local/cpanel/whostmgr/docroot/cgi/addons/mam_install/
/usr/local/cpanel/3rdparty/bin/perl /usr/local/cpanel/whostmgr/docroot/cgi/addons/mam_install/installer


%files

%clean
rm -rf %{buildroot}
%changelog
* Wed Aug 10 2016  Sky Bly <skyler.bly@cpanel.net> 0.01
- Initial Build

