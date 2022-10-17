# Copyright 2022 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

Name: protobuf
Epoch: 100
Version: 3.21.5
Release: 1%{?dist}
Summary: Protocol Buffers - Google's data interchange format
License: BSD-3-Clause
URL: https://github.com/protocolbuffers/protobuf/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: cmake
BuildRequires: fdupes
BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: python-rpm-macros
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: zlib-devel

%description
Protocol Buffers are a way of encoding structured data in an efficient yet
extensible format. Google uses Protocol Buffers for almost all of its internal
RPC protocols and file formats.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
pushd src && \
    cmake \
        ../cmake \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=/usr \
        -Dprotobuf_BUILD_LIBPROTOC=ON \
        -Dprotobuf_BUILD_PROTOC_BINARIES=ON \
        -Dprotobuf_BUILD_SHARED_LIBS=ON \
        -Dprotobuf_BUILD_TESTS=OFF && \
popd
pushd src && \
    cmake \
        --build . \
        --parallel 10 \
        --config Release && \
popd
mkdir -p src/.libs
pushd src/.libs && \
    ln -fs ../*.so* . && \
popd
pushd python && \
    python3 setup.py build \
        --cpp_implementation && \
popd

%install
pushd src && \
    export DESTDIR=%{buildroot} && \
    cmake \
        --install . && \
popd
pushd python && \
    python3 setup.py install \
        --cpp_implementation \
        --no-compile \
        --root=%{buildroot} && \
popd
find %{buildroot}%{python3_sitearch} -type f -name '*.pyc' -exec rm -rf {} \;
fdupes -qnrps %{buildroot}%{python3_sitearch}

%if 0%{?suse_version} > 1500 || 0%{?sle_version} > 150000
%package -n libprotobuf3_21_5_0
Summary: Protocol Buffers - Google's data interchange format

%description -n libprotobuf3_21_5_0
Protocol Buffers are a way of encoding structured data in an efficient
yet extensible format. Google uses Protocol Buffers for almost all of
its internal RPC protocols and file formats.

%package -n libprotoc3_21_5_0
Summary: Protocol Buffers - Google's data interchange format

%description -n libprotoc3_21_5_0
Protocol Buffers are a way of encoding structured data in an efficient
yet extensible format. Google uses Protocol Buffers for almost all of
its internal RPC protocols and file formats.

%package -n libprotobuf-lite3_21_5_0
Summary: Protocol Buffers - Google's data interchange format

%description -n libprotobuf-lite3_21_5_0
Protocol Buffers are a way of encoding structured data in an efficient
yet extensible format. Google uses Protocol Buffers for almost all of
its internal RPC protocols and file formats.

%package -n protobuf-devel
Summary: Header files, libraries and development documentation for %{name}
Requires: gcc-c++
Requires: libprotobuf-lite3_21_5_0 = %{epoch}:%{version}-%{release}
Requires: libprotobuf3_21_5_0 = %{epoch}:%{version}-%{release}
Requires: pkgconfig(zlib)
Provides: libprotobuf-devel = %{epoch}:%{version}-%{release}
Conflicts: protobuf2-devel

%description -n protobuf-devel
Protocol Buffers are a way of encoding structured data in an efficient yet
extensible format. Google uses Protocol Buffers for almost all of its internal
RPC protocols and file formats.

%if 0%{?suse_version} > 1500
%package -n python%{python3_version_nodots}-protobuf
Epoch: 100
Version: 4.21.5
Release: 1%{?dist}
Summary: Python3 Bindings for Google Protocol Buffers
Requires: python3
Requires: python3-six >= 1.9
Provides: python3-protobuf = %{epoch}:%{version}-%{release}
Provides: python3dist(protobuf) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}-protobuf = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}dist(protobuf) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}-protobuf = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}dist(protobuf) = %{epoch}:%{version}-%{release}

%description -n python%{python3_version_nodots}-protobuf
This package contains the Python bindings for Google Protocol Buffers.
%endif

%if 0%{?sle_version} > 150000
%package -n python3-protobuf
Epoch: 100
Version: 4.21.5
Release: 1%{?dist}
Summary: Python3 Bindings for Google Protocol Buffers
Requires: python3
Requires: python3-six >= 1.9
Provides: python3-protobuf = %{epoch}:%{version}-%{release}
Provides: python3dist(protobuf) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}-protobuf = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}dist(protobuf) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}-protobuf = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}dist(protobuf) = %{epoch}:%{version}-%{release}

%description -n python3-protobuf
This package contains the Python bindings for Google Protocol Buffers.
%endif

%post -n libprotobuf3_21_5_0 -p /sbin/ldconfig
%postun -n libprotobuf3_21_5_0 -p /sbin/ldconfig
%post -n libprotoc3_21_5_0 -p /sbin/ldconfig
%postun -n libprotoc3_21_5_0 -p /sbin/ldconfig
%post -n libprotobuf-lite3_21_5_0 -p /sbin/ldconfig
%postun -n libprotobuf-lite3_21_5_0 -p /sbin/ldconfig

%files -n libprotobuf3_21_5_0
%license LICENSE
%{_libdir}/libprotobuf.so.*

%files -n libprotoc3_21_5_0
%{_libdir}/libprotoc.so.*

%files -n libprotobuf-lite3_21_5_0
%{_libdir}/libprotobuf-lite.so.*

%files -n protobuf-devel
%dir %{_includedir}/google
%dir %{_libdir}/cmake
%dir %{_libdir}/cmake/protobuf
%{_bindir}/*
%{_includedir}/google/protobuf/
%{_libdir}/cmake/protobuf/*.cmake
%{_libdir}/libprotobuf-lite.so
%{_libdir}/libprotobuf.so
%{_libdir}/libprotoc.so
%{_libdir}/pkgconfig/protobuf-lite.pc
%{_libdir}/pkgconfig/protobuf.pc

%if 0%{?suse_version} > 1500
%files -n python%{python3_version_nodots}-protobuf
%license LICENSE
%{python3_sitearch}/*
%endif

%if 0%{?sle_version} > 150000
%files -n python3-protobuf
%license LICENSE
%{python3_sitearch}/*
%endif
%endif

%if !(0%{?suse_version} > 1500) && !(0%{?sle_version} > 150000)
%package -n protobuf-compiler
Summary: Protocol Buffers compiler
Requires: protobuf = %{epoch}:%{version}-%{release}

%description -n protobuf-compiler
This package contains Protocol Buffers compiler for all programming
languages

%package -n protobuf-devel
Summary: Protocol Buffers C++ headers and libraries
Requires: protobuf = %{epoch}:%{version}-%{release}
Requires: protobuf-compiler = %{epoch}:%{version}-%{release}
Requires: zlib-devel
Requires: pkgconfig

%description -n protobuf-devel
This package contains Protocol Buffers compiler for all languages and
C++ headers and libraries

%package -n protobuf-lite
Summary: Protocol Buffers LITE_RUNTIME libraries

%description -n protobuf-lite
Protocol Buffers built with optimize_for = LITE_RUNTIME.

%package -n protobuf-lite-devel
Summary: Protocol Buffers LITE_RUNTIME development libraries
Requires: protobuf-devel = %{epoch}:%{version}-%{release}
Requires: protobuf-lite = %{epoch}:%{version}-%{release}

%description -n protobuf-lite-devel
This package contains development libraries built with optimize_for =
LITE_RUNTIME.

%package -n python3-protobuf
Epoch: 100
Version: 4.21.5
Release: 1%{?dist}
Summary: Python 3 bindings for Google Protocol Buffers
Requires: python3-six >= 1.9
Provides: python3-protobuf = %{epoch}:%{version}-%{release}
Provides: python3dist(protobuf) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}-protobuf = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}dist(protobuf) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}-protobuf = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}dist(protobuf) = %{epoch}:%{version}-%{release}

%description -n python3-protobuf
This package contains Python 3 libraries for Google Protocol Buffers

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%post -n protobuf-compiler -p /sbin/ldconfig
%postun -n protobuf-compiler -p /sbin/ldconfig
%post -n protobuf-lite -p /sbin/ldconfig
%postun -n protobuf-lite -p /sbin/ldconfig

%files
%license LICENSE
%{_libdir}/libprotobuf.so.*

%files -n protobuf-compiler
%{_bindir}/*
%{_libdir}/libprotoc.so.*

%files -n protobuf-devel
%dir %{_includedir}/google
%dir %{_libdir}/cmake
%dir %{_libdir}/cmake/protobuf
%{_includedir}/google/protobuf/
%{_libdir}/cmake/protobuf/*.cmake
%{_libdir}/libprotobuf.so
%{_libdir}/libprotoc.so
%{_libdir}/pkgconfig/protobuf.pc

%files -n protobuf-lite
%{_libdir}/libprotobuf-lite.so.*

%files -n protobuf-lite-devel
%{_libdir}/libprotobuf-lite.so
%{_libdir}/pkgconfig/protobuf-lite.pc

%files -n python3-protobuf
%{python3_sitearch}/*
%endif

%changelog
