Name:           xenopsd
Version:        0.150.12
Release:        1.2%{?dist}
Summary:        Simple VM manager
License:        LGPL
URL:            https://github.com/xapi-project/xenopsd

Source0: https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xenopsd/archive?at=v0.150.12&format=tar.gz&prefix=xenopsd-0.150.12#/xenopsd-0.150.12.tar.gz
Source1: SOURCES/xenopsd/xenopsd-xc.service
Source2: SOURCES/xenopsd/xenopsd-simulator.service
Source3: SOURCES/xenopsd/xenopsd-sysconfig
Source4: SOURCES/xenopsd/xenopsd-64-conf


Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xenopsd/archive?at=v0.150.12&format=tar.gz&prefix=xenopsd-0.150.12#/xenopsd-0.150.12.tar.gz) = 5a5eae4da005787ead2b0eaf860dfa66f6d4e487


# XCP-ng patches
Patch1000:      xenopsd-0.66.0-use-xcp-clipboardd.XCP-ng.patch

BuildRequires:  xs-opam-repo
BuildRequires:  ocaml-xcp-idl-devel
BuildRequires:  forkexecd-devel
BuildRequires:  xen-devel
BuildRequires:  xen-libs-devel
BuildRequires:  xen-dom0-libs-devel
BuildRequires:  python-devel
BuildRequires:  systemd
Requires:       message-switch
Requires:       xen-dom0-tools
Requires:       python2-scapy

Requires:       jemalloc
%global _use_internal_dependency_generator 0
%global __requires_exclude *caml*
AutoReqProv: no

%{?systemd_requires}

%description
Simple VM manager for the xapi toolstack.

%if 0%{?coverage:1}
%package        cov
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xenopsd/archive?at=v0.150.12&format=tar.gz&prefix=xenopsd-0.150.12#/xenopsd-0.150.12.tar.gz) = 5a5eae4da005787ead2b0eaf860dfa66f6d4e487
Summary: Xenopsd is built with coverage enabled
%description    cov
Xenopsd is built with coverage enabled
%files          cov
%endif

%package        xc
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xenopsd/archive?at=v0.150.12&format=tar.gz&prefix=xenopsd-0.150.12#/xenopsd-0.150.12.tar.gz) = 5a5eae4da005787ead2b0eaf860dfa66f6d4e487
Summary:        Xenopsd using xc
Requires:       %{name} = %{version}-%{release}
%if 0%{?coverage:1}
Requires:       %{name}-cov = %{version}-%{release}
%endif
Requires:       forkexecd
Requires:       xen-libs
Requires:       emu-manager
# NVME support requires newer qemu
# Semantic versioning: describe acceptable range of qemu versions
# if a new major version of qemu/qemu.pg is released and xenopsd is still
# compatible then we just have to update this line and bump the minor for xenopsd
Requires:       qemu >= 2:4.2.1-4.4.0
Conflicts:      qemu >= 2:4.2.1-5.0.0
Obsoletes:      ocaml-xenops-tools

%description    xc
Simple VM manager for Xen using libxc.

%package        simulator
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xenopsd/archive?at=v0.150.12&format=tar.gz&prefix=xenopsd-0.150.12#/xenopsd-0.150.12.tar.gz) = 5a5eae4da005787ead2b0eaf860dfa66f6d4e487
Summary:        Xenopsd simulator
Requires:       %{name} = %{version}-%{release}
%description    simulator
A synthetic VM manager for testing.

%package        devel
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xenopsd/archive?at=v0.150.12&format=tar.gz&prefix=xenopsd-0.150.12#/xenopsd-0.150.12.tar.gz) = 5a5eae4da005787ead2b0eaf860dfa66f6d4e487
Summary:        Xenopsd library

%description    devel
A library containing a simulator for xenopsd, for use in unit tests
of interactions with xenopsd

%package        cli
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xenopsd/archive?at=v0.150.12&format=tar.gz&prefix=xenopsd-0.150.12#/xenopsd-0.150.12.tar.gz) = 5a5eae4da005787ead2b0eaf860dfa66f6d4e487
Summary:        CLI for xenopsd, the xapi toolstack domain manager
Requires:       %{name} = %{version}-%{release}
Obsoletes:      xenops-cli

%description    cli
Command-line interface for xenopsd, the xapi toolstack domain manager.

%global ocaml_dir    %{_opamroot}/ocaml-system
%global ocaml_libdir %{ocaml_dir}/lib
%global ocaml_docdir %{ocaml_dir}/doc

%prep
%autosetup -p1

%build
./configure --libexecdir %{_libexecdir}/%{name} %{?coverage:--enable-coverage}
echo "%{version}-%{release}" > VERSION
make

%check
make test

%install
make install DESTDIR=%{buildroot} QEMU_WRAPPER_DIR=%{_libdir}/xen/bin LIBEXECDIR=%{_libexecdir}/%{name} SBINDIR=%{_sbindir} MANDIR=%{_mandir} BINDIR=%{_bindir}

%{__install} -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/xenopsd-xc.service
%{__install} -D -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/xenopsd-simulator.service
%{__install} -D -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/xenopsd
%{__install} -D -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/xenopsd.conf

%files
%doc README.md LICENSE
%{_sysconfdir}/udev/rules.d/xen-backend.rules
%{_libdir}/xen/bin/qemu-wrapper
%{_libexecdir}/%{name}/vif
%{_libexecdir}/%{name}/vif-real
%{_libexecdir}/%{name}/block
%{_libexecdir}/%{name}/tap
%{_libexecdir}/%{name}/qemu-dm-wrapper
%{_libexecdir}/%{name}/qemu-vif-script
%{_libexecdir}/%{name}/setup-vif-rules
%{_libexecdir}/%{name}/setup-pvs-proxy-rules
%{_libexecdir}/%{name}/common.py
%{_libexecdir}/%{name}/common.pyo
%{_libexecdir}/%{name}/common.pyc
%{_libexecdir}/%{name}/igmp_query_injector.py
%{_libexecdir}/%{name}/igmp_query_injector.pyo
%{_libexecdir}/%{name}/igmp_query_injector.pyc
%config(noreplace) %{_sysconfdir}/sysconfig/xenopsd
%config(noreplace) %{_sysconfdir}/xenopsd.conf

%exclude %{ocaml_dir}

