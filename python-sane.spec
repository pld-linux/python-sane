#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Python 2 SANE module
Summary(pl.UTF-8):	Moduł SANE dla Pythona 2
Name:		python-sane
# keep 2.8.x here for python2 support
Version:	2.8.3
Release:	5
License:	MIT-like
Group:		Libraries/Python
#Source0Download: https://github.com/python-pillow/Sane/releases
Source0:	https://github.com/python-pillow/Sane/archive/v%{version}/Sane-%{version}.tar.gz
# Source0-md5:	96877da43524fdab2c367541da547d2b
URL:		https://github.com/python-pillow/Sane
%if %{with python2}
BuildRequires:	python-devel >= 1:2.6
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.2
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sane-backends-devel
%if %{with doc}
# mocking _sane module doesn't work with python 3.8, so use python2 here
BuildRequires:	python-mock
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-modules >= 1:2.6
Requires:	python-numpy
Requires:	python-pillow
Obsoletes:	python-PIL-sane < 1:2.0
Obsoletes:	python-pysane < 2.7.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The SANE module provides an interface to the SANE scanner and frame
grabber interface for Linux.

%description -l pl.UTF-8
Moduł SANE udostępnia interfejs do biblioteki SANE będącej interfejsem
do skanerów i urządzeń przechwytujących ramki obrazu dla Linuksa.

%package -n python3-sane
Summary:	Python 3 SANE module
Summary(pl.UTF-8):	Moduł SANE dla Pythona 3
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2
Requires:	python3-numpy
Requires:	python3-pillow

%description -n python3-sane
The SANE module provides an interface to the SANE scanner and frame
grabber interface for Linux.

%description -n python3-sane -l pl.UTF-8
Moduł SANE udostępnia interfejs do biblioteki SANE będącej interfejsem
do skanerów i urządzeń przechwytujących ramki obrazu dla Linuksa.

%package apidocs
Summary:	API documentation for Python SANE module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona SANE
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Python SANE module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona SANE.

%prep
%setup -q -n Sane-%{version}

%build
%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst COPYING README.rst sanedoc.txt
%attr(755,root,root) %{py_sitedir}/_sane.so
%{py_sitedir}/sane.py[co]
%{py_sitedir}/python_sane-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-sane
%defattr(644,root,root,755)
%doc CHANGES.rst COPYING README.rst sanedoc.txt
%attr(755,root,root) %{py3_sitedir}/_sane.cpython-*.so
%{py3_sitedir}/sane.py
%{py3_sitedir}/__pycache__/sane.cpython-*.py[co]
%{py3_sitedir}/python_sane-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{_static,*.html,*.js}
%endif
