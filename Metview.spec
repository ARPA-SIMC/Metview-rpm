%global releaseno 1

Name:           Metview
Version:        5.20.0
Release:        %{releaseno}%{dist}
Summary:        Metview is an interactive meteorological application
URL:            https://confluence.ecmwf.int/display/METV/Metview
License:        Apache License, Version 2.0
Source0:        https://confluence.ecmwf.int/download/attachments/3964985/%{name}-%{version}-Source.tar.gz
Patch0:         https://raw.githubusercontent.com/ARPA-SIMC/Metview-rpm/v%{version}-%{releaseno}/metview-include-algorithm.patch

BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  rpcgen
BuildRequires:  libtirpc-devel
BuildRequires:  cmake >= 3.12
# forcing libarchive update in CentOS 8 from simc/stable repo
# needed for updated cmake
%{?el8:BuildRequires: libarchive >= 3.3.3}
BuildRequires:  netcdf-devel
BuildRequires:  netcdf-cxx4-devel
BuildRequires:  proj-devel >= 6
BuildRequires:  eccodes-devel >= 2.12.0
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
BuildRequires:  ncurses-devel
BuildRequires:  eigen3-devel
BuildRequires:  blas-devel
BuildRequires:  openssl-devel
BuildRequires:  openjpeg2-devel

# The following is required for ctest
BuildRequires:  eccodes
BuildRequires:  eccodes-data

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
%patch0

%build

mkdir build
pushd build

# https://confluence.ecmwf.int/display/METV/Installation+Guide

cmake .. \
    -DCMAKE_PREFIX_PATH=%{_prefix} \
    -DCMAKE_C_FLAGS="%{optflags} -lgfortran -Wno-incompatible-pointer-types" \
    -DCMAKE_INSTALL_PREFIX=/opt/%{name}-%{version} \
    -DCMAKE_INSTALL_MESSAGE=NEVER \
    -DCMAKE_Fortran_FLAGS="%{optflags}" \
    -DINSTALL_LIB_DIR=%{_lib} \
    -DBUILD_SHARED_LIBS=ON \
    -DENABLE_UI=ON \
    -DENABLE_PLOTTING=ON \
    -DENABLE_OPERA_RADAR=ON

%{make_build}
popd

%check

# tests disabled since they generate a "no space left on device" on copr buildsystem
%{warn:"Tests disabled! (see specfile for details)"}

#pushd build
#CTEST_OUTPUT_ON_FAILURE=1 ECCODES_DEFINITION_PATH=%{_datarootdir}/eccodes/definitions LD_LIBRARY_PATH=%{buildroot}%{_libdir} ctest
#popd

%install
# install all files into the BuildRoot
[ "%{buildroot}" != / ] && rm -rf %{buildroot}

pushd build
%make_install
popd

mkdir -p %{buildroot}/usr/bin

ln -s /opt/%{name}-%{version}/bin/metview %{buildroot}/usr/bin/metview
ln -s /opt/%{name}-%{version}/bin/metview %{buildroot}/usr/bin/metview4
chmod +x %{buildroot}/opt/%{name}-%{version}/lib/metview-bundle/bin/metview_bin/metview_help

%clean
# clean up the hard disk after build
[ "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir /opt/%{name}-%{version}
/opt/%{name}-%{version}*
%{_bindir}/metview
%{_bindir}/metview4

%changelog
* Tue Oct 17 2023 Daniele Branchini <dbranchini@arpae.it> - 5.20.0-1
- Version 5.20.0

* Mon Sep 25 2023 Daniele Branchini <dbranchini@arpae.it> - 5.15.1-2
- Fixed download url for mir, added missing include

* Wed Mar 16 2022 Daniele Branchini <dbranchini@arpae.it> - 5.15.1-1
- Version 5.15.1

* Fri Oct 22 2021 Daniele Branchini <dbranchini@arpae.it> - 5.13.1-1
- Version 5.13.1

* Wed Jun 23 2021 Daniele Branchini <dbranchini@arpae.it> - 5.12.0-2
- fix Argument list too long issue (https://jira.ecmwf.int/browse/SUP-3467)

* Fri Jun  4 2021 Daniele Branchini <dbranchini@arpae.it> - 5.12.0-1
- Version 5.12.0

* Wed Mar 17 2021 Daniele Branchini <dbranchini@arpae.it> - 5.10.2-1
- Version 5.10.2

* Mon Jul 13 2020 Emanuele Di Giacomo <edigiacomo@arpae.it> - 5.9.0-1
- Version 5.9.0

* Wed Jun 24 2020 Daniele Branchini <dbranchini@arpae.it> - 5.8.3-1
- Version 5.8.3, dropping centos 7 support and proj < 6 support

* Wed Mar 18 2020 Daniele Branchini <dbranchini@arpae.it> - 5.7.5-1
- Version 5.7.5

* Thu Jan  9 2020 Daniele Branchini <dbranchini@arpae.it> - 5.7.4-1
- Version 5.7.4

* Fri Sep 20 2019 Daniele Branchini <dbranchini@arpae.it> - 5.6.1-1
- Version 5.6.1

* Wed May 22 2019 Daniele Branchini <dbranchini@arpae.it> - 5.5.3-3
- Restoring metview bundle options to avoid conflicts with atlas-devel

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
