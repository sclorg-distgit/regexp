%global pkg_name regexp
%{?scl:%scl_package %{pkg_name}}
%{?java_common_find_provides_and_requires}

# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%global full_name       jakarta-%{pkg_name}

Name:           %{?scl_prefix}%{pkg_name}
Version:        1.5
Release:        13.15%{?dist}
Epoch:          0
Summary:        Simple regular expressions API
License:        ASL 2.0
Url:            http://jakarta.apache.org/%{pkg_name}/
Source0:        http://www.apache.org/dist/jakarta/regexp/jakarta-regexp-%{version}.tar.gz
Source1:        http://repo.maven.apache.org/maven2/%{full_name}/%{full_name}/1.4/%{full_name}-1.4.pom
Source2:        %{full_name}-osgi-manifest.MF
Patch0:         %{full_name}-attach-osgi-manifest.patch
BuildRequires:  %{?scl_prefix}javapackages-tools

BuildRequires:  %{?scl_prefix}ant >= 1.6
BuildArch:      noarch

%description
Regexp is a 100% Pure Java Regular Expression package that was
graciously donated to the Apache Software Foundation by Jonathan Locke.
He originally wrote this software back in 1996 and it has stood up quite
well to the test of time.
It includes complete Javadoc documentation as well as a simple Applet
for visual debugging and testing suite for compatibility.

%package javadoc
Summary:        Javadoc for %{pkg_name}

%description javadoc
Javadoc for %{pkg_name}.

