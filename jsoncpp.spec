# (tpg) reduce bloat by excluding cmake requires on devel packages
#%%global __requires_exclude ^cmake.*$

%define major 25
%define	libname %mklibname %{name}
%define	devname %mklibname %{name} -d
%define	oldlibname %mklibname %{name} %{major}

%bcond_with docs
# (mandian) jsoncpp_static is required by liblinphone
%bcond_without	static

# Intentionally unversioned, because libname should not contain version number

Summary:	C++ JSON Library
Name:		jsoncpp
Version:	1.9.5
Release:	1
License:	Public Domain
Group:		System/Libraries
Url:		https://github.com/open-source-parsers
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

#---------------------------------------------------------------------------

%package -n	%{libname}
Summary:	JsonCpp library
Group:		System/Libraries
# Intentionally unversioned, because libname should not contain version number
Obsoletes:	%{oldlibname}

%description -n	%{libname}
JsonCpp is a simple API to manipulate JSON value, handle serialization
and unserialization to string.

It can also preserve existing comment in unserialization/serialization steps,
making it a convenient format to store user input files.

Unserialization parsing is user friendly and provides precise error reports.

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*
%{_libdir}/lib%{name}.so.%{version}*

#---------------------------------------------------------------------------

%package -n	%{devname}
Summary:	Development files for %{name}
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}
%rename		jsoncpp-devel

%description -n	%{devname}
Files for building applications with %{name} support.

%files -n %{devname}
%{_libdir}/lib%{name}.so
%{?with_static:
%{_libdir}/lib%{name}.a
}
%{_libdir}/objects-RelWithDebInfo
%{_includedir}/json
%{_libdir}/cmake/jsoncpp
%{_libdir}/pkgconfig/*.pc

#---------------------------------------------------------------------------

%prep
%autosetup -p1

%build
%cmake -G Ninja \
	-DBUILD_SHARED_LIBS:BOOL=ON \
	-DBUILD_STATIC_LIBS:BOOL=%{?with_static:ON}%{?!without_static:OFF} \
	-DJSONCPP_WITH_TESTS:BOOL=OFF \
	-DJSONCPP_WITH_POST_BUILD_UNITTEST:BOOL=OFF \
	-DJSONCPP_WITH_PKGCONFIG_SUPPORT:BOOL=ON \
	-DJSONCPP_WITH_CMAKE_PACKAGE:BOOL=ON

%ninja_build

%install
%ninja_install -C build

