Name:           xenopsd
Version:        0.66.0
Release:        2.1%{?dist}
Summary:        Simple VM manager
License:        LGPL
URL:            https://github.com/xapi-project/xenopsd

Source0: https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xenopsd/archive?at=v0.66.0&format=tar.gz&prefix=xenopsd-0.66.0#/xenopsd-0.66.0.tar.gz
Source1: SOURCES/xenopsd/xenopsd-xc.service
Source2: SOURCES/xenopsd/xenopsd-xenlight.service
Source3: SOURCES/xenopsd/xenopsd-simulator.service
Source4: SOURCES/xenopsd/xenopsd-sysconfig
Source5: SOURCES/xenopsd/xenopsd-64-conf
Patch0: SOURCES/xenopsd/0001-CP-31431-Add-quarantine-dequarantine-for-PCI-devices.patch


Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xenopsd/archive?at=v0.66.0&format=tar.gz&prefix=xenopsd-0.66.0#/xenopsd-0.66.0.tar.gz) = 949825f219c28b5008ad0e87f4351d8c2d2ae8bd

# XCP-ng Patches
Patch1000: xenopsd-0.66.0-CA-327906-migration-when-xenstore-dir-missing.backport.patch

BuildRequires:  xs-opam-repo
BuildRequires:  ocaml-xcp-idl-devel
BuildRequires:  forkexecd-devel
BuildRequires:  xen-devel
BuildRequires:  xen-libs-devel
BuildRequires:  xen-dom0-libs-devel
BuildRequires:  python-devel
BuildRequires:  systemd
Requires:       message-switch
Requires:       qemu
Requires:       xenops-cli
Requires:       xen-dom0-tools
Requires:       scapy

%global _use_internal_dependency_generator 0
%global __requires_exclude *caml*
AutoReqProv: no


%{?systemd_requires}

%description
Simple VM manager for the xapi toolstack.

%if 0%{?coverage:1}
%package        cov
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xenopsd/archive?at=v0.66.0&format=tar.gz&prefix=xenopsd-0.66.0#/xenopsd-0.66.0.tar.gz) = 949825f219c28b5008ad0e87f4351d8c2d2ae8bd
Summary: Xenopsd is built with coverage enabled
%description    cov
Xenopsd is built with coverage enabled
%files          cov
%endif

%package        xc
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xenopsd/archive?at=v0.66.0&format=tar.gz&prefix=xenopsd-0.66.0#/xenopsd-0.66.0.tar.gz) = 949825f219c28b5008ad0e87f4351d8c2d2ae8bd
Summary:        Xenopsd using xc
Requires:       %{name} = %{version}-%{release}
%if 0%{?coverage:1}
Requires:       %{name}-cov = %{version}-%{release}
%endif
Requires:       forkexecd
Requires:       xen-libs
Requires:       emu-manager
%description    xc
Simple VM manager for Xen using libxc.

%package        simulator
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xenopsd/archive?at=v0.66.0&format=tar.gz&prefix=xenopsd-0.66.0#/xenopsd-0.66.0.tar.gz) = 949825f219c28b5008ad0e87f4351d8c2d2ae8bd
Summary:        Xenopsd simulator
Requires:       %{name} = %{version}-%{release}
%description    simulator
A synthetic VM manager for testing.


%package        xenlight
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xenopsd/archive?at=v0.66.0&format=tar.gz&prefix=xenopsd-0.66.0#/xenopsd-0.66.0.tar.gz) = 949825f219c28b5008ad0e87f4351d8c2d2ae8bd
Summary:        Xenopsd using libxenlight
Requires:       %{name} = %{version}-%{release}

%description    xenlight
Simple VM manager for Xen using libxenlight

%package        devel
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xenopsd/archive?at=v0.66.0&format=tar.gz&prefix=xenopsd-0.66.0#/xenopsd-0.66.0.tar.gz) = 949825f219c28b5008ad0e87f4351d8c2d2ae8bd
Summary:        Xenopsd library

%description    devel
A library containing a simulator for xenopsd, for use in unit tests
of interactions with xenopsd

%global ocaml_dir    /usr/lib/opamroot/system
%global ocaml_libdir %{ocaml_dir}/lib
%global ocaml_docdir %{ocaml_dir}/doc

%prep
%autosetup -p1

%build
eval $(opam config env --root=/usr/lib/opamroot)
./configure --libexecdir %{_libexecdir}/%{name} %{?coverage:--enable-coverage}
make

%install
eval $(opam config env --root=/usr/lib/opamroot)
export OCAMLFIND_DESTDIR=%{buildroot}%{ocaml_libdir}
export OCAMLFIND_LDCONF=ignore
mkdir -p $OCAMLFIND_DESTDIR
make install DESTDIR=%{buildroot} QEMU_WRAPPER_DIR=%{_libdir}/xen/bin LIBEXECDIR=%{_libexecdir}/%{name} SBINDIR=%{_sbindir} MANDIR=%{_mandir}

# should really be in Makefile
gzip %{buildroot}%{_mandir}/man1/*.1

%{__install} -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/xenopsd-xc.service
%{__install} -D -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/xenopsd-xenlight.service
%{__install} -D -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}/xenopsd-simulator.service
%{__install} -D -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/xenopsd
%{__install} -D -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/xenopsd.conf

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

%files xenlight
%{_sbindir}/xenopsd-xenlight
%{_unitdir}/xenopsd-xenlight.service
%{_mandir}/man1/xenopsd-xenlight.1.gz

%post xenlight
%systemd_post xenopsd-xenlight.service

%preun xenlight
%systemd_preun xenopsd-xenlight.service

%postun xenlight
%systemd_postun_with_restart xenopsd-xenlight.service

%changelog
* Thu Nov 28 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.66.0-2.1
- Backport fix for CA-327906
- Fixes migration for VMs without network devices

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