# ---
%files devel
%{ocaml_libdir}/xapi-xenopsd/*
%{ocaml_libdir}/stublibs/dllc_stubs_stubs.so
%{ocaml_docdir}/xapi-xenopsd/*

%files xc
%{_sbindir}/xenopsd-xc
%{_unitdir}/xenopsd-xc.service
%{_mandir}/man1/xenopsd-xc.1.gz
%{_libexecdir}/%{name}/set-domain-uuid
/opt/xensource/libexec/fence.bin
%{_bindir}/list_domains

%files cli
%{_sbindir}/xenops-cli
%{_mandir}/man1/xenops-cli.1.gz

%pre
/usr/bin/getent passwd qemu >/dev/null 2>&1 || /usr/sbin/useradd \
    -M -U -r \
    -s /sbin/nologin \
    -d / \
    qemu >/dev/null 2>&1 || :
/usr/bin/getent passwd qemu_base >/dev/null 2>&1 || /usr/sbin/useradd \
    -M -U -r \
    -s /sbin/nologin \
    -d / \
    -u 65535 \
    qemu_base >/dev/null 2>&1 || :

%post xc
%systemd_post xenopsd-xc.service

%preun xc
%systemd_preun xenopsd-xc.service

%postun xc
%systemd_postun xenopsd-xc.service

%files simulator
%{_sbindir}/xenopsd-simulator
%{_unitdir}/xenopsd-simulator.service
%{_mandir}/man1/xenopsd-simulator.1.gz

%post simulator
%systemd_post xenopsd-simulator.service

%preun simulator
%systemd_preun xenopsd-simulator.service

%postun simulator
%systemd_postun_with_restart xenopsd-simulator.service

%changelog
* Wed Oct 12 2022 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.150.12-1.2
- Rebuild for security update synced from XS82ECU1019$

* Tue Aug 23 2022 Gael Duperrey <gduperrey@vates.fr> - 0.150.12-1.1
- * Tue May 17 2022 Christian Lindig <christian.lindig@citrix.com> - 0.150.12-1
- - Add featureset to xenopsd VM state
- - Add platformdata to persistent metadata
- - CA-363633: Always take the generation-id directly from xapi
- - CA-363700: update xenopsd platformdata if rtc-timeoffset changes
- - Remove CPUID levelling v1 compat code
- - Upgrade featureset in xenopsd when importing VM state
- - Upgrade VM runtime state when xenopsd restarts
- * Fri May 13 2022 Christian Lindig <christian.lindig@citrix.com> - 0.150.11-1
- - CA-366014 UPD-825 pass dm qemu to UEFI qemu, too
- - CA-364138 log when about to stop varstored and varstore-guard
- * Fri May 13 2022 Christian Lindig <christian.lindig@citrix.com> - 0.150.10-1
- - CA-361220: xenopsd: introduce TASK.destroy_on_finish

* Mon Dec 20 2021 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.150.9-1.1
- Sync with CH 8.2.1
- *** Upstream changelog ***
- * Tue Oct 12 2021 Christian Lindig <christian.lindig@citrix.com> - 0.150.9-1
- - Add mtu to VIF frontend xs tree (CA-359472)
- * Mon Sep 27 2021 Pau Ruiz Safont <pau.safont@citrix.com> - 0.150.8-2
- - Bump package after xs-opam update
- * Mon Aug 23 2021 Pau Ruiz Safont <pau.safont@citrix.com> - 0.150.8-1
- - maintenance: opam 2.1.0 compatibility
- - CP-38064: update for rpclib 7 compatibility
- - CP-38064: update usage of epoll to Core 0.14.0
- * Fri Jul 16 2021 Edwin Török <edvin.torok@citrix.com> - 0.150.7-1
- - CP-33898: Fix command line with QEMU 4.1.1
- - CA-341686: Don't let QEMU open device read-only
- - CA-341689: Set read-only to cdroms
- - CA-345834: Fix device id to be the same as QEMU
- - CA-351685: improved fix for XSA-354
- - CA-351685: increase default xenopsd quota
- * Tue Jul 13 2021 Edwin Török <edvin.torok@citrix.com> - 0.150.6-1
- - Maintenance: fix compiler warning about const
- - CP-37034: add featureset manipulation helpers
- - CP-37034: move TSX handling logic out of xenopsd
- - CP-37282: use xenctrl Max policy for Xen 4.7 compat code
- - CP-37282: Update CI to use Yangtze branch

* Mon Sep 27 2021 Pau Ruiz Safont <pau.safont@citrix.com> - 0.150.8-2
- Bump package after xs-opam update

* Wed Sep 01 2021 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.150.5.1-1.1
- Sync with hotfix XS82E031
- *** Upstream changelog ***
- * Fri Jul 16 2021 Ben Anson <ben.anson@citrix.com> - 0.150.5.1-1
- - CA-351685: improved fix for XSA-354
- - CA-351685: increase default xenopsd quota

* Mon Aug 23 2021 Pau Ruiz Safont <pau.safont@citrix.com> - 0.150.8-1
- maintenance: opam 2.1.0 compatibility
- CP-38064: update for rpclib 7 compatibility
- CP-38064: update usage of epoll to Core 0.14.0

* Fri Jul 16 2021 Edwin Török <edvin.torok@citrix.com> - 0.150.7-1
- CP-33898: Fix command line with QEMU 4.1.1
- CA-341686: Don't let QEMU open device read-only
- CA-341689: Set read-only to cdroms
- CA-345834: Fix device id to be the same as QEMU
- CA-351685: improved fix for XSA-354
- CA-351685: increase default xenopsd quota

* Tue Jul 13 2021 Edwin Török <edvin.torok@citrix.com> - 0.150.6-1
- Maintenance: fix compiler warning about const
- CP-37034: add featureset manipulation helpers
- CP-37034: move TSX handling logic out of xenopsd
- CP-37282: use xenctrl Max policy for Xen 4.7 compat code
- CP-37282: Update CI to use Yangtze branch

* Tue May 18 2021 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.150.5-1.1
- Update for XS82E020
- *** Upstream changelog ***
- * Mon Feb 22 2021 Ben Anson <ben.anson@citrix.com> - 0.150.5-1
- - UPD-678 CA-351823 Revert "Avoid sexp_option deprecation warning"
- - UPD-678 CA-351823 unit test for [@sexp.option] fix
- * Wed Feb 17 2021 Ben Anson <ben.anson@citrix.com> - 0.150.4-1
- - CP-28375: Implement soft reset handler for guest kdump support
- - CA-342935: Disengage guest balloon driver and reset PV features on soft reset
- * Thu Feb 11 2021 Ben Anson <ben.anson@citrix.com> - 0.150.3-1
- - CA-341518: send error handshake during migration
- - CA-341518: add tmp ids to vm_migrate_op
- - CA-341518: call VM_check_state on tmp VM on a failed VM_migrate
- - Avoid sexp_option deprecation warning
- - CA-332779: verify power state for start/reboot/resume
- - CA-332779: Fix resume unit test due to power-state checks
- - CA-347560: move metadata import and add/remove functions outside VM module
- - CA-347560: Introduce VM_import_metadata atomic and queue the op when needed
- - CA-347560: Introduce VM.import_metadata_async

* Mon Feb 22 2021 Ben Anson <ben.anson@citrix.com> - 0.150.5-1
- UPD-678 CA-351823 Revert "Avoid sexp_option deprecation warning"
- UPD-678 CA-351823 unit test for [@sexp.option] fix

* Wed Feb 17 2021 Ben Anson <ben.anson@citrix.com> - 0.150.4-1
- CP-28375: Implement soft reset handler for guest kdump support
- CA-342935: Disengage guest balloon driver and reset PV features on soft reset

* Thu Feb 11 2021 Ben Anson <ben.anson@citrix.com> - 0.150.3-1
- CA-341518: send error handshake during migration
- CA-341518: add tmp ids to vm_migrate_op
- CA-341518: call VM_check_state on tmp VM on a failed VM_migrate
- Avoid sexp_option deprecation warning
- CA-332779: verify power state for start/reboot/resume
- CA-332779: Fix resume unit test due to power-state checks
- maintenance: reformat
- CA-347560: move metadata import and add/remove functions outside VM module
- CA-347560: Introduce VM_import_metadata atomic and queue the op when needed
- CA-347560: Introduce VM.import_metadata_async

* Wed Dec 16 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.150.2-1.1
- Security update (XSA 354)
- Rebase on CH 8.2 hotfix XS82E013
- Keep xenopsd-0.66.0-use-xcp-clipboardd.XCP-ng.patch for https://github.com/xcp-ng/xcp/issues/166

* Tue Nov 24 2020 Ben Anson <ben.anson@citrix.com> - 0.150.2-1
-  CA-344431: read important xenstore entries first
-  CA-344431: refactor attr/os/hotfixes exclusion

* Wed Nov 18 2020 Ben Anson <ben.anson@citrix.com> - 0.150.1-1
-  CA-344431: ls_lR: factor out dir concatenation
-  CA-344431: ls_lR: refactor, use fold
-  CA-344431: ls_lR: separate recursion into separate function
-  CA-344431: ls_lR: add quota
-  CA-344431: ls_lR: limit depth
-  CA-344431, CA-348217: exclude attr/os/hotfixes from ls_lR

* Tue May 19 2020 Christian Lindig <christian.lindig@citrix.com> - 0.150.0-1
- maintenance: prepare for ocamlformat
- maintenance: format code with ocamlformat
- maintenance: format comments using ocamlformat

* Mon May 18 2020 Christian Lindig <christian.lindig@citrix.com> - 0.149.0-1
- CP-33793 make QMP monitoring more robust

* Wed Apr 29 2020 Christian Lindig <christian.lindig@citrix.com> - 0.148.0-1
- CA-335964: store the original vm uuid when starting migration
- CA-335964: refactor rename function
- maintenance: use travis validator suggestions

* Mon Apr 27 2020 Christian Lindig <christian.lindig@citrix.com> - 0.147.0-1
- CP-32863: Run hotplug scripts from xenopsd for storage driver domains
- CP-32863: fix hotplug script for storage driver domains
- CP-32863: make removal idempotent
- CP-32863: do not get stuck waiting for state to reach closed when key
	disappears
- CP-32863: Do not wait for hotplug scripts in Dom0 when plugging in
	storage driver domains

* Mon Mar 23 2020 Christian Lindig <christian.lindig@citrix.com> - 0.146.0-1
- CP-33121: replace Opt with Option
- CP-33121: Do not use Stdext directly
- maintenance: whitespace
- maintenace: remove warnings

* Mon Mar 02 2020 Christian Lindig <christian.lindig@citrix.com> - 0.145.0-1
- Use get_cpu_featureset instead of get_featureset

* Mon Feb 17 2020 Christian Lindig <christian.lindig@citrix.com> - 0.144.0-1
- CA-335206 catch exception from Rpcmarshal.unmarshal

* Fri Feb 07 2020 Christian Lindig <christian.lindig@citrix.com> - 0.143.0-1
- REQ-627 CA-334557 dequarantine VGPU PCIs
- maintenance: use stdext whenever possible
- maintenance: remove all usages of Xstringext
- maintenance: remove ocaml warnings
- opam: keep up-to-date with xs-opam

* Tue Jan 28 2020 Christian Lindig <christian.lindig@citrix.com> - 0.142.0-1
- REQ-627 CA-333495 Introduce PCI dequarantine

* Wed Jan 22 2020 Christian Lindig <christian.lindig@citrix.com> - 0.141.0-1
- CA-332811: Manage libxl type record properly

* Mon Jan 06 2020 Christian Lindig <christian.lindig@citrix.com> - 0.140.0-1
- CP-32429: Modernize python2 code (automated)
- CA-328130 use usb speed to determine bus

* Tue Dec 17 2019 Christian Lindig <christian.lindig@citrix.com> - 0.139.0-1
- Use Stdlib.compare instead of Pervasives.compare

* Wed Dec 11 2019 Christian Lindig <christian.lindig@citrix.com> - 0.138.0-1
- import xapi-xenops

* Tue Dec 03 2019 Christian Lindig <christian.lindig@citrix.com> - 0.137.0-1
- Import xenops-cli and xenops into this repository
- CA-325940 deactivate NVidia PCI SRIOV b/f using pass-through

* Fri Nov 29 2019 Christian Lindig <christian.lindig@citrix.com> - 0.136.0-1
- CA-330162 Ensure floppy options are passed to qemu
- maintenance: put Dm media in its own module

* Mon Nov 25 2019 Christian Lindig <christian.lindig@citrix.com> - 0.135.0-1
- CA-328093: Correctly report PV-driver status for UEFI-booted VMs

* Tue Nov 19 2019 Christian Lindig <christian.lindig@citrix.com> - 0.134.0-1
- Fix CI: add definitions from new xenctrl.h
- CA-330830: ignore errors during VM.pause on hard shutdown

* Mon Nov 18 2019 Christian Lindig <christian.lindig@citrix.com> - 0.133.0-1
- CP-32446: New hypercall to get MSR_ARCH_CAPS
- CP-32446: Allow migrated guests to continue using HLE and RTM

* Fri Nov 01 2019 Edvin Török <edvin.torok@citrix.com> - 0.132.0-1
- CP-31431: Add quarantine/dequarantine for PCI devices

* Tue Oct 29 2019 Edvin Török <edvin.torok@citrix.com> - 0.131.0-1
- Backport warning fix from Xen
- CP-32039: add new libxc bindings for NUMA
- CP-32039: print backtraces during tests and build_pre
- CP-32039: plumb has_hard_affinity through
- CP-32039: NUMA placement using CPU soft affinities
- CP-32039: add xenopsd.conf flag to enable NUMA placement
- CP-32039: unit test for NUMA placement
- CP-32039: address review comments

* Mon Oct 14 2019 Christian Lindig <christian.lindig@citrix.com> - 0.130.0-1
- Merge REQ-627 SR-IOV support for NVidia GPUs

* Fri Oct 04 2019 Christian Lindig <christian.lindig@citrix.com> - 0.129.0-1
- CA-327906: don't fail migration if a xenstore directory is missing
- Delete traces of VSS

* Tue Oct 01 2019 Christian Lindig <christian.lindig@citrix.com> - 0.128.0-1
- Merge changes for Xen 4.13

* Thu Sep 26 2019 Igor Druzhinin <igor.druzhinin@citrix.com> - 0.127.0-1
- CA-325848: PVinPVH: set video_mib to 0
- CA-326317: only allow HAP when the host provides it
- Resync flags with Xen 4.13

* Tue Sep 24 2019 Christian Lindig <christian.lindig@citrix.com> - 0.126.0-1
- CA-327280: Revert "Remove workaround for CA-140252"

* Fri Sep 13 2019 Christian Lindig <christian.lindig@citrix.com> - 0.125.0-1
- Remove workaround for CA-140252

* Mon Sep 09 2019 Christian Lindig <christian.lindig@citrix.com> - 0.124.0-1
- Travis CI: Test xapi-xenopsd-xc and xapi-xenopsd-simulator too
- Travis CI: Use common travis env
- CP-32111: Make shim_mem configurable

* Wed Aug 28 2019 Edvin Török <edvin.torok@citrix.com> - 0.123.0-1
- xapi-xenopsd*.opam: fix test dependencies
- Fix dependencies for xapi-xenopsd.opam
- CA-325129 don't pass "-fork true" to emu manager
- CA-325129 don't pass -pci_passthrough to emu-manager
- CA-320079: Add support for NVME namespaces (#653)
- CA-325129 don't pass -fork true to xenguest

* Fri Aug 23 2019 Edwin Török <edvin.torok@citrix.com> - 0.122.0-2
- bump packages after xs-opam update

* Thu Aug 15 2019 Christian Lindig <christian.lindig@citrix.com> - 0.122.0-1
- maintenance: remove bisect_ppx preprocessing

* Mon Aug 12 2019 Christian Lindig <christian.lindig@citrix.com> - 0.121.0-1
- CA-323893: Catch exceptions in Device.PV_Vnc.is_cmdline_valid

* Wed Aug 07 2019 Christian Lindig <christian.lindig@citrix.com> - 0.120.0-1
- CP-31117: Remove implementation of obsolete VM options
- CP-31117: Remove obsolete QEMU stub-domain code
- Remove `qemu_domid` arg from `Device.Dm.pci_assign_guest`

* Fri Aug 02 2019 Christian Lindig <christian.lindig@citrix.com> - 0.119.0-1
- CA-233384: move qemu save/restore to tmpfs in /var/run
- CP-31450: Add domid to Datapath.attach
- Simplify by removing simplify
- atomics_of_operation: switch to style based on List.concat

* Mon Jul 29 2019 Christian Lindig <christian.lindig@citrix.com> - 0.118.0-1
- Move xenstore_watch into xc to make base lib independent of xenstore

* Tue Jul 23 2019 Rob Hoes <rob.hoes@citrix.com> - 0.117.0-1
- CA-322498: Ensure that QEMU receives the max-memory value used for domain build

* Mon Jul 08 2019 Christian Lindig <christian.lindig@citrix.com> - 0.116.0-1
- CA-322749: Make toolstack work with old Nvidia host drivers
- CA-322786 improve ionice handling

* Mon Jul 01 2019 Christian Lindig <christian.lindig@citrix.com> - 0.115.0-1
- CA-322749: Make toolstack work with old Nvidia host drivers
- CA-322655: only replace reboots with shutdown when throttling a VM that crashes too often

* Mon Jul 01 2019 Christian Lindig <christian.lindig@citrix.com> - 0.114.0-1
- Use (||) not "or", avoid warning

* Tue Jun 25 2019 Christian Lindig <christian.lindig@citrix.com> - 0.113.0-1
- CA-321983: Handle vGPU migration from older releases
- CA-320189: miss "-vgpu" argument for multiple vGPUs

* Fri Jun 21 2019 Christian Lindig <christian.lindig@citrix.com> - 0.112.0-1
- CA-315450 pause VM before shutdown
- Simplify Travis setup

* Tue Jun 18 2019 Christian Lindig <christian.lindig@citrix.com> - 0.111.0-1
- CP-31545: Support live migration of VM with multiple vGPUs.
- CA-320361: use device-id if it exists

* Tue Jun 11 2019 Christian Lindig <christian.lindig@citrix.com> - 0.109.0-1
- CA-320215: use xl pci attach for PV guests

* Wed Jun 05 2019 Christian Lindig <christian.lindig@citrix.com> - 0.108.0-1
- CP-31060: Support multiple NVIDIA vGPUs in VM startup. (#617)
- CP-31122: Add uuid into parameters to demu.
- CP-31321: Support extra_args for vGPU configuration
- CA-314693: Live migration failure without any vGPU.
- Support multiple vGPUs in resuming.

* Wed May 29 2019 Christian Lindig <christian.lindig@citrix.com> - 0.107.0-1
- Revert "CA-306943: Revert "CA-297602: Always create a physical-device 
  node for HVM CD-ROMs""
- CP-30037: move start_daemon inside DaemonMgmt
- PV_Vnc: use DaemonMgmt
- CP-30037: drop dead argument ?ready_val from init_daemon
- CP-30037: finished is always true inside wait_path
- CP-30037: simplify wait_path after removing dead code
- CP-30037: factor out forkhelpers.waitpid_nohang
- CP-30037: use systemd to manage varstored
- CP-30136 Allow specifying of pci slot (#620)

* Tue May 28 2019 Christian Lindig <christian.lindig@citrix.com> - 0.106.0-1
- CA-318579 write serial device to xenstore for HVM

* Tue May 14 2019 Christian Lindig <christian.lindig@citrix.com> - 0.105.0-1
- CA-315621 Pass vm_uuid
- CP-31257: Make the tests work again
- CP-31257: test: port to alcotest
- CP-31257: disable 1 unreliable unit test for now

* Tue Apr 16 2019 Christian Lindig <christian.lindig@citrix.com> - 0.104.0-1
- CA-314170: Revert "Don't wait for hotplug-status to disappear for qdisk"
- CA-314170: trigger udev events for qemu-dp (qdisk) disks too
- CA-314170: remove hotplug status when backend is closed on
             clean shutdown (qdisk)
- CA-314170: remove hotplug status immediately on hard shutdown (qdisk)
- CA-314715: Allow backends to generate arguments for hooks
- CA-314715: Allow to pass extra arguments to hooks
- CA-314715: Pass to hooks a consistent domid during migrations
- maintenance: whitespace, consolidate args for vm hooks, i
  remove unused functions

* Tue Apr 09 2019 Christian Lindig <christian.lindig@citrix.com> - 0.103.0-1
- CA-314511: Set "type" key for HVM domains that is expected by xl

* Wed Apr 03 2019 Christian Lindig <christian.lindig@citrix.com> - 0.102.0-1
- CA-314034: Ensure QEMU appends to the logconsole file
- CA-313265: Don't limit QEMU's file size when using file serial

* Fri Mar 29 2019 Christian Lindig <christian.lindig@citrix.com> - 0.101.0-1
- Fix cross-pool migration for qemu-trad VMs
- CA-313709: Introduce a Naples version in the VM state
- CA-313709: Save xen-platform QEMU params in persistent VM state
- CA-313709: Remember the original QEMU profile
- CA-313709: Fix migrations from older versions for VMs without device_id

* Thu Mar 28 2019 Christian Lindig <christian.lindig@citrix.com> - 0.100.0-1
- maintenance: do not apply patch for building

* Mon Feb 25 2019 Christian Lindig <christian.lindig@citrix.com> - 0.99.0-1
- CA-306416: Get 'num_file_descrs' at runtime instead of hardcode.

* Fri Feb 15 2019 Christian Lindig <christian.lindig@citrix.com> - 0.98.0-1
- CA-308199: fix VM migration to Xen 4.9+ on AMD machines

* Tue Feb 12 2019 Christian Lindig <christian.lindig@citrix.com> - 0.97.0-1
- XSI-254 don't create empty /domain/N/device/vif

* Wed Feb 06 2019 Rob Hoes <rob.hoes@citrix.com> - 0.96.0-1
- CP-29962: Stop passing -vgt_monitor_config_file argument to QEMU
- CA-309427: interpret the -serial option rather than looking for hvm_serial

* Tue Feb 05 2019 Christian Lindig <christian.lindig@citrix.com> - 0.95.0-1
- CA-306943: Revert "CA-297602: Always create a physical-device node for HVM CD-ROMs"

* Fri Feb 01 2019 Christian Lindig <christian.lindig@citrix.com> - 0.94.0-1
- CA-309144: use xen platform rev 1 if no device-id specified
- CP-30166: Recognise multi-queue blkback kthreads for QoS setting
- CA-309685 fix fd leak in QMP connection handling

* Tue Jan 29 2019 Christian Lindig <christian.lindig@citrix.com> - 0.93.0-1
- CP-30508: Expose the host's IOMMU presence
- Expose host's support for HVM

* Wed Jan 23 2019 Christian Lindig <christian.lindig@citrix.com> - 0.92.0-1
- Fix DESTDIR handling for Dune 1.6

* Tue Jan 22 2019 Christian Lindig <christian.lindig@citrix.com> - 0.91.0-1
- CA-307829: XSI-216 add active state to VGPU
- CA-272180: report suspend ack failure to xapi
- CA-272180: report suspend timeouts to xapi
- maintenance: whitespace

* Fri Jan 11 2019 Christian Lindig <christian.lindig@citrix.com> - 0.90.0-1
- Use xapi-rrd; rrd is being deprecated.

* Wed Jan 09 2019 Christian Lindig <christian.lindig@citrix.com> - 0.89.0-1
- xenopsd: silence failed-to-read PID messages
- CP-24362: remove qemu-trad profile, treat it as qemu-upstream-compat
- CP-25680 CP-25605: do not attempt to start qemu upstream with qemu-trad args

* Mon Jan 07 2019 Christian Lindig <christian.lindig@citrix.com> - 0.88.0-1
- CA-304519 wait for QMP socket by connecting to it

* Tue Dec 18 2018 Christian Lindig <christian.lindig@citrix.com> - 0.87.0-1
- CP-28301: set `hvmloader/bios` to "ovmf" for UEFI guests
- CP-28659: plumb through NVRAM field
- CP-28662: refactor stop_vgpu
- CP-28662: use varstored for VM start/stop of UEFI guests
- CP-28663: build and fix suspend-image-viewer
- CP-29054: use locked PID files for QEMU
- CP-29058: use string in Io.read/write to contain 
  Bytes.unsafe_to_string to io.ml
- CP-28663: implement VM.suspend/resume for UEFI
- CP-28662: use record instead of string map for NVRAM
- CP-29056, CP-28662: use pidfile for varstored, drop --init and use 
  --nonpersistent
- CA-295520: do not attempt to suspend varstored in Bios mode
- Add OVMF debug print arguments (commented) for convinience
- CA-297602: Always create a physical-device node for HVM CD-ROMs
- CP-29100: Remove PCI Device and expose IO port for communication 
  with varstored.
- CP-29857: Use NVME when platform:device-model=qemu-upstream (#563)
- CA-301610: fix name for Qemu_upstream_uefi device model
- CA-301610: move QMP event thread out of qemu_upstream_compat
- CP-29936: UEFI: block migration when NVME devices are present (#571)
- CP-29967: varstored deprivileging
- CP-29827: drop some trad-compat options (#579)
- CA-302981, CP-30032: Do not try to stop/destroy varstored chroot in 
  BIOS mode, and sandbox varstore-rm (#584)
- CA-305090: do not fail on older versions of qemu

* Tue Dec 04 2018 Christian Lindig <christian.lindig@citrix.com> - 0.86.0-1
- Reference xapi-inventory instead of xcp-inventory; the latter is being deprecated.
- Reference xapi-idl instead of xcp; the latter is being deprecated.

* Fri Nov 30 2018 Christian Lindig <christian.lindig@citrix.com> - 0.85.0-1
- CA-303253: XenMotion breaks VIF connectivity when using DVSC
- CA-303253: Use final-uuid for migration VM as value of xs-vm-uuid in OVS DB

* Tue Nov 27 2018 Christian Lindig <christian.lindig@citrix.com> - 0.84.0-1
- Update jbuild files to use 'preprocess pps'
- Port to Dune
- Revert "CP-28951: Call xapi to send message when receive xen lowmem event"
- Revert "CP-28951: Add a script to send message to xapi"

* Fri Nov 23 2018 Christian Lindig <christian.lindig@citrix.com> - 0.83.0-2
- update exclude rules for builds with Dune
- update VERSION file in source code to reflect version

* Fri Nov 16 2018 Christian Lindig <christian.lindig@citrix.com> - 0.83.0-1
- CA-254835: make Xen 4.8+ featuresets compatible with Xen 4.7
- Switch to new ocaml-rpc

* Fri Nov 09 2018 Christian Lindig <christian.lindig@citrix.com> - 0.82.0-1
- CA-301452: adapt new version scapy igmp changes

* Tue Nov 06 2018 Christian Lindig <christian.lindig@citrix.com> - 0.81.0-1
- CA-298916 don't wait for domain to disappear

* Wed Oct 31 2018 Christian Lindig <christian.lindig@citrix.com> - 0.80.0-1
- Update opam files for Opam 2

* Thu Oct 25 2018 Christian Lindig <christian.lindig@citrix.com> - 0.79.0-1
- CA-297137: Log when finding an undefined domain type
- CA-254698: Drop call to `xl pci-detach` on PCI.unplug

* Mon Oct 22 2018 Christian Lindig <christian.lindig@citrix.com> - 0.78.0-1
- CA-297343: Preserve Xenops_interface errors in migration handshake

* Thu Oct 11 2018 Rob Hoes <rob.hoes@citrix.com> - 0.77.0-1
- CP-28951: Add a script to send message to xapi
- CP-28951: Call xapi to send message when receive xen lowmem event

* Thu Oct 04 2018 Christian Lindig <christian.lindig@citrix.com> - 0.76.0-1
- Clear reservation in case of error in with_reservation

* Mon Oct 01 2018 Christian Lindig <christian.lindig@citrix.com> - 0.75.0-1
- CA-298525 make QMP interaction more robust
- Use new implementations_of_backend helper from xcp-idl

* Wed Sep 26 2018 Christian Lindig <christian.lindig@citrix.com> - 0.74.0-1
- CA-297520: Ensure we can always turn exceptions into at least internal errors
- CA-290696: Block VM migration cancelation just before suspending VM

* Mon Sep 24 2018 Christian Lindig <christian.lindig@citrix.com> - 0.73.0-1
- Revert "CP-28088: Tell xenguest about GVT-g"
- CP-27110: Use PPX storage interface
- CP-27110: Use Opaque SR and VDI types

* Mon Sep 17 2018 Christian Lindig <christian.lindig@citrix.com> - 0.72.0-1
- Remove xapi-xenopsd-xenlight.opam

* Wed Sep 12 2018 Christian Lindig <christian.lindig@citrix.com> - 0.71.0-1
- Update opam files

* Tue Sep 11 2018 Christian Lindig <christian.lindig@citrix.com> - 0.70.0-1
- CA-296924 add "resuming" as a good DEMU state

* Tue Sep 04 2018 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.69.0-2
- Remove xenlight

* Tue Sep 04 2018 Christian Lindig <christian.lindig@citrix.com> - 0.69.0-1
- Remove xenlight backend
- Fixup jbuild files
- Use the PPX IDL rather than Camlp4
- Upgrade old-style RPCs to support RPU/SXM
- jbuild: remove ppx_deriving_rpc from libraries
- lib/jbuild: link only ppx_sexp_conv.runtime-lib

* Tue Aug 21 2018 Christian Lindig <christian.lindig@citrix.com> - 0.68.0-1
- Update to newer interface requirements of Task_server

* Mon Aug 13 2018 Christian Lindig <christian.lindig@citrix.com> - 0.67.0-1
- CA-295092: cancel resume task if process_header raises an exception
- Pass the maximum number of vcpus into Domain.make
- Duplicate Xenctrl.domain_create_flag and use shorter names locally

* Wed Jul 25 2018 Christian Lindig <christian.lindig@citrix.com> - 0.66.0-1
- CA-290688 don't kill emu-manager on cancel, send "abort" cmd

* Wed Jul 18 2018 Christian Lindig <christian.lindig@citrix.com> - 0.65.0-1
- CA-291050: qemu: Don't unshare network namespace when hvm_serial is set

* Wed Jul 11 2018 Christian Lindig <christian.lindig@citrix.com> - 0.64.0-1
- CA-292693: use the corresponding QMP device of a cdrom userdevice
- CA-292693: extend try-except to encompass all QMP code
- CA-293191: Remove non-tail-recursive List.maps when reading xenstore data
- Make dbgring.ml safe-string compliant and build it by default

* Tue Jul 10 2018 Christian Lindig <christian.lindig@citrix.com> - 0.63.0-1
- Build dbgring tool by default

* Wed Jul 04 2018 Christian Lindig <christian.lindig@citrix.com> - 0.62.0-1
- CP-24770: create QEMU disk command line in xenopsd instead of qemu-wrapper
- CP-24770: disregard qemu_disk_cmdline when creating QEMU disk parameters

* Tue Jul 03 2018 Christian Lindig <christian.lindig@citrix.com> - 0.61.0-1
- CA-287333: Report storage backtraces in JSON, not S-expressions

* Thu Jun 28 2018 Christian Lindig <christian.lindig@citrix.com> - 0.60.0-1
- Merge of GFS2 and QEMU upstream features
- CP-28132: Temporary hack to get the xl backend to build until it's removed
- CP-28132: Move to new VDI.attach2 SMAPIv2 call.
- CP-28132: attach now directly returns the xenstore directory
- CP-28132: remove domain_uuid from attach response
- CA-292860: Ensure MTU is set for TAP devices
- CA-287928: Use logger for upstream QEMU logging
- CP-23308 pass "-dm qemu" to emu-manager
- CP-24775 remove with_dirty_log() code and calls
- CA-290644: introduce a version number in the xenopsd persistent_t vm metadata
- CA-290644: vm import_metadata: upgrade profile qemu-trad->qemu-upstream-compat
- CA-290644: name the known versions of the VM persistent metadata used by xenopsd
- CA-292656: Use qemu-upstream-compat if profile is unknown
- CA-292873: Allow "xl destroy" to work with QEMU upstream VMs

* Fri Jun 15 2018 Christian Lindig <christian.lindig@citrix.com> - 0.59.0-1
- CA-289561: Do FLR before de-assigning device.
- CP-28114: Don't have duplicate uuids over a migrate
- CP-28114: Ensure we can still receive migrations from older hosts
- CP-28114: Excise domain_selection now we'll never have the same uuid twice

* Tue May 29 2018 Christian Lindig <christian.lindig@citrix.com> - 0.58.0-1
- lib/xenopsd, xc/device_common: update interface to fd-send-recv >= 2.0.0
- opam: update fd-send-recv bounds
- xc: remove deprecation warnings

* Thu May 24 2018 Christian Lindig <christian.lindig@citrix.com> - 0.57.0-1
- CA-289145: Close socket if error occurs when connecting
- CA-289887: qemu-wrapper: Detect raw disks
- lib: make safe-string compliant
- xc: make safe-string compliant
- xl: make safe-string compliant

* Fri May 18 2018 Christian Lindig <christian.lindig@citrix.com> - 0.56.0-1
- travis-python-nosetests: fix tests

* Thu May 10 2018 Christian Lindig <christian.lindig@citrix.com> - 0.55.0-1
- CA-285401 use Readln module (avoid unread QMP msg)
- CP-26583: Upgrade Xenopsd to use PPX-based IDL of RRDD
- CP-27696: Additionally pass QEMU arguments into the upgrade script
- CP-28088: Tell xenguest about GVT-g

* Tue May 01 2018 Christian Lindig <christian.lindig@citrix.com> - 0.54.0-1
- CA-288350 don't leak fd if QEMU startup too slow
- CA-287881 use "raw" format for Blockdev_change_medium
- CA-288191 VM shutdown failed when resetting VUSB

* Tue Apr 24 2018 Christian Lindig <christian.lindig@citrix.com> - 0.53.0-2
- Remove patch for CA-287881 ("raw" media format for CD change). The
  code is now in the repository.

* Mon Apr 23 2018 Christian Lindig <christian.lindig@citrix.com> - 0.53.0-1
- CA-267368: Remove vcpu_max/shadow_multiplier/memory_static_max
- CA-267368: Remove vcpus from non_persistent
- CA-267368: Remove create_info from non_persistent data
- CA-267368: Move suspend_memory_bytes into persistent data
- CA-267368: Move qemu_vbds into persistent data
- CA-267368: Move qemu_vifs into persistent data
- CA-267368: Move pci_msitranslate/pci_power_mgmt into persistent data
- CA-267368: Remove non_persistent data
- CA-267368: Update notations of VmExtra.t data
- CA-288207: fix finally()

* Fri Apr 20 2018 Christian Lindig <christian.lindig@citrix.com> - 0.52.0-3
- CA-288349: Raise xenopsd file descriptor limit

* Mon Apr 16 2018 Christian Lindig <christian.lindig@citrix.com> - 0.52.0-2
- CA-287881 use "raw" media format for CD change. This depends
  on an updated OCaml QMP library and is applied as a Patch0.

* Wed Apr 04 2018 Christian Lindig <christian.lindig@citrix.com> - 0.52.0-1
- Add qdisk to supported vbd backends
- Add device kind qdisk3
- Add qdisk support to hotplug rules
- Set direct-io-safe=1 to allow direct i/o
- Hack: read 'params' from attach and split it into 'params' and 'qemu-params'
- Don't wait for hotplug-status to disappear for qdisk
- VM suspend/resume: use nbd-client for nbd qemu-datapath
- Device.add_async: use String instead of Xstringext
- Xenops_server_xen.with_disk: use Astring instead of Xstringext
- Xenops_server_xen.with_disk: log when using nbd-client
- Device.add_async: use Astring instead of Xstringext.startswith
- Revert "Set direct-io-safe=1 to allow direct i/o"
- Don't add qemu-params keys unless we're using qemu as datapath
- Make qemu-wrapper work with QEMU datapath

* Tue Apr 03 2018 Christian Lindig <christian.lindig@citrix.com> - 0.51.0-1
- CP-27581: Move MMIO hole size key to a persistent location

* Wed Mar 28 2018 Christian Lindig <christian.lindig@citrix.com> - 0.50.0-1
- Merge QEMU support
- qemu-wrapper: Call unshare() before executing QEMU
- CA-271407: qemu-wrapper: Change arguments for starting GVT-g
- CA-265699: Don't use jemalloc for xs-clipboardd
- CA-265699: Tweak jemalloc config to reduce QEMU memory usage
- CA-282008 refactor qmp interaction for robustness
- CA-285426: Increase qemu save file limit
- CA-285400: Ensure tap devices are not held open
- CA-284857: VM clean shutdown failed when usb is attached to the vm.
- CA-285245 keep better count of NICs
- CA-285245 add address parameter for xen-pvdevice
- CA-285245 add addr=2 option to QEMU for VGA devices
- CA-284857: call usb_reset_detach unconditionally
- CA-286261 calculate address of xen-pvdevice
- CA-286455: Make lower MMIO hole twice as big for the VMs with vGPU

* Thu Mar 22 2018 Marcello Seri <marcello.seri@citrix.com> - 0.49.0-1
- CP-25795: Add new VIF backend for network SR-IOV
- CP-26859: Update guest permission on "*/xenserver/attr" path
- CP-26858: Revert to use Device.Generic.add_device on network SR-IOV
- CP-26858: Add logic to cleanup xenstore paths of net-sriov-vf
- CP-26858: Add device_kind_of function in module VIF
- Adapt sriov idl changes
- CA-285751: Fix VIF.get_state to return Vif.active as reality
- CA-285751: Remove unnecessary open clauses
- ocp-indent xenops_server_xen.ml after rebasing master

