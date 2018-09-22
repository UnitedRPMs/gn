%global debug_package %{nil}

Name:           gn
Version:        0.1463 
Release:        1%{?dist}
Summary:        A meta-build system that generates build files for Ninja
License:        BSD
Group:          Development/Tools/Building 
URL:            https://gn.googlesource.com/
Source:         https://dev.gentoo.org/~floppym/dist/%{name}-%{version}.tar.gz
Patch0:         gn-flags.patch
BuildRequires:	clang llvm

BuildRequires:  ninja-build
BuildRequires:  python2-devel

%description
GN is a meta-build system that generates build files for Ninja.

%prep
%setup -q
%patch0 -p1

%build
export CC=clang
export CXX=clang++
export AR=ar

# bootstrap
python2 build/gen.py --no-sysroot --no-last-commit-position
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

* Thu Jul 26 2018 - David Va <davidva AT tuta DOT io> 0.1463-1
- Initial build
