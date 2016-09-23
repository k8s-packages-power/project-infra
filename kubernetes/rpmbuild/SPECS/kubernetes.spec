%if 0%{?fedora}
%global with_devel 1
%global with_bundled 1
%global with_debug 0
%else
%global with_devel 0
%global with_bundled 1
%global with_debug 0
%endif

%if 0%{?with_debug}
# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif
%global provider	github
%global provider_tld	com
%global project		kubernetes
%global repo		kubernetes
# https://github.com/kubernetes/kubernetes
%global provider_prefix	%{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     k8s.io/kubernetes
%global commit          dfce7e639b341a13a1b6c8c1c52517949772b650
%global shortcommit	%(c=%{commit}; echo ${c:0:7})

%global con_provider         github
%global con_provider_tld     com
%global con_project          kubernetes
%global con_repo             contrib
%global con_provider_prefix  %{con_provider}.%{con_provider_tld}/%{con_project}/%{con_repo}
%global con_commit          d519cddaa0b85d37cc912fa6cf2c0592c2b8cf74
%global con_shortcommit      %(c=%{con_commit}; echo ${c:0:7})


#I really need this, otherwise "version_ldflags=$(kube::version_ldflags)"
# does not work
%global _buildshell	/bin/bash
%global _checkshell	/bin/bash

Name:		kubernetes
Version:        1.4.0
Release:        1.beta9.git%{shortcommit}%{?dist}
Summary:        Container cluster management
License:        ASL 2.0
URL:            %{import_path}
#ExclusiveArch:  x86_64
Source0:        kubernetes-%{shortcommit}.tar.gz
Source1:        https://%{provider}.%{provider_tld}/%{project}/%{con_repo}/archive/%{con_commit}/%{con_repo}-%{con_shortcommit}.tar.gz
Source2:        genmanpages.sh
#Patch1:         Fix-Persistent-Volumes-and-Persistent-Volume-Claims.patch
#Patch2:         Change-etcd-server-port.patch
%if 0%{?with_debug}
#Patch3:         build-with-debug-info.patch
%endif
#Patch4:         change-internal-to-inteernal.patch

# It obsoletes cadvisor but needs its source code (literally integrated)
Obsoletes:      cadvisor

# kubernetes is decomposed into master and node subpackages
# require both of them for updates
Requires: kubernetes-master = %{version}-%{release}
Requires: kubernetes-node = %{version}-%{release}

%description
%{summary}

%if 0%{?with_devel}
%package devel
Summary:       %{summary}
#BuildRequires: golang >= 1.2.1-3

%description devel
%{summary}

This package contains library source intended for
building other packages which use %{project}/%{repo}.
%endif

%package unit-test
Summary: %{summary} - for running unit tests

# below Rs used for testing
#Requires: golang >= 1.2-7
Requires: etcd >= 2.0.9
Requires: hostname
Requires: rsync
Requires: NetworkManager

%description unit-test
%{summary} - for running unit tests

%package master
Summary: Kubernetes services for master host

#BuildRequires: golang >= 1.2-7
BuildRequires: systemd
BuildRequires: rsync
#BuildRequires: go-md2man

Requires(pre): shadow-utils
Requires: kubernetes-client = %{version}-%{release}

# if node is installed with node, version and release must be the same
Conflicts: kubernetes-node < %{version}-%{release}
Conflicts: kubernetes-node > %{version}-%{release}

%description master
Kubernetes services for master host

%package node
Summary: Kubernetes services for node host

%if 0%{?fedora} >= 21 
Requires: docker
%else
Requires: docker-io
%endif

#BuildRequires: golang >= 1.2-7
BuildRequires: systemd
BuildRequires: rsync
#BuildRequires: go-md2man

Requires(pre): shadow-utils
Requires: socat
Requires: kubernetes-client = %{version}-%{release}

# if master is installed with node, version and release must be the same
Conflicts: kubernetes-master < %{version}-%{release}
Conflicts: kubernetes-master > %{version}-%{release}

%description node
Kubernetes services for node host

%package client
Summary: Kubernetes client tools

#BuildRequires: golang >= 1.2-7

%description client
Kubernetes client tools like kubectl

%prep
%setup -q -n %{con_repo}-%{con_commit} -T -b 1
%setup -q -n %{repo}-%{commit}
# move content of contrib back to kubernetes
mv ../%{con_repo}-%{con_commit}/init contrib/init

#%patch1 -p1
#%patch2 -p1
#%if 0%{?with_debug}
#%patch3 -p1
#%endif
#%patch4 -p1

%build
export KUBE_GIT_TREE_STATE="clean"
export KUBE_GIT_COMMIT=%{commit}
KUBE_GIT_VERSION=1.4.0-beta.9

hack/build-go.sh --use_go_build
#hack/build-go.sh --use_go_build cmd/kube-version-change

hack/update-generated-docs.sh

# convert md to man
pushd docs
pushd admin
cp kube-apiserver.md kube-controller-manager.md kube-proxy.md kube-scheduler.md kubelet.md ..
popd
cp %{SOURCE2} genmanpages.sh
bash genmanpages.sh
popd

%install
. hack/lib/init.sh
kube::golang::setup_env

output_path="${KUBE_OUTPUT_BINPATH}/$(kube::golang::current_platform)"

binaries=(kube-apiserver kube-controller-manager kube-scheduler kube-proxy kubelet kubectl )
install -m 755 -d %{buildroot}%{_bindir}
for bin in "${binaries[@]}"; do
  echo "+++ INSTALLING ${bin}"
  install -p -m 755 -t %{buildroot}%{_bindir} ${output_path}/${bin}
done

# install the bash completion
install -d -m 0755 %{buildroot}%{_datadir}/bash-completion/completions/
if [ ! -e "contrib/completions/bash/kubectl" ]; then
  install -d -m 0755 contrib/completions/bash
  ${output_path}/kubectl completion bash > contrib/completions/bash/kubectl
fi 

install -t %{buildroot}%{_datadir}/bash-completion/completions/ contrib/completions/bash/kubectl

# install config files
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}
install -m 644 -t %{buildroot}%{_sysconfdir}/%{name} contrib/init/systemd/environ/*

# install service files
install -d -m 0755 %{buildroot}%{_unitdir}
install -m 0644 -t %{buildroot}%{_unitdir} contrib/init/systemd/*.service

# install manpages
install -d %{buildroot}%{_mandir}/man1
install -p -m 644 docs/man/man1/* %{buildroot}%{_mandir}/man1

# install the place the kubelet defaults to put volumes
install -d %{buildroot}%{_sharedstatedir}/kubelet

# place contrib/init/systemd/tmpfiles.d/kubernetes.conf to /usr/lib/tmpfiles.d/kubernetes.conf
install -d -m 0755 %{buildroot}%{_tmpfilesdir}
install -p -m 0644 -t %{buildroot}/%{_tmpfilesdir} contrib/init/systemd/tmpfiles.d/kubernetes.conf

%if 0%{?with_debug}
# remove porter as it is built inside docker container without options for debug info
rm -rf contrib/for-tests/porter
%endif

%if 0%{?with_devel}
# install devel source codes
install -d %{buildroot}/%{gopath}/src/%{import_path}
for d in build cluster cmd contrib examples hack pkg plugin test; do
    cp -rpav $d %{buildroot}/%{gopath}/src/%{import_path}/
done
%endif

# place files for unit-test rpm
#install -d -m 0755 %{buildroot}%{_sharedstatedir}/kubernetes-unit-test/
#cp -pav README.md %{buildroot}%{_sharedstatedir}/kubernetes-unit-test/.
#for d in _output Godeps api cmd docs examples hack pkg plugin third_party test; do
#  cp -a $d %{buildroot}%{_sharedstatedir}/kubernetes-unit-test/
#done

%check
# Fedora, RHEL7 and CentOS are tested via unit-test subpackage
if [ 1 != 1 ]; then
echo "******Testing the commands*****"
hack/test-cmd.sh
echo "******Benchmarking kube********"
hack/benchmark-go.sh

# In Fedora 20 and RHEL7 the go cover tools isn't available correctly
%if 0%{?fedora} >= 21
echo "******Testing the go code******"
hack/test-go.sh
echo "******Testing integration******"
hack/test-integration.sh --use_go_build
%endif
fi

%files
# empty as it depends on master and node

%files master
%doc README.md LICENSE CONTRIB.md CONTRIBUTING.md DESIGN.md
%{_mandir}/man1/kube-apiserver.1*
%{_mandir}/man1/kube-controller-manager.1*
%{_mandir}/man1/kube-scheduler.1*
%attr(754, -, kube) %caps(cap_net_bind_service=ep) %{_bindir}/kube-apiserver
%{_bindir}/kube-controller-manager
%{_bindir}/kube-scheduler
#%{_bindir}/kube-version-change
%{_unitdir}/kube-apiserver.service
%{_unitdir}/kube-controller-manager.service
%{_unitdir}/kube-scheduler.service
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/apiserver
%config(noreplace) %{_sysconfdir}/%{name}/scheduler
%config(noreplace) %{_sysconfdir}/%{name}/config
%config(noreplace) %{_sysconfdir}/%{name}/controller-manager
%{_tmpfilesdir}/kubernetes.conf

%files node
%doc README.md LICENSE CONTRIB.md CONTRIBUTING.md DESIGN.md
%{_mandir}/man1/kubelet.1*
%{_mandir}/man1/kube-proxy.1*
%{_bindir}/kubelet
%{_bindir}/kube-proxy
#%{_bindir}/kube-version-change
%{_unitdir}/kube-proxy.service
%{_unitdir}/kubelet.service
%dir %{_sharedstatedir}/kubelet
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/config
%config(noreplace) %{_sysconfdir}/%{name}/kubelet
%config(noreplace) %{_sysconfdir}/%{name}/proxy
%{_tmpfilesdir}/kubernetes.conf

%files client
%doc README.md LICENSE CONTRIB.md CONTRIBUTING.md DESIGN.md
%{_mandir}/man1/kubectl.1*
%{_mandir}/man1/kubectl-*
%{_bindir}/kubectl
%{_datadir}/bash-completion/completions/kubectl

%files unit-test
#%{_sharedstatedir}/kubernetes-unit-test/

%if 0%{?with_devel}
%files devel
%doc README.md LICENSE CONTRIB.md CONTRIBUTING.md DESIGN.md
%dir %{gopath}/src/k8s.io
%{gopath}/src/%{import_path}
%endif

%pre master
getent group kube >/dev/null || groupadd -r kube
getent passwd kube >/dev/null || useradd -r -g kube -d / -s /sbin/nologin \
        -c "Kubernetes user" kube

%post master
%systemd_post kube-apiserver kube-scheduler kube-controller-manager

%preun master
%systemd_preun kube-apiserver kube-scheduler kube-controller-manager

%postun master
%systemd_postun


%pre node
getent group kube >/dev/null || groupadd -r kube
getent passwd kube >/dev/null || useradd -r -g kube -d / -s /sbin/nologin \
        -c "Kubernetes user" kube

%post node
%systemd_post kubelet kube-proxy

%preun node
%systemd_preun kubelet kube-proxy

%postun node
%systemd_postun

%changelog