* Wed Mar 21 2018 Christian Lindig <christian.lindig@citrix.com> - 0.48.0-1
- CP-27433 remove xenguest-based suspend/restore
- CA-286115 Remove race between DB and xenstore watch thread

* Thu Mar 15 2018 Christian Lindig <christian.lindig@citrix.com> - 0.47.0-1
- CA-284768: Improve thread-safety of TypedTable
- CA-284768: Use DB.update_exn in VM.build
- CA-284768: Use DB.update in store_rtc_timeoffset
- CA-284768: Replace uses of dB_m mutex with DB.update
- CA-284768: Use DB.update in VM.create
- CA-284768: Use DB.update_exn in VM.save
- CA-284768: Use DB.update in set_internal_state
- CA-284768: Use DB.update_exn in VIF.plug
- CA-284768: Use DB.update in VIF.unplug
- CA-284768: Use DB.update_exn in VIF.move
- CA-284768: Use DB.update in maybe_update_pv_drivers_detected

* Fri Mar 09 2018 Christian Lindig <christian.lindig@citrix.com> - 0.46.0-1
- CA-277850 move xenstore_watch to ezxenstore

* Wed Feb 28 2018 Christian Lindig <christian.lindig@citrix.com> - 0.45.0-1
- Rename build_linux -> build_pv
- Remove build_* from mli
- Remove protocol/arch (only used for logging)
- Deduplicate Domain.build functions
- Include PVH mode in Domain.build
- Handle Vm.PVinPVH build mode
- Populate domain_type in Vm.state
- Make pvinpvh_xen path configurable from config file
- Update save and restore functions for PVH mode
- Correctly distinguish between domain types
- Add pvinpvh xen cmdline override to platform flags
- Update Xenctrl.domain_create to take new flags
- Add correct emulation flags during Domain.make
- Default xen-shim cmdline to be "pv-in-pvh" if there's nothing in the config file
- Update default command line for pv-shim
- Use the emulation flags to distinguish between HVM and PVinPVH domains
- Fix shutdown-ack logic to be aware of pvh domains
- CA-277044: Recreate domain_config when it hasn't been persistently stored
- Move memory.ml to xcp-idl
- Use the PVinPVH memory model
- Update PV-in-PVH shim cmdline with memory arg
- Fix mib/kib mixup when setting shim_mem
- For PVinPVH domains only, start the VM with VCPUs=VCPU_max rather than
- Remove fast-resume code from domain.ml
- import_metadata: PVinPVH domains use HVM-style CPU feature sets
- Remove xenclient-related (dead) code
- Use the domain type from the persistent metadata rather than the vm record
- Distinguish between domain types using xenstore key
- Temporary commit to not require sidewinder xenctrl

