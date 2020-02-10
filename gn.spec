#
# spec file for package ffmpeg
#
# Copyright (c) 2020 UnitedRPMs.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://goo.gl/zqFJft
#

# 
%define _legacy_common_support 1

%global debug_package %{nil}

Name:           gn
Version:        0.1616
Release:        1%{?dist}
Summary:        A meta-build system that generates build files for Ninja
License:        BSD
Group:          Development/Tools/Building 
URL:            https://gn.googlesource.com/
Source:         https://dev.gentoo.org/~floppym/dist/gn-0.1616.tar.xz
Patch0:         gn-gen-r3.patch
Patch1:         gn-always-python3.patch

BuildRequires:	llvm clang

BuildRequires:  ninja-build
BuildRequires:  python3-devel

%description
GN is a meta-build system that generates build files for Ninja.

%prep
%autosetup -p1 


%build

find -depth -type f -writable -name "*.py" -exec sed -iE '1s=^#! */usr/bin/\(python\|env python\)[23]\?=#!%{__python3}=' {} +

# bootstrap
python3 build/gen.py --no-last-commit-position
cat >out/last_commit_position.h <<-EOF
	#ifndef OUT_LAST_COMMIT_POSITION_H_
	#define OUT_LAST_COMMIT_POSITION_H_
	#define LAST_COMMIT_POSITION "${PV}"
	#endif  // OUT_LAST_COMMIT_POSITION_H_
EOF

%ninja_build -C out gn

%install
install -Dm 0755 out/%{name} %{buildroot}%{_bindir}/%{name}

%files
%license LICENSE
%{_bindir}/%{name}

%changelog

* Thu Feb 06 2020 - David Va <davidva AT tuta DOT io> 0.1616-1
- Updated to 0.1616
- Migration to python3

* Thu Apr 25 2019 - David Va <davidva AT tuta DOT io> 0.1544-1
- Updated to 0.1544 

* Thu Jul 26 2018 - David Va <davidva AT tuta DOT io> 0.1463-1
- Initial build
