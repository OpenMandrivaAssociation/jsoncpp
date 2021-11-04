# (tpg) reduce bloat by excluding cmake requires on devel packages
%global __requires_exclude ^cmake.*$

%bcond_with docs
%define major 24
%define	libname %mklibname %{name} %{major}
%define	devname %mklibname -d %{name}

Summary:	C++ JSON Library
Name:		jsoncpp
Version:	1.9.4
Release:	3
License:	Public Domain
Group:		System/Libraries
Url:		http://jsoncpp.sourceforge.net/
Source0:	https://github.com/open-source-parsers/jsoncpp/archive/%{version}.tar.gz
Patch0:		jsoncpp-1.6.0-work-around-i586-float-inaccuracy.patch
BuildRequires:	cmake
BuildRequires:	ninja
#To generate docs
%if %{with docs}
BuildRequires:	doxygen 
BuildRequires:	graphviz
%endif

%description
JsonCpp is a simple API to manipulate JSON value, handle serialization 
and unserialization to string.

It can also preserve existing comment in unserialization/serialization steps,
making it a convenient format to store user input files.

Unserialization parsing is user friendly and provides precise error reports.

%package -n	%{libname}
Summary:	JsonCpp library
Group:		System/Libraries

%description -n	%{libname}
JsonCpp is a simple API to manipulate JSON value, handle serialization 
and unserialization to string.

It can also preserve existing comment in unserialization/serialization steps,
making it a convenient format to store user input files.

Unserialization parsing is user friendly and provides precise error reports.

%package -n	%{devname}
Summary:	Development files for %{name}
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}
%rename		jsoncpp-devel

%description -n	%{devname}
Files for building applications with %{name} support.

%prep 
%setup -q
%autopatch -p1

%build
%cmake -G Ninja \
	-DJSONCPP_LIB_BUILD_SHARED:BOOL=ON \
	-DJSONCPP_LIB_BUILD_STATIC:BOOL=OFF \
	-DJSONCPP_WITH_TESTS:BOOL=OFF \
	-DJSONCPP_WITH_POST_BUILD_UNITTEST:BOOL=OFF \
	-DJSONCPP_WITH_PKGCONFIG_SUPPORT:BOOL=ON \
	-DJSONCPP_WITH_CMAKE_PACKAGE:BOOL=ON

%ninja_build

%install
%ninja_install -C build

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*
%{_libdir}/lib%{name}.so.%{version}*

%files -n %{devname}
%{_libdir}/lib%{name}.so
%{_libdir}/objects-RelWithDebInfo
%{_includedir}/json
%{_libdir}/cmake/jsoncpp
%{_libdir}/pkgconfig/*.pc