* Thu Feb 22 2018 Christian Lindig <christian.lindig@citrix.com> - 0.44.0-1
- CA-275746: Build + install fence.bin

* Mon Feb 19 2018 Christian Lindig <christian.lindig@citrix.com> - 0.43.0-1
- Use String.lowercase_ascii over deprecated String.lowercase
- CA-283704: The suspend stream should be opened with O_APPEND

* Mon Jan 08 2018 Christian Lindig <christian.lindig@citrix.com> - 0.42.0-1
- CA-265581: pass pipe_r to emu_manager, as is done in xenguest helper
- CA-270640: Avoid leaking waker threads
- CA-270640: Avoid leaking reader threads
- CA-270640: make sure that flambda will not inline necessary calls
- CA-273775: improve error handling in VM_receive_memory
- CA-273775: remove race in vgpu_receiver_sync during vm migration
- CP-26145: fail vgpu-migration from pre-Jura to Jura and later hosts

* Wed Jan 03 2018 Christian Lindig <christian.lindig@citrix.com> - 0.41.0-1
- xenopsd: add missing dependency

* Mon Dec 18 2017 Christian Lindig <christian.lindig@citrix.com> - 0.40.0-1
- CA-254911: Don't trigger cleanup actions when triggering cleanup actions

* Fri Nov 24 2017 Christian Lindig <christian.lindig@citrix.com> - 0.39.0-1
- Ported the build from oasis to jbuilder.
- scripts/block: fix incorrect variable name

