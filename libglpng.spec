%define major		1
%define libname		%mklibname glpng %{major}
%define develname	%mklibname glpng -d

Summary:	A toolkit for loading PNG images as OpenGL textures
Name:		libglpng
Version:	1.45
Release:	9
License:	MIT
Group:		System/Libraries
# Upstream's dead
Source0:	http://ftp.de.debian.org/debian/pool/main/libg/%{name}/%{name}_%{version}.orig.tar.gz
# From Debian - a Makefile. Yay.
Source1:	libglpng-1.45-makefile
# Debian patch, couple of small fixes.
Patch0:		libglpng-1.45-debian.patch
Patch1:		libglpng-1.45-CVE-2010-1519.diff
Patch2:		glpng-1.45-libpng15.patch
URL:		http://packages.debian.org/libglpng
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
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%doc glpng.htm Example/
%{_includedir}/GL/glpng.h
%{_libdir}/%{name}.so
%{_libdir}/%{name}.*a



%changelog
* Tue Oct 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1.45-7mdv2012.0
+ Revision: 702866
- fix build with libpng-1.5.x (mageia)
- attempt to relink against libpng15.so.15

* Fri Apr 29 2011 Oden Eriksson <oeriksson@mandriva.com> 1.45-6
+ Revision: 660254
- mass rebuild

* Sun Sep 12 2010 Oden Eriksson <oeriksson@mandriva.com> 1.45-5mdv2011.0
+ Revision: 577821
- sync with MDVSA-2010:179

* Sun Sep 27 2009 Olivier Blin <blino@mandriva.org> 1.45-4mdv2010.0
+ Revision: 449879
- rediff patch (from Arnaud Patard)

* Tue Dec 09 2008 Adam Williamson <awilliamson@mandriva.org> 1.45-3mdv2009.1
+ Revision: 312108
- quick fix for x86-64
- build with -fPIC (needed for x86-64)
- buildrequires GL-devel
- fix leftover buildrequires
- import libglpng


