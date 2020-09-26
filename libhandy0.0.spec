%bcond_with glade

%define api		0.0
%define major		0
%define libname		%mklibname handy %{api} %{major}
%define girhandyname	%mklibname handy-gir %{api}
%define develname	%mklibname handy -d %{api}

Name:		libhandy0.0
Version:	0.0.13
Release:	1
Summary:	Old compact version of a GTK+ library to develop UI for mobile devices
License:	LGPLv2+
Group:		Development/GNOME and GTK+
URL:		https://gitlab.gnome.org/GNOME/libhandy/
Source0:	https://gitlab.gnome.org/GNOME/libhandy/-/archive/v%{version}/libhandy-v%{version}.tar.bz2
Patch1:		libhandy-adapt-glade-3-36.patch

BuildRequires:	gtk-doc
BuildRequires:	meson
BuildRequires:	vala
%if %{with glade}
BuildRequires:	pkgconfig(gladeui-2.0)
%endif
BuildRequires:	pkgconfig(gnome-desktop-3.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.24.1

%description
libhandy is a library to help with developing UI for mobile devices
using GTK+/GNOME.

#------------------------------------------------

%package -n	%{libname}
Summary:	A GTK+ library to develop UI for mobile devices
Group:		System/Libraries

%description -n	%{libname}
This package provides the shared library for libhandy, a library to
help with developing mobile UI using GTK+/GNOME.

#------------------------------------------------

%package -n	%{girhandyname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n	%{girhandyname}
GObject Introspection interface description for %{name}.

#------------------------------------------------

%package -n	%{develname}
Summary:	Development package for %{name}
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girhandyname} = %{version}-%{release}
Provides:	handy%{api}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
Header files for development with %{name}.

#------------------------------------------------
%if %{with glade}

%package -n	%{name}-glade
Summary:	Glade (GTK+3) modules for %{name}
Group:		Graphical desktop/GNOME
Requires:	glade

%description -n	%{name}-glade
This package provides a catalog for Glade (GTK+3) which allows the use
of the provided Handy widgets in Glade.

%endif
#------------------------------------------------

%prep
%autosetup -p1 -n libhandy-v%{version}

%build
%meson \
	-Dprofiling=false \
	-Dstatic=false \
	-Dintrospection=enabled \
	-Dvapi=true \
	-Dgtk_doc=true \
	-Dtests=false \
	-Dexamples=false \
%if %{with glade}
	-Dglade_catalog=enabled \
%else
	-Dglade_catalog=disabled \
%endif
	%{nil}
%meson_build

%install
%meson_install

%files -n %{libname}
%{_libdir}/libhandy-%{api}.so.%{major}{,.*}

%files -n %{girhandyname}
%{_libdir}/girepository-1.0/Handy-%{api}.typelib

%files -n %{develname}
%license COPYING
%doc AUTHORS README.md
%{_includedir}/libhandy-%{api}/
%{_libdir}/libhandy-%{api}.so
%{_datadir}/gir-1.0/Handy-%{api}.gir
%{_libdir}/pkgconfig/libhandy-%{api}.pc
%{_datadir}/vala/vapi/libhandy-%{api}.deps
%{_datadir}/vala/vapi/libhandy-%{api}.vapi
%{_datadir}/gtk-doc/html/libhandy/

%if %{with glade}
%files -n %{name}-glade
%{_libdir}/glade/modules/*.so
%{_datadir}/glade/catalogs/*.xml
%endif
