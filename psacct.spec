Summary:	Utilities for monitoring process activities
Name:		psacct
Version:	6.6.1
Release:	8
License:	GPLv2
Group:		Monitoring
Url:		ftp://ftp.gnu.org/pub/gnu/acct
Source0:	ftp://ftp.gnu.org/pub/gnu/acct/acct-%{version}.tar.gz
Source1:	psacct.logrotate
Source2:	psacct.initscript
Patch1:		acct-6.6.1-texinfo5.1.patch
BuildRequires:	texinfo
Requires(post,preun):	rpm-helper

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
%setup -qn acct-%{version}
%apply_patches

%build
%serverbuild
%configure2_5x

perl -p -i -e "s@/var/account@/var/log@g" files.h configure

#make CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" SHELL="/bin/sh"
#make CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" SHELL="/bin/sh" accounting.info
%make
#make SHELL="/bin/sh" accounting.info

%install
mkdir -p %{buildroot}/{sbin,usr,var/log}
%makeinstall

# move accton to /sbin -- leave historical symlink
mv %{buildroot}%{_sbindir}/accton %{buildroot}/sbin/accton
ln -s ../../sbin/accton %{buildroot}%{_sbindir}/accton

# Because of the last command conflicting with the one from SysVinit
# We used to rename it, just delete it instead - it doesn't work any
# more, and this is what Debian and Fedora do - AdamW 2008/03
rm -f %{buildroot}%{_bindir}/last
rm -f %{buildroot}%{_mandir}/man1/last.1

touch %{buildroot}/var/log/pacct %{buildroot}/var/log/usracct %{buildroot}/var/log/savacct

install -D -m 644 %{SOURCE1} %{buildroot}/etc/logrotate.d/psacct
install -D -m 755 %{SOURCE2} %{buildroot}/%{_initrddir}/psacct

%post
# Create initial log files so that logrotate doesn't complain
if [ $1 = 1 ]; then
   %create_ghostfile /var/log/usracct root root 644
   %create_ghostfile /var/log/savacct root root 644
   %create_ghostfile /var/log/pacct root root 644
fi

%_post_service %{name}

%preun
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