* Tue Nov 21 2017 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 0.38.0-2
- Updated spec file after porting the build from oasis to jbuilder.

* Tue Nov 21 2017 Rob Hoes <rob.hoes@citrix.com> - 0.38.0-1
- CA-269046: Add "console/limit" again

* Wed Nov 01 2017 Rob Hoes <rob.hoes@citrix.com> - 0.37.0-1
- vGPU migration tech preview
- Optionally use emu-manager rather than xenguest for suspend/restore

* Tue Oct 24 2017 Rob Hoes <rob.hoes@citrix.com> - 0.36.0-1
- USB passthrough

* Thu Oct 12 2017 Rob Hoes <rob.hoes@citrix.com> - 0.35.0-1
- Add `qmp` to opam dependencies
- sort opam dependencies
- CP-24774: prepare QMP_Event handler to isolate event handler functions
- CP-24774: use QMP event XEN_PLATFORM_PV_DRIVER_INFO to set HVM Linux feature flags
- CP-24774: replace control/feature flags according to xen upstream design
- CA-267954: prevent too strict association of QMP.event_data type in xenopsd

* Wed Oct 04 2017 Rob Hoes <rob.hoes@citrix.com> - 0.34.0-1
- Support for upstream QEMU

* Fri Sep 22 2017 Rob Hoes <rob.hoes@citrix.com> - 0.33.0-1
- CP-22269: Remove multicast toggle on VIF
- CP-23605: Implement script to inject IGMP query
- CP-23606: Inject IGMP query after VM migration

