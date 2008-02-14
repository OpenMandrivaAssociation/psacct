%define name	psacct
%define version	6.4
%define pre	1
%if %pre
%define release %mkrel 0.pre%pre.5
%else
%define release %mkrel 1
%endif

Summary:	Utilities for monitoring process activities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Monitoring
Url:		ftp://ftp.gnu.org/pub/gnu/
%if %pre
Source:		http://www.physik3.uni-rostock.de/tim/kernel/utils/acct/acct-%{version}-pre%{pre}.tar.bz2
%else
Source:		ftp://ftp.gnu.org/pub/gnu/acct/acct-%version.tar.bz2
%endif
Source1:	psacct.logrotate
Source2:	psacct.initscript
Patch1:		psacct-6.3.2-info.patch
Patch2:		psacct-6.3.2-biarch-utmp.patch
Buildroot:	%{_tmppath}/%{name}-%{version}-root
Requires(post):		info-install rpm-helper
Requires(preun):		info-install rpm-helper
BuildRequires:	texinfo

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
%if %pre
%setup -q -n acct-%version-pre%pre
%else
%setup -q -n acct-%version
%endif
%patch1 -p1 -b .infoentry
%patch2 -p1 -b .biarch-utmp

%build
%serverbuild

%configure2_5x

perl -p -i -e "s@/var/account@/var/log@g" files.h configure

#make CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" SHELL="/bin/sh"
#make CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" SHELL="/bin/sh" accounting.info
%make
#make SHELL="/bin/sh" accounting.info

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/{sbin,usr,var/log}
%makeinstall

# move accton to /sbin -- leave historical symlink
mv %{buildroot}%{_sbindir}/accton %{buildroot}/sbin/accton
ln -s ../../sbin/accton %{buildroot}%{_sbindir}/accton

# Because of the last command conflicting with the one from SysVinit
mv %{buildroot}%{_bindir}/last %{buildroot}%{_bindir}/last-psacct
mv %{buildroot}%{_mandir}/man1/last.1 %{buildroot}%{_mandir}/man1/last-psacct.1

touch %{buildroot}/var/log/pacct %{buildroot}/var/log/usracct %{buildroot}/var/log/savacct

install -D -m 644 %{SOURCE1} %{buildroot}/etc/logrotate.d/psacct
install -D -m 755 %{SOURCE2} %{buildroot}/%{_initrddir}/psacct

%clean
rm -rf %{buildroot}

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

