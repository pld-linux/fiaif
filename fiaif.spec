%define		rel	1
Summary:	Fiaif is an Intelligent Firewall for iptables based Linux systems.
Summary(pl):	Fiaif to inteligentny firewall bazuj±cy na iptables.
Name:		fiaif
Version:	1.3.0
Release:	0.5
License:	GPL
Group:		Networking/Utilities
Source0:	http://fiaif.fugmann.dhs.org/dist/%{name}_%{version}-%{rel}.tar.gz
URL:		http://fiaif.fugmann.dhs.org/
BuildArch:	noarch
Requires:	iptables, bash >= 2.04, sed, grep, textutils, sh-utils
Prereq:         /sbin/chkconfig
Conflicts:	ipmasq, knetfilter, firewall-easy, shorewall, firewall-init
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Goal of  FIAIF is to provide a  highly customizable script
for setting up an iptables based firewall.

Unlike  many  other scripts,  FIAIF  can  be truly  customized
allowing multiple  interfaces (or  rather zones). There  is no
limit  on  the number  of  zones.  All configuration  is  done
through configuration files. No  need to understand the script
behind it all.

The script makes heavy use  of state-full firewalling, and all
RELATED and ESTABLISHED packets are accepted on all chains. If
you which  to block  something out,  do not  accept it  in the
first place.

The script is written in BASH.  Though this is not the optimal
program to use, it means that you do not need to install extra
interpreters  on your  firewall.  This allows  you  to have  a
minimalistic installation on your firewall.

Install this package if your machine is ever on the internet.

%description -l pl
Celem FIAIF jest  udostêpnienie wysoce dostosowawczego skryptu
zak³adania regu³ ¶ciany ogniowej opartej na netfiltrze.

W   przeciwieñstwie  do   innych  skryptów,   FIAIF  umo¿liwia
ustawianie regu³ na wielu interfejsach, a raczej strefach. Nie
ma limitu stref.

Skrypt  mocno u¿ywa  zabezpieczeñ typu  'state-full', napisany
jest w bashu, co pozwala na zmniejszenie koniecznej instalacji
na ¶cianie ogniowej.

Zainstaluj  ten  pakiet,  gdy  twoja  maszyna  jest  na  sta³e
pod³±czona do internetu.

%prep
%setup -q -n %{name}-%{version}_%{rel}
%build

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT
%{__make} install-config DESTDIR=$RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
install src/fiaif $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/fiaif

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add fiaif 
chkconfig --level 345 fiaif on
if [ -f /var/state/fiaif/iptables ]; then
	/etc/rc.d/init.d/fiaif restart >&2
else
	echo "Configure fiaif and remove the line 'DONT_START=1'"
	echo "from /etc/fiaif/fiaif.conf, then execute"
	echo "'/etc/rc.d/init.d/fiaif start' to start fiaif."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/state/fiaif/iptables ]; then
		/etc/rc.d/init.d/fiaif stop >&2
	fi
	/sbin/chkconfig --del fiaif
fi

%files
%defattr(644,root,root,755)

%dir %attr(0700,root,root) %{_sysconfdir}/fiaif/
%dir /var/state/fiaif/
%config(noreplace) %verify(not size mtime md5) %attr(0600,root,root) %{_sysconfdir}/fiaif/zone.dmz
%config(noreplace) %verify(not size mtime md5) %attr(0600,root,root) %{_sysconfdir}/fiaif/zone.ext
%config(noreplace) %verify(not size mtime md5) %attr(0600,root,root) %{_sysconfdir}/fiaif/zone.int
%config(noreplace) %verify(not size mtime md5) %attr(0600,root,root) %{_sysconfdir}/fiaif/fiaif.conf
%config(noreplace) %verify(not size mtime md5) %attr(0600,root,root) %{_sysconfdir}/fiaif/reserved_networks
%config(noreplace) %verify(not size mtime md5) %attr(0600,root,root) %{_sysconfdir}/fiaif/private_networks
%config(noreplace) %verify(not size mtime md5) %attr(0600,root,root) %{_sysconfdir}/fiaif/type_of_services

%attr(0755,root,root) %{_sysconfdir}/rc.d/init.d/fiaif
%attr(0755,root,root) %{_sbindir}/fiaif-scan

%dir %{_datadir}/fiaif
%{_datadir}/fiaif/traffic-shaping.sh
%{_datadir}/fiaif/functions.sh
%{_datadir}/fiaif/zones.sh
%{_datadir}/fiaif/iptables.sh
%{_datadir}/fiaif/proc-check.sh
%{_datadir}/fiaif/sanity_check.sh
%{_datadir}/fiaif/constants.sh

%{_mandir}/man8/fiaif.8.gz
%{_mandir}/man5/zone.conf.5.gz
%{_mandir}/man5/fiaif.conf.5.gz
%{_mandir}/man8/fiaif-scan.8.gz

%doc todo VERSION doc/faq.txt
