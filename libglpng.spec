%define major		1
%define libname		%mklibname glpng %{major}
%define develname	%mklibname glpng -d

Summary:	A toolkit for loading PNG images as OpenGL textures
Name:		libglpng
Version:	1.45
Release:	%mkrel 5
License:	MIT
Group:		System/Libraries
# Upstream's dead
Source0:	http://ftp.de.debian.org/debian/pool/main/libg/%{name}/%{name}_%{version}.orig.tar.gz
# From Debian - a Makefile. Yay.
Source1:	libglpng-1.45-makefile
# Debian patch, couple of small fixes.
Patch0:		libglpng-1.45-debian.patch
Patch1:		libglpng-1.45-CVE-2010-1519.diff
URL:		http://packages.debian.org/libglpng
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	png-devel
BuildRequires:	GL-devel

%description
glpng is a small toolkit to make loading PNG image files as an OpenGL
texture as easy as possible.

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libname}
glpng is a small toolkit to make loading PNG image files as an OpenGL
texture as easy as possible.

%package -n %{develname}
Summary:	Development headers for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
glpng is a small toolkit to make loading PNG image files as an OpenGL
texture as easy as possible.

%prep
%setup -q -n %{name}-%{version}.orig
%patch0 -p1 -b .debian
%patch1 -p0 -b .CVE-2010-1519

install -m 0644 %{SOURCE1} ./Makefile

%build
%make CFLAGS="%{optflags} -fPIC -I ./include"

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot}%{_prefix} install
rm -rf %{buildroot}%{_docdir}
%ifarch x86_64
mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}
%endif

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%doc glpng.htm Example/
%defattr(-,root,root)
%{_includedir}/GL/glpng.h
%{_libdir}/%{name}.so
%{_libdir}/%{name}.*a

