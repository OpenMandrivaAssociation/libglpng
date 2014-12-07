%define major	1
%define libname	%mklibname glpng %{major}
%define devname	%mklibname glpng -d
%define staticname %mklibname glpng -d -s

Summary:	A toolkit for loading PNG images as OpenGL textures
Name:		libglpng
Version:	1.45
Release:	16
License:	MIT
Group:		System/Libraries
Url:		http://packages.debian.org/libglpng
# Upstream's dead
Source0:	http://ftp.de.debian.org/debian/pool/main/libg/%{name}/%{name}_%{version}.orig.tar.gz
# From Debian - a Makefile. Yay.
Source1:	libglpng-1.45-makefile
# Debian patch, couple of small fixes.
Patch0:		libglpng-1.45-debian.patch
Patch1:		libglpng-1.45-CVE-2010-1519.diff
Patch2:		glpng-1.45-libpng15.patch
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(gl)

%description
glpng is a small toolkit to make loading PNG image files as an OpenGL
texture as easy as possible.

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libname}
glpng is a small toolkit to make loading PNG image files as an OpenGL
texture as easy as possible.

%package -n %{devname}
Summary:	Development headers for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
glpng is a small toolkit to make loading PNG image files as an OpenGL
texture as easy as possible.

%package -n %{staticname}
Summary:	Static libraries for %{name}
Group:		Development/C
Requires:	%{devname} = %{version}-%{release}

%description -n %{staticname}
glpng is a small toolkit to make loading PNG image files as an OpenGL
texture as easy as possible.

%prep
%setup -qn %{name}-%{version}.orig
%patch0 -p1 -b .debian
%patch1 -p0 -b .CVE-2010-1519
%patch2 -p1 -b .libpng15

install -m 0644 %{SOURCE1} ./Makefile

%build
%make CFLAGS="%{optflags} -fPIC -I ./include"

%install
make DESTDIR=%{buildroot}%{_prefix} install
rm -rf %{buildroot}%{_docdir}
%ifarch x86_64
mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}
%endif

chmod 0755 %{buildroot}%{_libdir}/*.so.%{major}*

%files -n %{libname}
%{_libdir}/libglpng.so.%{major}*

%files -n %{devname}
%doc glpng.htm Example/
%{_includedir}/GL/glpng.h
%{_libdir}/%{name}.so

%files -n %{staticname}
%{_libdir}/%{name}.a
