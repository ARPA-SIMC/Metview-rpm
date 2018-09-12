%if 0%{?rhel} == 7
%define cmake_vers cmake3
%define ctest_vers ctest3
%else
%define cmake_vers cmake
%define ctest_vers ctest
%endif

Name:           Metview
Version:        5.1.1
Release:        1%{dist}
Summary:        Metview is an interactive meteorological application
URL:            https://confluence.ecmwf.int/display/METV/Metview
License:        Apache License, Version 2.0
Source0:        https://confluence.ecmwf.int/download/attachments/3964985/%{name}-%{version}-Source.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  cmake
%{?rhel:BuildRequires: cmake3}
BuildRequires:  netcdf-devel
BuildRequires:  netcdf-cxx-devel
%{?fedora:BuildRequires: netcdf-cxx4-devel}
BuildRequires:  proj-devel
BuildRequires:  eccodes-devel
BuildRequires:  libemos
BuildRequires:  Magics-devel
BuildRequires:  boost-devel
BuildRequires:  git
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  byacc
BuildRequires:  gdbm-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qtxmlpatterns-devel
BuildRequires:  cairo-devel
BuildRequires:  pango-devel
BuildRequires:  libgeotiff-devel
BuildRequires:  jasper-devel
BuildRequires:  fftw-devel

# SunRPC has been removed from glibc since version 2.26, so newer systems should rely on tirpc instead
# https://fedoraproject.org/wiki/Changes/SunRPCRemoval
%{?fedora:BuildRequires: rpcgen libtirpc-devel}

%description
Metview is a meteorological workstation application designed to be
a complete working environment for both the operational and research
meteorologist.
Its capabilities include powerful data access, processing and visualisation.
It features a powerful icon-based user interface for interactive work, and
a scripting language for batch processing. The two are linked through the
ability to automatically convert icons into their equivalent script code.

Metview can take input data from a variety of sources, including:
 - GRIB files (editions 1 and 2)
 - BUFR files
 - MARS (ECMWFs meteorological archive)
 - ODB (Observation Database)
 - Local databases
 - ASCII data files (CSV, grids and scattered data)
 - NetCDF

 Powerful data filtering and processing facilities are then available, and
if graphics output is desired, then Metview can produce many plot types,
including:
 - map views in various projections
 - cross sections
 - vertical profiles
 - x/y graph plots
 - intelligent overlay of data from various sources on the same map
 - arrangement of multiple plots on the same page

Metview was developed as part of a cooperation between ECMWF and INPE/CPTEC
(Brazilian National Institute for Space Research / Centre for Weather
Forecasts and Climate Studies).

%prep
%setup -q -n %{name}-%{version}-Source

%build

mkdir build
pushd build

# https://confluence.ecmwf.int/display/METV/Installation+Guide

%{cmake_vers} .. \
    -DCMAKE_PREFIX_PATH=%{_prefix} \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_MESSAGE=NEVER \
    -DINSTALL_LIB_DIR=%{_lib} \
    -DCMAKE_CXX_FLAGS="%{optflags} -Wno-unused -Wno-deprecated-declarations -Wno-error=format-security %{?fedora:-I/usr/include/tirpc -ltirpc}" \
    -DCMAKE_C_FLAGS="%{optflags} -Wno-unused %{?fedora:-I/usr/include/tirpc -ltirpc}" \
    -DGRIB_API_PATH=%{_libdir} \
    -DGRIB_API_INCLUDE_DIR=%{_libdir}/gfortran/modules \
    -DBUILD_SHARED_LIBS=ON \
    -DENABLE_UI=ON \
    -DENABLE_PLOTTING=ON \
    -DENABLE_OPERA_RADAR=ON

%{make_build}
popd

%check

pushd build
%{ctest_vers} -VV
popd

%install
# install all files into the BuildRoot
[ "%{buildroot}" != / ] && rm -rf %{buildroot}
pushd build
%make_install
popd

ln -s metview $RPM_BUILD_ROOT/usr/bin/metview4

%clean
# clean up the hard disk after build
[ "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)

%dir %{_bindir}/metview_bin
%{_bindir}/metview_bin/*
%{_bindir}/metview
%{_bindir}/metview4
%{_includedir}/macro_api.h
%{_includedir}/metview_ecbuild_config.h
%{_datadir}/metview
%{_datadir}/applications/metview.desktop
%{_libdir}/libmacro_api_c.a
%{_libdir}/libmacro_api_f90.a
%{_libdir}/libMetview.so
%{_libdir}/libMvFTimeUtil.so
%{_libdir}/libMvMacro.so
%{_libdir}/libMvMars.so

%changelog
* Mon Sep 10 2018 Daniele Branchini <dbranchini@arpae.it> - 5.1.1-1
- Version 5.1.1