* Tue Sep 12 2017 Rob Hoes <rob.hoes@citrix.com> - 0.32.0-1
- CA-264331: Make shutdown ack timeout configurable

* Fri Aug 11 2017 Rob Hoes <rob.hoes@citrix.com> - 0.31.0-1
- Add README badges: Build Status and Lines of Code

* Mon Jul 24 2017 Rob Hoes <rob.hoes@citrix.com> - 0.30.0-1
- Use ppx version of memory-interface rpcs
- Revert "Merge pull request #346 from mseri/CA-254991"
- CA-259579: watch balloon-active key to infer ballooning complete

* Wed Jul 12 2017 Rob Hoes <rob.hoes@citrix.com> - 0.29.0-1
- CA-258444: Fix a race when removing files from the filesystem
- qemu-dm-wrapper: Add functionality to read "nic_type" key as a part of

* Mon Jul 03 2017 Rob Hoes <rob.hoes@citrix.com> - 0.28.0-1
- CA-254911: delay shutdown cleanup actions to mitigate a potential stack overflow

* Fri Jun 23 2017 Edwin Török <edvin.torok@citrix.com> - 0.27.0-1
- CP-22451: coverage build for xenopsd controlled by 'coverage' RPM macro

* Fri Jun 16 2017 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.26.0-1
- Remove unnecessary diff-from-xen-api.sh script

