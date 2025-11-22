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
Version:        0.0.0
Release:        0
Summary:        A blazingly fast parallel wrapper for zypper
License:        MIT
Group:          System/Packages
URL:            https://github.com/itachi-re/zypperx
Source:         %{name}-%{version}.tar.zst
BuildRequires:  python3-base
BuildRequires:  python-rpm-macros
BuildRequires:  python3-rich
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
%{buildroot}%{_bindir}/zypperx --version
%files
%license LICENSE
%doc README.md
%{_bindir}/zypperx

%changelog
* Sat Nov 22 2025 itachi_re <xanbenson99@gmail.com> - 0.0.2-0
- Initial package release
- Implemented parallel download with chroot isolation
- Added atomic locking and signal handling
