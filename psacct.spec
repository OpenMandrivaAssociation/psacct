%define name	psacct
%define version	6.5.5
%define release 1

Summary:	Utilities for monitoring process activities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv3+
Group:		Monitoring
Url:		http://www.gnu.org/software/acct/
Source:		ftp://ftp.gnu.org/pub/gnu/acct/acct-%version.tar.gz
Source1:	psacct.logrotate
Source2:	psacct.initscript

Requires(post):		info-install rpm-helper
Requires(preun):	info-install rpm-helper
BuildRequires:	texinfo

%description
The psacct package contains several utilities for monitoring process
activities, including ac, lastcomm, accton and sa.  The ac command
displays statistics about how long users have been logged on.  The
lastcomm command displays information about previous executed commands.
The accton command turns process accounting on or off.  The sa command
summarizes information about previously executed commands.

Install the psacct package if you'd like to use its utilities for
monitoring process activities on your system.


%prep
%setup -q -n acct-%version

%build
%serverbuild

%configure2_5x

perl -p -i -e "s@/var/account@/var/log@g" files.h configure

%make

%install
mkdir -p %{buildroot}%{_logdir}
%makeinstall

# Because of the last command conflicting with the one from SysVinit
# We used to rename it, just delete it instead - it doesn't work any
# more, and this is what Debian and Fedora do - AdamW 2008/03
rm -f %{buildroot}%{_bindir}/last
rm -f %{buildroot}%{_mandir}/man1/last.1

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
%doc README NEWS INSTALL AUTHORS ChangeLog
%{_sbindir}/*
%{_bindir}/*
%{_mandir}/*/*
%{_infodir}/*
%config(noreplace) /etc/logrotate.d/%{name}
%config(noreplace) %{_initrddir}/%{name}
%ghost /var/log/pacct
%ghost /var/log/usracct
%ghost /var/log/savacct