* Fri May 12 2017 Rob Hoes <rob.hoes@citrix.com> - 0.25.0-1
- Install the xenopsd library, and move stuff into xcp.updates for easy sharing
- CA-248130 Domain.suspend: eliminate subtree read, write empty list to fd
- add optional xentoollog linker flag and update opam file
- Remove qemu and libvirt backends from xenopsd
- Remove coverage from default build tags
- Merlin: Updates following recent changes
- cancel_utils: optimise xenstore calls in on_shutdown
- add_device: don't write private_list twice
- PCI.ensure_device_frontend_exists: don't overwrite existing frontend keys
- Domain.make: prefer Xst.writev over multiple Xst.write
- CP-21636: Serialise all operations on MxGPU VMs
- configure.ml: More robust way to detect whether xentoollog needs linking

* Fri Mar 24 2017 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.23.0-2
- Add xenopsd-devel package

* Thu Mar 16 2017 Rob Hoes <rob.hoes@citrix.com> - 0.23.0-1
- CP-20431: Handle MxGPU
- CP-21148: Call gimtool when starting the first MxGPU VM on a pGPU

* Mon Mar 13 2017 Marcello Seri <marcello.seri@citrix.com> - 0.22.0-2
- Update OCaml dependencies and build/install script after xs-opam-repo split

* Thu Mar 09 2017 Rob Hoes <rob.hoes@citrix.com> - 0.22.0-1
- CA-245402/PAR-213: Use the right bridge in VIF.move
- Fix VIF.move for tap devices
- CP-20761: PPX
- CP-20761: Remove unused optcomp dependency

* Wed Feb 22 2017 Rob Hoes <rob.hoes@citrix.com> - 0.21.1-1
- Prepare for compiler upgrade

* Fri Feb 17 2017 Frederico Mazzone <frederico.mazzone@citrix.com> - 0.21.0-3
- CA-243676: Do not restart toolstack services on RPM upgrade

