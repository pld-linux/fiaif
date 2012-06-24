Summary:	Fiaif is an Intelligent Firewall for iptables based Linux systems
Summary(pl):	Fiaif - inteligentny firewall bazuj�cy na iptables
Name:		fiaif
Version:	1.19.2
Release:	1
License:	GPL
Group:		Networking/Utilities
Source0:	http://www.fiaif.net/dist/%{name}_%{version}.tar.gz
# Source0-md5:	9042013b1aba5ce20e42c4c235094f82
URL:		http://www.fiaif.net/
BuildRequires:	tetex-dvips
BuildRequires:	tetex-fonts-jknappen
BuildRequires:	tetex-format-latex
BuildRequires:	tetex-latex-ams
BuildRequires:	tetex-latex-bibtex
BuildRequires:	tetex-latex-psnfss
BuildRequires:	tetex-makeindex
BuildRequires:	tetex-metafont
Requires(post,preun):	/sbin/chkconfig
Requires:	bash >= 2.04
Requires:	grep
Requires:	iptables >= 1.2.7a
Requires:	sh-utils
Requires:	textutils
Conflicts:	ipmasq, knetfilter, firewall-easy, shorewall, firewall-init
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Goal of FIAIF is to provide a highly customizable script for
setting up an iptables based firewall.

Unlike many other scripts, FIAIF can be truly customized allowing
multiple interfaces (or rather zones). There is no limit on the number
of zones. All configuration is done through configuration files. No
need to understand the script behind it all.

The script makes heavy use of stateful firewalling, and all RELATED
and ESTABLISHED packets are accepted on all chains. If you wish to
block something out, do not accept it in the first place.

The script is written in BASH. Though this is not the optimal program
to use, it means that you do not need to install extra interpreters on
your firewall. This allows you to have a minimalistic installation on
your firewall.

%description -l pl
Celem FIAIF jest udost�pnienie wysoce dostosowawczego skryptu
ustawiania regu� �ciany ogniowej opartej na netfiltrze.

W przeciwie�stwie do innych skrypt�w, FIAIF umo�liwia ustawianie regu�
na wielu interfejsach, a raczej strefach. Nie ma limitu stref. Ca��
konfiguracj� przeprowadza si� za pomoc� plik�w konfiguracyjnych. Nie
ma potrzeby rozumienia stoj�cego za nimi skryptu.

Skrypt mocno u�ywa zabezpiecze� typu stateful, przepuszczaj�c
wszystkie pakiety RELATED i ESTABLISHED na wszystkich �a�cuchach.
�eby co� zablokowa�, wystarczy nie akceptowa� tego na pocz�tku.

Skrypt napisany jest w bashu, co pozwala na zmniejszenie koniecznej
instalacji na �cianie ogniowej.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
%{__make} install-config \
	DESTDIR=$RPM_BUILD_ROOT

install prog/fiaif $RPM_BUILD_ROOT/etc/rc.d/init.d/fiaif

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add fiaif
if [ -f /var/lib/fiaif/iptables ]; then
	/etc/rc.d/init.d/fiaif force-reload >&2
else
	echo "Configure fiaif and remove the line 'DONT_START=1'"
	echo "from /etc/fiaif/fiaif.conf, then execute"
	echo "'/etc/rc.d/init.d/fiaif start' to start fiaif."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lib/fiaif/iptables ]; then
		/etc/rc.d/init.d/fiaif stop >&2
	fi
	/sbin/chkconfig --del fiaif
fi

%files
%defattr(644,root,root,755)
%doc doc/faq.txt doc/DHCP.txt doc/reporting_bugs.txt doc/upgrade.txt

%dir %attr(700,root,root) %{_sysconfdir}/fiaif
%dir %attr(700,root,root) /var/lib/fiaif
%attr(600,root,root) %{_sysconfdir}/cron.daily/fiaif
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fiaif/zone.dmz
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fiaif/zone.ext
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fiaif/zone.int
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fiaif/fiaif.conf
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fiaif/reserved_networks
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fiaif/private_networks
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fiaif/type_of_services
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fiaif/aliases

%attr(754,root,root) /etc/rc.d/init.d/fiaif
%attr(755,root,root) %{_sbindir}/fiaif-scan
%attr(755,root,root) %{_sbindir}/fiaif-getdev
%attr(755,root,root) %{_sbindir}/fiaif-update

%dir %{_datadir}/fiaif
%{_datadir}/fiaif/traffic-shaping.sh
%{_datadir}/fiaif/functions.sh
%{_datadir}/fiaif/zones.sh
%{_datadir}/fiaif/iptables.sh
%{_datadir}/fiaif/proc-check.sh
%{_datadir}/fiaif/sanity_check.sh
%{_datadir}/fiaif/constants.sh
%{_datadir}/fiaif/cleanup_rules.sh
%{_datadir}/fiaif/aliases.sh
%{_datadir}/fiaif/cleanup_rules.awk
%{_datadir}/fiaif/fiaif_rules.awk
%{_datadir}/fiaif/syntax.awk
%{_datadir}/fiaif/zone_rules.awk
%{_datadir}/fiaif/VERSION

%{_mandir}/man8/fiaif.8*
%{_mandir}/man5/zone.conf.5*
%{_mandir}/man5/fiaif.conf.5*
%{_mandir}/man8/fiaif-scan.8*
%{_mandir}/man8/fiaif-getdev.8*
%{_mandir}/man8/fiaif-update.8*
