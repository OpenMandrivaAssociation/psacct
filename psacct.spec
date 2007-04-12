%define version	6.3.2
%define release 17mdk

Summary:	Utilities for monitoring process activities
Name:		psacct
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Monitoring
Url:		ftp://ftp.gnu.org/pub/gnu/
Source:		ftp://ftp.gnu.org/pub/gnu/acct/acct-%version.tar.bz2
Source1:	psacct.logrotate
Source2:	psacct.initscript
Patch0:		psacct-log.patch
Patch1:		psacct-6.3.2-info.patch
Patch2:		psacct-6.3.2-biarch-utmp.patch
Buildroot:	%{_tmppath}/%{name}-%{version}-root
Prereq:		/sbin/install-info
Prereq:		/sbin/chkconfig
Prereq:		rpm-helper
BuildRequires:	texinfo
BuildRequires:	autoconf2.1 >= 1:2.13-21mdk
BuildRequires:	automake1.4

%description
The psacct package contains several utilities for monitoring process
activities, including ac, lastcomm, accton and sa.  The ac command
displays statistics about how long users have been logged on.  The
lastcomm command displays information about previous executed commands.
The accton command turns process accounting on or off.  The sa command
summarizes information about previously executed commmands.

Install the psacct package if you'd like to use its utilities for
monitoring process activities on your system.

%prep
%setup -q -n acct-%version
%patch0 -p0 -b .loglocation
%patch1 -p1 -b .infoentry
%patch2 -p1 -b .biarch-utmp

# needed by patch0
# ACLOCAL=aclocal-1.4 AUTOMAKE=automake-1.4 autoreconf --force

%build
%serverbuild
%configure2_5x

perl -p -i -e "s/\/\* #undef HAVE_LINUX_ACCT_H \*\//#define HAVE_LINUX_ACCT_H/" config.h

perl -p -i -e "s@/var/account@/var/log@g" files.h

perl -p -i -e "s/struct acct/struct acct_v3/g" *

#make CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" SHELL="/bin/sh"
#make CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" SHELL="/bin/sh" accounting.info
%make
#make SHELL="/bin/sh" accounting.info

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{sbin,usr,var/log}
%makeinstall

# move accton to /sbin -- leave historical symlink
mv $RPM_BUILD_ROOT%{_sbindir}/accton $RPM_BUILD_ROOT/sbin/accton
ln -s ../../sbin/accton $RPM_BUILD_ROOT%{_sbindir}/accton

# Because of the last command conflicting with the one from SysVinit
mv $RPM_BUILD_ROOT%{_bindir}/last $RPM_BUILD_ROOT%{_bindir}/last-psacct
mv $RPM_BUILD_ROOT%{_mandir}/man1/last.1 $RPM_BUILD_ROOT%{_mandir}/man1/last-psacct.1

touch $RPM_BUILD_ROOT/var/log/pacct $RPM_BUILD_ROOT/var/log/usracct $RPM_BUILD_ROOT/var/log/savacct

install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT/etc/logrotate.d/psacct
install -D -m 755 %{SOURCE2} $RPM_BUILD_ROOT/%{_initrddir}/psacct

%clean
rm -rf $RPM_BUILD_ROOT

%post
# Create initial log files so that logrotate doesn't complain
if [ $1 = 1 ]; then
   %create_ghostfile /var/log/usracct root root 644
   %create_ghostfile /var/log/savacct root root 644
   %create_ghostfile /var/log/pacct root root 644
fi

%_install_info accounting.info
%_post_service %{name}

%preun
%_remove_install_info accounting.info
%_preun_service %{name}


%files
%defattr(-,root,root)
%doc README NEWS INSTALL AUTHORS ChangeLog COPYING
/sbin/*
%{_sbindir}/*
%{_bindir}/*
%{_mandir}/*/*
%{_infodir}/*
%config(noreplace) /etc/logrotate.d/%{name}
%config(noreplace) %{_initrddir}/%{name}
%ghost /var/log/pacct
%ghost /var/log/usracct
%ghost /var/log/savacct