* Tue Jan 10 2017 Christian Lindig <christian.lindig@citrix.com> - 0.21.0-2
- remove sub-packages simulator-cov, xenlight-cov for coverage builds
  as they are not fully defined and we will need a general overhaul
  how to build for coverage analysis in the Transformer build system.

* Tue Jan 10 2017 Rob Hoes <rob.hoes@citrix.com> - 0.21.0-1
- Build dbgring by default (but don't install it)
* Mon Dec 19 2016 Rob Hoes <rob.hoes@citrix.com> - 0.20.1-1
- CA-234037: Fix race in CDROM status checking

* Wed Dec 07 2016 Gabor Igloi <gabor.igloi@citrix.com> - 0.20.0-1
- CA-227605: Fix issues with PVS caching under stress tests
- CA-226099: Revert previous fix; ensure that disabled VIFs are not put on a bridge
- vif-real: log with a consistent tag
- CA-227626: Look for VIF in all the pvs-proxy sites
- CA-227101: Increase timeout from 0 to 60 seconds when squeezing domains.
- CP-19645: qemu-dm-wrapper: Allow QEMU to be optionally used when starting a guest
- CA-220466: bootloader: check kernel/ramdisk paths

* Mon Nov 21 2016 Rob Hoes <rob.hoes@citrix.com> - 0.17.0-2
- Install systemd service files with 644 permissions (non-executable)

* Fri Nov 04 2016 Euan Harris <euan.harris@citrix.com> - 0.17.0-1
- CA-226099: setup-vif-rules: drop all traffic on disabled VIFs
- CA-223506: setup-pvs-proxy-rules: handle localhost migration
- CA-225971: Bring up all netback devices, regardless of the locking mode
- CP-18612: Introduce multiple flow tables for pvs vswitch rules
- CA-225067: move qemu-dm to default cgroup slice
- setup-pvs-proxy-rules: announce we are done only at the end
- CA-225257: Fix XSRM typo in setup-pvs-proxy-rules
- CA-203423: fail to parse ionice, error -> warn

* Thu Oct 13 2016 Euan Harris <euan.harris@citrix.com> - 0.16.0-1
- Add PVS support

* Wed Sep 14 2016 Euan Harris <euan.harris@citrix.com> - 0.15.0-1
- Add force option to VM.start
- Add device information in VIF.state

* Fri Sep 02 2016 Euan Harris <euan.harris@citrix.com> - 0.14.0-1
- Update to 0.14.0

* Mon Aug 22 2016 Rafal Mielniczuk <rafal.mielniczuk@citrix.com> - 0.13.0-2
- Package for systemd

* Fri Aug 12 2016 Christian Lindig <christian.lindig@citrix.com> - 0.13.0-1
- Version bump; xenopsd maintains state for nested_virt, nomigrate

* Fri Jul 22 2016 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.12.2-1
- New release

* Thu May 26 2016 Christian Lindig <christian.lindig@citrix.com> - 0.12.1-2
- Fix post xc-cov: have to rm existing symlink just like in upgrade

* Fri May 20 2016 Christian Lindig <christian.lindig@citrix.com> - 0.12.1-1
- New upstream release that supports coverage analysis
- Introduce subpackages *-cov for coverage analysis

* Mon May 16 2016 Si Beaumont <simon.beaumont@citrix.com> - 0.12.0-2
- Re-run chkconfig on upgrade

* Thu Sep 24 2015 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.12.0-1
- New upstream release, and an extra file

* Thu Apr 30 2015 Jon Ludlam <jonathan.ludlam@citrix.com> - UNRELEASED
- Revert some PCI passthrough patches

* Mon Sep 8 2014 David Scott <dave.scott@citrix.com> - 0.9.43-4
- Add a search-path to the xenopsd.conf

* Thu Sep 4 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.9.43-3
- Remove xen-missing-headers dependency

* Thu Sep 4 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.9.43-2
- Reinstate xenlight package in CentOS

* Sun Aug 24 2014 David Scott <dave.scott@citrix.com> - 0.9.43-1
- Update to 0.9.43 which supports OCaml 4.01.0

* Fri Aug 22 2014 David Scott <dave.scott@citrix.com> - 0.9.41-1
- Update to 0.9.41: now pygrub, eliloader, hvmloader and vncterm
  are optional

* Fri Aug 22 2014 David Scott <dave.scott@citrix.com> - 0.9.39-5
- vncterm-wrapper: ensure the groups are added on startup.

* Fri Aug 22 2014 David Scott <dave.scott@citrix.com> - 0.9.39-4
- Add a vncterm-wrapper: needed to locate the qemu keymaps

* Thu Aug 21 2014 David Scott <dave.scott@citrix.com> - 0.9.39-2
- Include {vbd,vif}-xl in the package

* Wed Aug 20 2014 David Scott <dave.scott@citrix.com> - 0.9.39-2
- Package xenopsd-xenlight

* Wed Aug 20 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.9.39-1
- Update to 0.9.39 which compiles without warnings

* Tue Aug 19 2014 David Scott <dave.scott@citrix.com> - 0.9.38-1
- Update to 0.9.38 with better libxl support

* Sat Jun 21 2014 David Scott <dave.scott@citrix.com> - 0.9.37-1
- Depend on the ocaml-xen-lowlevel-libs-runtime package
- Don't include xenguest: this now comes from ocaml-xen-lowlevel-libs

* Fri Jun  6 2014 Jonathan Ludlam <jonathan.ludlam@citrix.com> - 0.9.37-1
- Update to 0.9.37

* Fri Jan 17 2014 Euan Harris <euan.harris@eu.citrix.com> - 0.9.34-1
- Update to 0.9.34, restoring fixes from the 0.9.32 line which were
  not merged to trunk before 0.9.33 was tagged

* Wed Dec 4 2013 Euan Harris <euan.harris@eu.citrix.com> - 0.9.33-1
- Update to 0.9.33, with fixes for suspending and resuming HVM guests

* Mon Oct 28 2013 David Scott <dave.scott@eu.citrix.com> - 0.9.32-1
- Update to 0.9.32, with udev fix (no more "task was asynchronously cancelled")

* Mon Oct 21 2013 David Scott <dave.scott@eu.citrix.com>
- Update to 0.9.31
- move scripts back to libexecdir

* Sun Oct 20 2013 David Scott <dave.scott@eu.citrix.com>
- give up on making libxl work, since it requires xen-4.4
- move scripts from libexecdir to libdir

* Fri Oct 18 2013 David Scott <dave.scott@eu.citrix.com>
- update to 0.9.29

* Fri Oct 18 2013 David Scott <dave.scott@eu.citrix.com>
- update to 0.9.28

* Wed Sep 25 2013 David Scott <dave.scott@eu.citrix.com>
- modprobe blk{tap,back} in the xenopsd-xc init.d script since
  we need these to make virtual disks work
- update to 0.9.27

* Tue Sep 24 2013 David Scott <dave.scott@eu.citrix.com>
- Update to 0.9.26, which includes fixes for networking and libxl

* Fri Sep 20 2013 Euan Harris <euan.harris@citrix.com>
- Generate xenopsd.conf automatically

* Mon Sep 16 2013 Euan Harris <euan.harris@citrix.com>
- Update to 0.9.25, which includes linker paths required on Debian

* Tue Sep 10 2013 David Scott <dave.scott@eu.citrix.com>
- Update to 0.9.24

* Fri Jun 21 2013 David Scott <dave.scott@eu.citrix.com>
- Update to 0.9.5, which includes xenopsd-xenlight

* Thu May 30 2013 David Scott <dave.scott@eu.citrix.com>
- Initial package

