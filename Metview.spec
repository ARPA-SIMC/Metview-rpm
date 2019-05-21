%if 0%{?rhel} == 7
%define cmake_vers cmake3
%define ctest_vers ctest3
%else
%define cmake_vers cmake
%define ctest_vers ctest
%endif

Name:           Metview
Version:        5.5.3
Release:        2%{dist}
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
BuildRequires:  eccodes-devel >= 2.12.0
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

# The following is required for ctest
BuildRequires:  eccodes
BuildRequires:  eccodes-data

%if 0%{?rhel} == 7
# newer gcc needed
BuildRequires: devtoolset-7
%endif


# SunRPC has been removed from glibc since version 2.26, so newer systems should rely on tirpc instead
# https://fedoraproject.org/wiki/Changes/SunRPCRemoval

%if 0%{?fedora} >= 28
%define norpc 1
%endif

%{?norpc:BuildRequires: rpcgen libtirpc-devel}
# required in scripts
Requires: hostname /usr/bin/xdpyinfo
# launched by UI
Requires: xterm vi
# not installed as dependency on barebone systems, without it keyboard
# does not work
Requires: xkeyboard-config

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
%if 0%{?rhel} == 7
    -DCMAKE_C_COMPILER=/opt/rh/devtoolset-7/root/usr/bin/gcc \
    -DCMAKE_CXX_COMPILER=/opt/rh/devtoolset-7/root/usr/bin/g++ \
    -DCMAKE_Fortran_COMPILER=/usr/bin/gfortran \
%endif
    -DCMAKE_CXX_FLAGS="%{optflags} -L/opt/rh/devtoolset-7/root/usr/lib64 -L/opt/rh/devtoolset-7/root/usr/lib/gcc/x86_64-redhat-linux/7/ -I/opt/rh/devtoolset-7/root/usr/local/include -Wno-unused -Wno-deprecated-declarations -Wno-error=format-security %{?norpc:-I/usr/include/tirpc -ltirpc}" \
    -DCMAKE_C_FLAGS="%{optflags} -L/opt/rh/devtoolset-7/root/usr/lib64 -L/opt/rh/devtoolset-7/root/usr/lib/gcc/x86_64-redhat-linux/7/ -I/opt/rh/devtoolset-7/root/usr/local/include -Wno-unused %{?norpc:-I/usr/include/tirpc -ltirpc}" \
    -DGRIB_API_INCLUDE_DIR=%{_libdir}/gfortran/modules \
    -DBUILD_SHARED_LIBS=ON \
    -DENABLE_UI=ON \
    -DENABLE_PLOTTING=ON \
    -DENABLE_OPERA_RADAR=ON \
    -DENABLE_EXPOSE_SUBPACKAGES=ON

#    -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON 

%{make_build}
popd

%check

# test disabled since they generate a "no space left on device" on copr buildsystem
%{warn:"Tests disabled! (see specfile for details)"}

#if 0%{?rhel} == 7

# TODO: investigate tests failures
#The following tests FAILED:
#418 - nccombine_bounds_merge_2 (Failed)
#421 - test_compute_req (Failed)
#422 - test_interpolation_wave_req (Failed)
#423 - test_interpolation_gaussian_req (Failed)
#424 - test_interpolation_l137_req (Failed)
#425 - test_interpolation_rgg2ll_req (Failed)
#426 - test_interpolation_latlon_req (Failed)
#427 - test_interpolation_sh2ll_req (Failed)
#428 - test_transform_vod2uv_req (Failed)
#430 - test_retrieve_enfo_req (Failed)
#431 - test_retrieve_ocean_req (Failed)
#432 - test_retrieve_fdb_uv_pl_req (Failed)
#433 - test_retrieve_fdb_uv_ml_req (Failed)
#434 - test_MARSC_94_req (Failed)
#447 - interp_emos.mv_dummy_target (Failed)

#pushd build
#CTEST_OUTPUT_ON_FAILURE=1 ECCODES_DEFINITION_PATH=%{_datarootdir}/eccodes/definitions LD_LIBRARY_PATH=%{buildroot}%{_libdir}:/opt/rh/devtoolset-7/root/usr/lib64/:/opt/rh/devtoolset-7/root/usr/lib/gcc/x86_64-redhat-linux/7/ %{ctest_vers}
#popd


#else

#pushd build
#CTEST_OUTPUT_ON_FAILURE=1 ECCODES_DEFINITION_PATH=%{_datarootdir}/eccodes/definitions LD_LIBRARY_PATH=%{buildroot}%{_libdir} %{ctest_vers}
#popd

#endif

%install
# install all files into the BuildRoot
[ "%{buildroot}" != / ] && rm -rf %{buildroot}

pushd build
%make_install
popd

ln -s metview $RPM_BUILD_ROOT/usr/bin/metview4

# this is hideous
# TODO: fix /etc/ path
mv $RPM_BUILD_ROOT/usr/etc/ $RPM_BUILD_ROOT/etc/

%clean
# clean up the hard disk after build
[ "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)

%dir %{_bindir}/metview_bin
%{_bindir}/metview_bin/*
%{_bindir}/metview
%{_bindir}/metview4
%{_bindir}/atlas*
%{_bindir}/*
%dir %{_sysconfdir}/mir
%{_sysconfdir}/mir/*
%dir %{_includedir}/atlas
%{_includedir}/atlas/*
%dir %{_includedir}/eckit
%{_includedir}/eckit/*
%{_includedir}/macro_api.h
%{_includedir}/metview_ecbuild_config.h
%{_includedir}/mars_client_ecbuild_config.h
%dir %{_includedir}/mir
%{_includedir}/mir/*
%{_libdir}/lib*
%{_libdir}/pkgconfig/*.pc
%exclude %{_datadir}/MetviewMiniBundle
%{_datadir}/applications/metview.desktop
%dir %{_datadir}/atlas/
%{_datadir}/atlas/*
%dir %{_datadir}/eckit/
%{_datadir}/eckit/*
%dir %{_datadir}/mars_client/
%{_datadir}/mars_client/*
%dir %{_datadir}/metview/
%{_datadir}/metview/*
%dir %{_datadir}/mir/
%{_datadir}/mir/*

%changelog
* Tue May 21 2019 Daniele Branchini <dbranchini@arpae.it> - 5.5.3-2
- Disabling tests for issues on copr buildsystem

* Thu May 16 2019 Daniele Branchini <dbranchini@arpae.it> - 5.5.3-1
- Version 5.5.3
- Forced old gfortran compiler to match eccodes/Magics packages

* Mon May  6 2019 Daniele Branchini <dbranchini@arpae.it> - 5.5.0-2
- Added CentOs7 dependency for newer gcc

* Mon Apr 15 2019 Daniele Branchini <dbranchini@arpae.it> - 5.5.0-1
- Version 5.5.0

* Tue Oct 23 2018 Daniele Branchini <dbranchini@arpae.it> - 5.2.1-1
- Version 5.2.1

* Mon Sep 10 2018 Daniele Branchini <dbranchini@arpae.it> - 5.1.1-1
- Version 5.1.1
