#
# spec file for package zypperx
#
# Copyright (c) 2025 itachi_re <xanbenson99@gmail.com>
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

Name:           zypperx
Version:        1.1.1
Release:        0
Summary:        A blazingly fast parallel wrapper for zypper
License:        GPL-3.0-or-later
Group:          System/Packages
URL:            https://github.com/itachi-re/zypperx
Source:         %{name}-%{version}.tar.zst
BuildRequires:  python3-base
BuildRequires:  python-rpm-macros
Requires:       python3
Requires:       python3-rich
Requires:       zypper
Requires:       util-linux
Conflicts:      zypperoni
BuildArch:      noarch

%description
ZypperX is a parallel wrapper for the zypper package manager.
It accelerates repository refreshes and package downloads by running
them in isolated chroot environments concurrently.
It behaves exactly like zypper but runs download operations in parallel.

%prep
%setup -q

%build
# Pure Python script, no compilation needed.

%install
install -D -m 0755 zypperx %{buildroot}%{_bindir}/zypperx
sed -i 's|#!/usr/bin/env python3|#!/usr/bin/python3|' %{buildroot}%{_bindir}/zypperx

%check
python3 -c "import ast; ast.parse(open('%{buildroot}%{_bindir}/zypperx').read())"

%files
%license LICENSE
%doc README.md
%{_bindir}/zypperx

%changelog
* Sun Mar 22 2026 itachi_re <xanbenson99@gmail.com> - 1.1.0-0
- Safety overhaul and automatic pre-refresh cache clean
- Fix startup crash from duplicate -f/--force and -d/--download-only argparse flags
- Fix potential /var deletion by checking /proc/mounts before rmtree
- Fix mount cleanup order using dynamic /proc/mounts read, deepest-first
- Fix /var/lib/zypp incorrectly mounted read-write inside worker chroot
- Fix unshare check to perform a real functional namespace test
- Fix download queue incorrectly including packages scheduled for removal
- Run zypper clean --all automatically before every refresh (--no-clean to skip)
- Add SIGINT/SIGTERM handlers for clean lock release and workspace removal
- Use realpath for /bin /sbin /lib /lib64 bind mounts (Tumbleweed symlink fix)

* Mon Nov 24 2025 itachi_re <xanbenson99@gmail.com> - 0.0.5-0
- Update to GPLv3 license
- Fix critical network issues in chroot (DNS resolution)
- Add bind mounts for /etc/ssl and certificates
- Implement tmpfs for /run to securely hide lock file

* Sat Nov 22 2025 itachi_re <xanbenson99@gmail.com> - 0.0.3-0
- Fix deadlock: Move transaction calculation outside of locked scope
