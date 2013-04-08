%define name	psacct
%define version	6.6.1
%define pre	0
%if %pre
%define release 1.pre%pre.15
%else
%define release 1
%endif

Summary:	Utilities for monitoring process activities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Monitoring
Url:		ftp://ftp.gnu.org/pub/gnu/acct
%if %pre
Source:		http://www.physik3.uni-rostock.de/tim/kernel/utils/acct/acct-%{version}-pre%{pre}.tar.bz2
%else
Source:		ftp://ftp.gnu.org/pub/gnu/acct/acct-%version.tar.gz
%endif
Source1:	psacct.logrotate
Source2:	psacct.initscript
Patch1:		acct-6.6.1-texinfo5.1.patch
Requires(post):		rpm-helper
Requires(preun):	rpm-helper
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
%patch1 -p1

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



%changelog
* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 6.4-0.pre1.12mdv2011.0
+ Revision: 667892
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 6.4-0.pre1.11mdv2011.0
+ Revision: 607226
- rebuild

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 6.4-0.pre1.10mdv2010.1
+ Revision: 520203
- rebuilt for 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 6.4-0.pre1.9mdv2010.0
+ Revision: 426784
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 6.4-0.pre1.8mdv2009.1
+ Revision: 351597
- rebuild

* Mon Aug 25 2008 Frederic Crozat <fcrozat@mandriva.com> 6.4-0.pre1.7mdv2009.0
+ Revision: 275850
- Update initscript to be LSB compliant

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 6.4-0.pre1.6mdv2009.0
+ Revision: 225083
- rebuild

* Fri Mar 21 2008 Adam Williamson <awilliamson@mandriva.org> 6.4-0.pre1.6mdv2008.1
+ Revision: 189317
- don't package last at all, even renamed: it fails (#37071), and neither Fedora nor Debian package it, the one in SysVInit is apparently sufficient
- finally fix logrotate issues (#34543), thanks to E. Kunze for the fix

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Oct 09 2007 Guillaume Rousse <guillomovitch@mandriva.org> 6.4-0.pre1.4mdv2008.1
+ Revision: 96269
- remove few settings from logrotate configuration, so as to rely on main logrotate configuration
- fix pre-rotate script (bug #34543)
- cosmetics
- spec cleanup

* Wed Sep 19 2007 Guillaume Rousse <guillomovitch@mandriva.org> 6.4-0.pre1.3mdv2008.0
+ Revision: 90184
- rebuild

* Thu Aug 23 2007 Thierry Vignaud <tv@mandriva.org> 6.4-0.pre1.2mdv2008.0
+ Revision: 69930
- convert prereq

* Fri Jun 08 2007 Adam Williamson <awilliamson@mandriva.org> 6.4-0.pre1.1mdv2008.0
+ Revision: 37123
- drop acct.h and acct_v3 workarounds (no longer needed)
- drop old autotools buildrequires (no longer needed)
- drop patch0, replace with substitution in spec
- clean spec
- new release 6.4pre1


* Thu Dec 01 2005 Warly <warly@mandriva.com> 6.3.2-17mdk
- fix broken lastcomm output (mandriva kernel is using acct V3) (bug 19950)

* Wed Feb 09 2005 Abel Cheung <deaddog@mandrake.org> 6.3.2-16mdk
- Rebuild with fixed auto* call

* Sat May 22 2004 Abel Cheung <deaddog@deaddog.org> 6.3.2-15mdk
- Fix logrotate script to avoid warning if psacct is not running (#1045)
- Modify P1: Add a patch, then add another hack to change that patch !? WTF?
- Fix rpmlint warnings

* Fri May 14 2004 Nicolas Planel <nplanel@mandrakesoft.com> 6.3.2-14mdk
- rebuild for cooker.

* Tue Apr 08 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 6.3.2-13mdk
- Patch2: Handle biarch struct utmp

* Fri Jan 04 2002 Frederic Lepied <flepied@mandrakesoft.com> 6.3.2-12mdk
- corrected log file creation

* Fri Dec 21 2001 Warly <warly@mandrakesoft.com> 6.3.2-11mdk
- include the initscript in package

* Wed Nov 14 2001 Frederic Lepied <flepied@mandrakesoft.com> 6.3.2-10mdk
- put accton on /sbin and keep symbolic link
- start/stop is done in initscripts

* Thu Oct 04 2001 Philippe Libat <philippe@mandrakesoft.com> 6.3.2-9mdk
- fix ghost creation, psacct.init

* Mon Sep 03 2001 Yoann Vandoorselaere <yoann@mandrakesoft.com> 6.3.2-8mdk
- Correct logrotate entry

* Fri Mar 30 2001 Frederic Lepied <flepied@mandrakesoft.com> 6.3.2-7mdk
- use new server macro

* Tue Mar 13 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.3.2-6mdk
- add logrotate entry

* Thu Nov 02 2000 Frederic Lepied <flepied@mandrakesoft.com> 6.3.2-5mdk
- use RPM_OPT_FLAGS.
- force default dir to /var/log instead of /var/account (FHS).
- added an initscript.
- make /var/log/* ghost files.

* Mon Sep 04 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 6.3.2-4mdk
- fix the conflict with SysVinit :
	- Rename the psacct provided 'last' command to 'last-psacct'
	- Rename the psacct provided 'last.1' manpage to 'last-psacct.1'
- Specfile do not specify each binary but directory which contain them

* Tue Aug 29 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 6.3.2-3mdk
- use /usr/share/man & noreplace
- cleanup
- logfile created in %%post, removed in %%preun

* Thu Apr 13 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 6.3.2-2mdk
- Fix bad tag value.
- usr /usr/sbin not /sbin.

* Tue Mar 21 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 6.3.2-1mdk
- Update to 6.3.2
- User 6.3.2 in tag.
- Don't run autoconf, just the configure script.
- Removed a not so usefull sleep 2 :-)
- Removed no more needed patch.

* Mon Nov 29 1999 Florent Villard <warly@mandrakesoft.com>
- built in new environment

* Wed May 05 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions
- handle RPM_OPT_FLAGS

* Mon Apr 05 1999 Preston Brown <pbrown@redhat.com>
- wrap post script with reference count.

* Tue Mar 23 1999 Preston Brown <pbrown@redhat.com>
- install-info sucks.  Still.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 8)

* Thu Mar 18 1999 Bill Nottingham <notting@redhat.com>
- #define HAVE_LINUX_ACCT_H too, so it works. :)

* Sun Aug 16 1998 Jeff Johnson <jbj@redhat.com>
- accton needs to be accessible to /etc/rc.d/init.d/halt

* Fri May 08 1998 Erik Troan <ewt@redhat.com>
- install-info sucks

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- updated from 6.2 to 6.3

* Mon Jul 21 1997 Erik Troan <ewt@redhat.com>
- built against glibc