%prep
%setup -q -n %{full_name}-%{version}
%patch0
cp -p %{SOURCE2} MANIFEST.MF
%{?scl:scl enable %{scl_maven} %{scl} - <<"EOF"}
set -e -x
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - <<"EOF"}
set -e -x
mkdir lib
ant -Djakarta-site2.dir=. jar javadocs
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - <<"EOF"}
set -e -x
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 build/*.jar %{buildroot}%{_javadir}/%{pkg_name}.jar

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -r docs/api/* %{buildroot}%{_javadocdir}/%{name}

install -d -m 755 %{buildroot}%{_mavenpomdir}
install -p -m 644 %{SOURCE1} %{buildroot}%{_mavenpomdir}/JPP-%{pkg_name}.pom
%add_maven_depmap -a regexp:regexp
%{?scl:EOF}

%check
%{?scl:scl enable %{scl_maven} %{scl} - <<"EOF"}
set -e -x
ant -Djakarta-site2.dir=. test
%{?scl:EOF}

%files -f .mfiles
%doc LICENSE

%files javadoc
%doc LICENSE
%doc %{_javadocdir}/%{name}

%changelog
* Thu Jan 28 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-13.15
- Add OSGi manifest

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 0:1.5-13.14
- Mass rebuild 2015-01-13

* Fri Jan 09 2015 Michal Srb <msrb@redhat.com> - 0:1.5-13.13
- Mass rebuild 2015-01-09

* Wed Jan 07 2015 Michal Srb <msrb@redhat.com> - 1.5-13.12
- Migrate to .mfiles

* Tue Dec 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-13.11
- Migrate requires and build-requires to rh-java-common

* Mon Dec 15 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-13.10
- Mass rebuild 2014-12-15

* Mon Dec 15 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-13.9
- Rebuild for rh-java-common collection

* Mon Jun  2 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-13.8
- Fix dist tag
- Install unversioned javadocs

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-13.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-13.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-13.5
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-13.4
- Remove requires on java

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-13.3
- SCL-ize build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-13.2
- Rebuild to regenerate auto-requires

* Thu Feb 13 2014 Michal Srb <msrb@redhat.com> - 0:1.5-13.1
- SCL-ize %%check section

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-13
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 01.5-13
- Mass rebuild 2013-12-27

* Tue Jul 23 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.5-12
- Enable testsuite

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-11
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 31 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-9
- Install LICENSE file with javadoc package
- Add maven POM file
- Update to current packaging guidelines
- Convert versioned JAR to unversioned

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 6 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.5-5
- Drop gcj support.

* Fri Jan 08 2010 Andrew Overholt <overholt@redhat.com> 1.5-4.3
- Remove javadoc ghost symlinking.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5-4.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5-3.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.5-2.2
- drop repotag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.5-2jpp.1
- Autorebuild for GCC 4.3

* Sat Feb 9 2008 Devrim GUNDUZ <devrim@commandprompt.com> 0:1.5-1jpp.1
- Update to 1.5
- Fix license
- Cosmetic cleanup

* Thu Feb 8 2007 Vivek Lakshmanan <vivekl at redhat.com> 0:1.4-3jpp.1.fc7
- Resync with JPP
- Use the upstream tar ball as JPP does since they clean it off jars anyway
- Use JPackage exception compliant naming scheme
- Remove section definition
- Install unversioned symlink
- Add missing ghost for unversioned link
- Add requires on java

* Fri Aug 4 2006 Vivek Lakshmanan <vivekl@redhat.com> 0:1.4-2jpp.2
- Rebuild.

* Fri Aug 4 2006 Vivek Lakshmanan <vivekl@redhat.com> 0:1.4-2jpp.1
- Merge with latest from JPP.
- Remove prebuilt jars from new source tar ball.

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:1.3-2jpp_9fc
- Rebuilt

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0:1.3-2jpp_8fc
- rebuild

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 0:1.3-2jpp_7fc
- stop scriptlet spew

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0:1.3-2jpp_6fc
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0:1.3-2jpp_5fc
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Dec 21 2005 Jesse Keating <jkeating@redhat.com> 0:1.2-2jpp_4fc
- rebuilt again

* Tue Dec 13 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Jul 15 2005 Gary Benson <gbenson@redhat.com> 0:1.3-2jpp_3fc
- Build on ia64, ppc64, s390 and s390x.
- Switch to aot-compile-rpm.

* Tue Jun 14 2005 Gary Benson <gbenson@redhat.com> 0:1.3-2jpp_2fc
- Remove jarfile from the tarball.

* Thu May 26 2005 Gary Benson <gbenson@redhat.com> 0:1.3-2jpp_1fc
- Upgrade to 1.3-2jpp.
- Rearrange how BC-compiled stuff is built and installed.

* Mon May 23 2005 Gary Benson <gbenson@redhat.com> 0:1.3-1jpp_6fc
- Add alpha to the list of build architectures (#157522).
- Use absolute paths for rebuild-gcj-db.

* Thu May  5 2005 Gary Benson <gbenson@redhat.com> 0:1.3-1jpp_5fc
- BC-compile.

* Tue Jan 11 2005 Gary Benson <gbenson@redhat.com> 0:1.3-1jpp_4fc
- Sync with RHAPS.

* Thu Nov  4 2004 Gary Benson <gbenson@redhat.com> 0:1.3-1jpp_3fc
- Build into Fedora.

* Fri Oct  1 2004 Andrew Overholt <overholt@redhat.com> 0:1.3-1jpp_3rh
- add coreutils BuildRequires

* Wed Aug 25 2004 Fernando Nasser <fnasser@redhat.com> 0:1.3-2jpp
- Require Ant > 1.6
- Rebuild with Ant 1.6.2

* Fri Mar 26 2004 Frank Ch. Eigler <fche@redhat.com> 0:1.3-1jpp_2rh
- add RHUG upgrade cleanup

* Thu Mar  3 2004 Frank Ch. Eigler <fche@redhat.com> 0:1.3-1jpp_1rh
- RH vacuuming

* Thu Oct 09 2003 Henri Gomez <hgomez at users.sourceforge.net> 0:1.3-1jpp
- regexp 1.3

* Fri May 09 2003 David Walluck <david@anti-microsoft.org> 0:1.2-14jpp
- update for JPackage 1.5

* Fri Mar 23 2003 Nicolas Mailhot <Nicolas.Mailhot (at) JPackage.org> 1.2-13jpp
- for jpackage-utils 1.5

* Tue Jul 02 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.2-11jpp
- section marcro
- removed additional symlink

* Mon Jun 24 2002 Henri Gomez <hgomez@slib.fr> 1.2-10jpp
- add official jakarta jarname (jakarta-regexp-1.2.jar) symlink to real
  jarname

* Mon Jun 10 2002 Henri Gomez <hgomez@slib.fr> 1.2-9jpp
- use sed instead of bash 2.x extension in link area to make spec compatible
  with distro using bash 1.1x
- use official tarball

* Fri Jan 18 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.2-8jpp 
- versioned dir for javadoc
- no dependencies javadoc package

* Sat Dec 1 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.2-7jpp
- javadoc in javadoc package
- official summary

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 1.2-5jpp
- removed packager tag
- new jpp extension

* Sun Sep 30 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.2-5jpp
- first unified release
- s/jPackage/JPackage

* Sun Aug 26 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.2-4mdk
- vendor tag
- packager tag
- s/Copyright/License/
- truncated description to 72 columns in spec
- spec cleanup
- used versioned jar
- used new source packaging policy

* Sat Feb 17 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.2-3mdk
- spec cleanup
- changelog correction

* Sun Feb 04 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.2-2mdk
- merged with Henri Gomez <hgomez@slib.fr> specs:
- changed name to regexp
-  changed javadir to /usr/share/java
-  dropped jdk & jre requirement
-  added Jikes support
- changed jar name to regexp.jar
- corrected doc

* Sun Jan 14 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.2-1mdk
- first Mandrake release
