%if 0%{?fedora}
%global with_devel 1
%global with_bundled 1
%global with_debug 1
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
%global provider        github
%global provider_tld    com
%global project	        kubernetes
%global repo            kubernetes
# https://github.com/kubernetes/kubernetes
%global provider_prefix	%{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     k8s.io/kubernetes
%global commit          92b4f971662de9d8770f8dcd2ee01ec226a6f6c0
%global shortcommit	%(c=%{commit}; echo ${c:0:7})

%global con_provider        github
%global con_provider_tld    com
%global con_project         kubernetes
%global con_repo            contrib
# https://github.com/kubernetes/contrib
%global con_provider_prefix %{con_provider}.%{con_provider_tld}/%{con_project}/%{con_repo}
%global con_commit          6a097f6ad2c9ae396cc208b6ea6065e524bdc240
%global con_shortcommit %(c=%{con_commit}; echo ${c:0:7})

%global kube_version	1.4.7
%global kube_git_version      v%{kube_version}

#I really need this, otherwise "version_ldflags=$(kube::version_ldflags)"
# does not work
%global _buildshell	/bin/bash
%global _checkshell	/bin/bash

Name:		kubernetes
Version:	%{kube_version}
Release:        1.git%{shortcommit}%{?dist}
Summary:        Container cluster management
License:        ASL 2.0
URL:            %{import_path}
ExclusiveArch:  x86_64 aarch64 ppc64le
Source0:        kubernetes-%{shortcommit}.tar.gz
Source1:        https://%{provider}.%{provider_tld}/%{project}/%{con_repo}/archive/%{con_commit}/%{con_repo}-%{con_shortcommit}.tar.gz
Source2:        genmanpages.sh
Source3:        kubernetes-accounting.conf

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
BuildArch:      noarch

Provides: golang(%{import_path}/cmd/genutils) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/kube-apiserver/app) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/kube-apiserver/app/options) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/kube-controller-manager/app) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/kube-controller-manager/app/options) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/kube-proxy/app) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/kube-proxy/app/options) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/kubectl/app) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/kubelet/app) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/kubelet/app/options) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/libs/go2idl/args) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/libs/go2idl/client-gen/args) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/libs/go2idl/client-gen/generators) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/libs/go2idl/client-gen/generators/fake) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/libs/go2idl/client-gen/generators/normalization) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/libs/go2idl/client-gen/test_apis/testgroup.k8s.io) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/libs/go2idl/client-gen/test_apis/testgroup.k8s.io/install) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/libs/go2idl/client-gen/test_apis/testgroup.k8s.io/v1) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/libs/go2idl/client-gen/testoutput/clientset_generated/test_internalclientset) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/libs/go2idl/client-gen/testoutput/clientset_generated/test_internalclientset/fake) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/libs/go2idl/client-gen/testoutput/clientset_generated/test_internalclientset/typed/testgroup.k8s.io/unversioned) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/libs/go2idl/client-gen/testoutput/clientset_generated/test_internalclientset/typed/testgroup.k8s.io/unversioned/fake) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/libs/go2idl/conversion-gen/generators) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/libs/go2idl/deepcopy-gen/generators) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/libs/go2idl/generator) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/libs/go2idl/go-to-protobuf/protobuf) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/libs/go2idl/import-boss/generators) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/libs/go2idl/namer) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/libs/go2idl/parser) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/libs/go2idl/set-gen/generators) = %{version}-%{release}
Provides: golang(%{import_path}/cmd/libs/go2idl/types) = %{version}-%{release}
Provides: golang(%{import_path}/federation/apis/federation) = %{version}-%{release}
Provides: golang(%{import_path}/federation/apis/federation/install) = %{version}-%{release}
Provides: golang(%{import_path}/federation/apis/federation/v1beta1) = %{version}-%{release}
Provides: golang(%{import_path}/federation/client/clientset_generated/federation_internalclientset) = %{version}-%{release}
Provides: golang(%{import_path}/federation/client/clientset_generated/federation_internalclientset/fake) = %{version}-%{release}
Provides: golang(%{import_path}/federation/client/clientset_generated/federation_internalclientset/typed/core/unversioned) = %{version}-%{release}
Provides: golang(%{import_path}/federation/client/clientset_generated/federation_internalclientset/typed/core/unversioned/fake) = %{version}-%{release}
Provides: golang(%{import_path}/federation/client/clientset_generated/federation_internalclientset/typed/extensions/unversioned) = %{version}-%{release}
Provides: golang(%{import_path}/federation/client/clientset_generated/federation_internalclientset/typed/extensions/unversioned/fake) = %{version}-%{release}
Provides: golang(%{import_path}/federation/client/clientset_generated/federation_internalclientset/typed/federation/unversioned) = %{version}-%{release}
Provides: golang(%{import_path}/federation/client/clientset_generated/federation_internalclientset/typed/federation/unversioned/fake) = %{version}-%{release}
Provides: golang(%{import_path}/federation/client/clientset_generated/federation_release_1_3) = %{version}-%{release}
Provides: golang(%{import_path}/federation/client/clientset_generated/federation_release_1_3/fake) = %{version}-%{release}
Provides: golang(%{import_path}/federation/client/clientset_generated/federation_release_1_3/typed/core/v1) = %{version}-%{release}
Provides: golang(%{import_path}/federation/client/clientset_generated/federation_release_1_3/typed/core/v1/fake) = %{version}-%{release}
Provides: golang(%{import_path}/federation/client/clientset_generated/federation_release_1_3/typed/federation/v1beta1) = %{version}-%{release}
Provides: golang(%{import_path}/federation/client/clientset_generated/federation_release_1_3/typed/federation/v1beta1/fake) = %{version}-%{release}
Provides: golang(%{import_path}/federation/client/clientset_generated/federation_release_1_4) = %{version}-%{release}
Provides: golang(%{import_path}/federation/client/clientset_generated/federation_release_1_4/fake) = %{version}-%{release}
Provides: golang(%{import_path}/federation/client/clientset_generated/federation_release_1_4/typed/core/v1) = %{version}-%{release}
Provides: golang(%{import_path}/federation/client/clientset_generated/federation_release_1_4/typed/core/v1/fake) = %{version}-%{release}
Provides: golang(%{import_path}/federation/client/clientset_generated/federation_release_1_4/typed/extensions/v1beta1) = %{version}-%{release}
Provides: golang(%{import_path}/federation/client/clientset_generated/federation_release_1_4/typed/extensions/v1beta1/fake) = %{version}-%{release}
Provides: golang(%{import_path}/federation/client/clientset_generated/federation_release_1_4/typed/federation/v1beta1) = %{version}-%{release}
Provides: golang(%{import_path}/federation/client/clientset_generated/federation_release_1_4/typed/federation/v1beta1/fake) = %{version}-%{release}
Provides: golang(%{import_path}/federation/pkg/federation-controller/util) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/admission) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/annotations) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/endpoints) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/errors) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/errors/storage) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/install) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/meta) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/meta/metatypes) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/pod) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/resource) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/rest) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/rest/resttest) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/service) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/testapi) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/testing) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/testing/compat) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/unversioned) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/unversioned/validation) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/util) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/v1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/api/validation) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apimachinery) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apimachinery/registered) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/abac) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/abac/latest) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/abac/v0) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/abac/v1beta1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/apps) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/apps/install) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/apps/v1alpha1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/apps/validation) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/authentication) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/authentication/install) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/authentication/v1beta1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/authorization) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/authorization/install) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/authorization/v1beta1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/authorization/validation) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/autoscaling) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/autoscaling/install) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/autoscaling/v1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/autoscaling/validation) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/batch) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/batch/install) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/batch/v1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/batch/v2alpha1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/batch/validation) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/certificates) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/certificates/install) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/certificates/v1alpha1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/certificates/validation) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/componentconfig) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/componentconfig/install) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/componentconfig/v1alpha1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/extensions) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/extensions/install) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/extensions/v1beta1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/extensions/validation) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/imagepolicy) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/imagepolicy/install) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/imagepolicy/v1alpha1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/policy) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/policy/install) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/policy/v1alpha1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/policy/validation) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/rbac) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/rbac/install) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/rbac/v1alpha1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/rbac/validation) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/storage) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/storage/install) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/storage/v1beta1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apis/storage/validation) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apiserver) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apiserver/audit) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apiserver/authenticator) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apiserver/metrics) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/apiserver/testing) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/auth/authenticator) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/auth/authenticator/bearertoken) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/auth/authorizer) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/auth/authorizer/abac) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/auth/authorizer/union) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/auth/handlers) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/auth/user) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/capabilities) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/cache) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/chaosclient) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/internalclientset) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/internalclientset/fake) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/internalclientset/typed/authentication/unversioned) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/internalclientset/typed/authentication/unversioned/fake) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/internalclientset/typed/authorization/unversioned) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/internalclientset/typed/authorization/unversioned/fake) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/internalclientset/typed/autoscaling/unversioned) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/internalclientset/typed/autoscaling/unversioned/fake) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/internalclientset/typed/batch/unversioned) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/internalclientset/typed/batch/unversioned/fake) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/internalclientset/typed/certificates/unversioned) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/internalclientset/typed/certificates/unversioned/fake) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/internalclientset/typed/core/unversioned) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/internalclientset/typed/core/unversioned/fake) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/internalclientset/typed/extensions/unversioned) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/internalclientset/typed/extensions/unversioned/fake) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/internalclientset/typed/rbac/unversioned) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/internalclientset/typed/rbac/unversioned/fake) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/internalclientset/typed/storage/unversioned) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/internalclientset/typed/storage/unversioned/fake) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_2) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_2/fake) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_2/typed/core/v1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_2/typed/core/v1/fake) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_2/typed/extensions/v1beta1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_2/typed/extensions/v1beta1/fake) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_3) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_3/fake) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_3/typed/autoscaling/v1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_3/typed/autoscaling/v1/fake) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_3/typed/batch/v1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_3/typed/batch/v1/fake) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_3/typed/core/v1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_3/typed/core/v1/fake) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_3/typed/extensions/v1beta1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_3/typed/extensions/v1beta1/fake) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_4) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_4/fake) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_4/typed/authorization/v1beta1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_4/typed/authorization/v1beta1/fake) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_4/typed/autoscaling/v1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_4/typed/autoscaling/v1/fake) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_4/typed/batch/v1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_4/typed/batch/v1/fake) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_4/typed/core/v1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_4/typed/core/v1/fake) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_4/typed/extensions/v1beta1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_4/typed/extensions/v1beta1/fake) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_4/typed/policy/v1alpha1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/clientset_generated/release_1_4/typed/policy/v1alpha1/fake) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/leaderelection) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/metrics) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/metrics/prometheus) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/record) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/restclient) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/testing/core) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/transport) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/typed/discovery) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/typed/discovery/fake) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/typed/dynamic) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/unversioned) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/unversioned/adapters/internalclientset) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/unversioned/auth) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/unversioned/clientcmd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/unversioned/clientcmd/api) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/unversioned/clientcmd/api/latest) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/unversioned/clientcmd/api/v1) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/unversioned/fake) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/unversioned/portforward) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/unversioned/remotecommand) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/unversioned/testclient) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/client/unversioned/testclient/simple) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/cloudprovider) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/cloudprovider/providers) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/cloudprovider/providers/aws) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/cloudprovider/providers/azure) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/cloudprovider/providers/cloudstack) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/cloudprovider/providers/fake) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/cloudprovider/providers/gce) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/cloudprovider/providers/mesos) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/cloudprovider/providers/openstack) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/cloudprovider/providers/ovirt) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/cloudprovider/providers/rackspace) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/cloudprovider/providers/vsphere) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/certificates) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/daemon) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/deployment) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/deployment/util) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/disruption) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/endpoint) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/framework) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/framework/informers) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/garbagecollector) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/garbagecollector/metaonly) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/job) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/namespace) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/node) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/petset) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/podautoscaler) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/podautoscaler/metrics) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/podgc) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/replicaset) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/replicaset/options) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/replication) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/resourcequota) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/route) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/scheduledjob) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/service) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/serviceaccount) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/volume/attachdetach) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/volume/attachdetach/cache) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/volume/attachdetach/populator) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/volume/attachdetach/reconciler) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/volume/attachdetach/statusupdater) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/volume/attachdetach/testing) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/volume/persistentvolume) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/controller/volume/persistentvolume/options) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/conversion) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/conversion/queryparams) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/credentialprovider) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/credentialprovider/aws) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/credentialprovider/gcp) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/dns) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/fieldpath) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/fields) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/genericapiserver) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/genericapiserver/authorizer) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/genericapiserver/openapi) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/genericapiserver/options) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/genericapiserver/validation) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/healthz) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/httplog) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/hyperkube) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubectl) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubectl/cmd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubectl/cmd/config) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubectl/cmd/rollout) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubectl/cmd/set) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubectl/cmd/templates) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubectl/cmd/util) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubectl/cmd/util/editor) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubectl/cmd/util/jsonmerge) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubectl/metricsutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubectl/resource) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubectl/testing) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/api) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/api/testing) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/api/v1alpha1/runtime) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/api/v1alpha1/stats) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/cadvisor) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/cadvisor/testing) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/client) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/cm) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/config) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/container) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/container/testing) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/custommetrics) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/dockershim) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/dockertools) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/envvars) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/events) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/eviction) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/images) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/kuberuntime) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/leaky) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/lifecycle) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/metrics) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/network) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/network/cni) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/network/cni/testing) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/network/exec) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/network/hairpin) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/network/hostport) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/network/hostport/testing) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/network/kubenet) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/network/mock_network) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/network/testing) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/pleg) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/pod) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/pod/testing) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/prober) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/prober/results) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/prober/testing) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/qos) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/remote) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/rkt) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/rkt/mock_os) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/rktshim) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/server) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/server/portforward) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/server/remotecommand) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/server/stats) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/status) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/sysctl) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/types) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/util) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/util/cache) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/util/format) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/util/ioutils) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/util/queue) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/util/sliceutils) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/volumemanager) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/volumemanager/cache) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/volumemanager/populator) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubelet/volumemanager/reconciler) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/kubemark) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/labels) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/master) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/master/ports) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/metrics) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/probe) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/probe/exec) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/probe/http) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/probe/tcp) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/proxy) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/proxy/config) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/proxy/healthcheck) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/proxy/iptables) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/proxy/userspace) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/quota) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/quota/evaluator/core) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/quota/generic) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/quota/install) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/authorization/subjectaccessreview) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/authorization/util) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/cachesize) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/certificates) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/certificates/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/clusterrole) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/clusterrole/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/clusterrole/policybased) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/clusterrolebinding) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/clusterrolebinding/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/clusterrolebinding/policybased) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/componentstatus) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/configmap) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/configmap/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/controller) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/controller/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/daemonset) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/daemonset/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/deployment) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/deployment/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/endpoint) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/endpoint/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/event) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/event/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/experimental/controller/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/generic) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/generic/registry) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/generic/rest) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/horizontalpodautoscaler) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/horizontalpodautoscaler/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/ingress) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/ingress/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/job) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/job/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/limitrange) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/limitrange/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/namespace) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/namespace/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/networkpolicy) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/networkpolicy/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/node) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/node/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/node/rest) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/persistentvolume) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/persistentvolume/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/persistentvolumeclaim) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/persistentvolumeclaim/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/petset) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/petset/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/pod) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/pod/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/pod/rest) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/poddisruptionbudget) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/poddisruptionbudget/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/podsecuritypolicy) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/podsecuritypolicy/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/podtemplate) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/podtemplate/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/rangeallocation) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/registrytest) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/replicaset) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/replicaset/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/resourcequota) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/resourcequota/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/role) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/role/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/role/policybased) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/rolebinding) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/rolebinding/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/rolebinding/policybased) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/scheduledjob) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/scheduledjob/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/secret) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/secret/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/securitycontextconstraints) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/securitycontextconstraints/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/service) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/service/allocator) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/service/allocator/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/service/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/service/ipallocator) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/service/ipallocator/controller) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/service/ipallocator/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/service/portallocator) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/service/portallocator/controller) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/serviceaccount) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/serviceaccount/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/storageclass) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/storageclass/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/thirdpartyresource) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/thirdpartyresource/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/thirdpartyresourcedata) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/thirdpartyresourcedata/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/registry/tokenreview) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/runtime) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/runtime/serializer) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/runtime/serializer/json) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/runtime/serializer/protobuf) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/runtime/serializer/recognizer) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/runtime/serializer/streaming) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/runtime/serializer/versioning) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/runtime/serializer/yaml) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/security) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/security/apparmor) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/security/podsecuritypolicy) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/security/podsecuritypolicy/apparmor) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/security/podsecuritypolicy/capabilities) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/security/podsecuritypolicy/group) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/security/podsecuritypolicy/selinux) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/security/podsecuritypolicy/sysctl) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/security/podsecuritypolicy/user) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/security/podsecuritypolicy/util) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/securitycontext) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/securitycontextconstraints) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/securitycontextconstraints/capabilities) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/securitycontextconstraints/group) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/securitycontextconstraints/seccomp) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/securitycontextconstraints/selinux) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/securitycontextconstraints/user) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/securitycontextconstraints/util) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/selection) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/serviceaccount) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/ssh) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/storage) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/storage/etcd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/storage/etcd/etcdtest) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/storage/etcd/metrics) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/storage/etcd/testing) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/storage/etcd/testing/testingcert) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/storage/etcd/util) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/storage/etcd3) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/storage/storagebackend) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/storage/storagebackend/factory) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/storage/testing) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/types) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/ui) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/async) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/bandwidth) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/cache) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/certificates) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/chmod) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/chown) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/clock) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/codeinspector) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/config) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/configz) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/crlf) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/crypto) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/dbus) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/diff) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/ebtables) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/env) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/errors) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/exec) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/flag) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/flock) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/flowcontrol) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/flushwriter) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/framer) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/goroutinemap) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/goroutinemap/exponentialbackoff) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/hash) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/homedir) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/httpstream) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/httpstream/spdy) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/integer) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/interrupt) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/intstr) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/io) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/iptables) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/iptables/testing) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/json) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/jsonpath) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/keymutex) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/labels) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/limitwriter) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/logs) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/maps) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/metrics) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/mount) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/net) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/net/sets) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/node) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/oom) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/parsers) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/pod) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/procfs) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/proxy) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/rand) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/replicaset) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/resourcecontainer) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/rlimit) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/runtime) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/selinux) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/sets) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/sets/types) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/slice) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/strategicpatch) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/strings) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/sysctl) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/sysctl/testing) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/system) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/term) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/testing) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/threading) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/uuid) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/validation) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/validation/field) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/wait) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/workqueue) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/wsstream) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/util/yaml) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/version) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/version/prometheus) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/version/verflag) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/aws_ebs) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/azure_dd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/azure_file) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/cephfs) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/cinder) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/configmap) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/downwardapi) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/empty_dir) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/fc) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/flexvolume) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/flocker) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/gce_pd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/git_repo) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/glusterfs) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/host_path) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/iscsi) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/nfs) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/quobyte) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/rbd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/secret) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/testing) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/util) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/util/nestedpendingoperations) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/util/operationexecutor) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/util/types) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/util/volumehelper) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/volume/vsphere_volume) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/watch) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/watch/json) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/watch/versioned) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/cmd/kube-scheduler/app) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/cmd/kube-scheduler/app/options) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/admission/admit) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/admission/alwayspullimages) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/admission/antiaffinity) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/admission/deny) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/admission/exec) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/admission/imagepolicy) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/admission/initialresources) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/admission/limitranger) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/admission/namespace/autoprovision) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/admission/namespace/exists) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/admission/namespace/lifecycle) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/admission/persistentvolume/label) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/admission/resourcequota) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/admission/security) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/admission/security/podsecuritypolicy) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/admission/securitycontext/scdeny) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/admission/serviceaccount) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/admission/storageclass/default) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/auth) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/auth/authenticator) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/auth/authenticator/password) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/auth/authenticator/password/allow) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/auth/authenticator/password/keystone) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/auth/authenticator/password/passwordfile) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/auth/authenticator/request/basicauth) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/auth/authenticator/request/union) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/auth/authenticator/request/x509) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/auth/authenticator/token/oidc) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/auth/authenticator/token/oidc/testing) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/auth/authenticator/token/tokenfile) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/auth/authenticator/token/tokentest) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/auth/authenticator/token/webhook) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/auth/authorizer) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/auth/authorizer/rbac) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/auth/authorizer/webhook) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/client/auth) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/client/auth/gcp) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/client/auth/oidc) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/scheduler) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/scheduler/algorithm) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/scheduler/algorithm/predicates) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/scheduler/algorithm/priorities) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/scheduler/algorithm/priorities/util) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/scheduler/algorithmprovider) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/scheduler/algorithmprovider/defaults) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/scheduler/api) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/scheduler/api/latest) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/scheduler/api/v1) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/scheduler/api/validation) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/scheduler/factory) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/scheduler/metrics) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/scheduler/schedulercache) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/scheduler/testing) = %{version}-%{release}
Provides: golang(%{import_path}/plugin/pkg/webhook) = %{version}-%{release}

%description devel
Libraries for building packages importing k8s.io/kubernetes.
Currently, the devel is not suitable for development.
It is meant only as a buildtime dependency for other projects.

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
#BuildRequires: go-bindata

Requires(pre): shadow-utils
Requires: kubernetes-client = %{version}-%{release}

# if node is installed with node, version and release must be the same
Conflicts: kubernetes-node < %{version}-%{release}
Conflicts: kubernetes-node > %{version}-%{release}

%description master
Kubernetes services for master host

%package node
Summary: Kubernetes services for node host

Requires: docker
#Requires: conntrack-tools

#BuildRequires: golang >= 1.2-7
BuildRequires: systemd
BuildRequires: rsync
#BuildRequires: go-md2man
#BuildRequires: go-bindata

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
#BuildRequires: go-bindata

%description client
Kubernetes client tools like kubectl

%prep
%setup -q -n %{con_repo}-%{con_commit} -T -b 1
%setup -q -n %{repo}-%{commit}

# copy contrib folder
cp -r ../%{con_repo}-%{con_commit}/init contrib/.

# Move all the code under src/k8s.io/kubernetes directory
mkdir -p src/k8s.io/kubernetes
mv $(ls | grep -v "^src$") src/k8s.io/kubernetes/.

%build
pushd src/k8s.io/kubernetes/
export KUBE_GIT_TREE_STATE="clean"
export KUBE_GIT_COMMIT=%{commit}
export KUBE_GIT_VERSION=1.4.7
export KUBE_EXTRA_GOPATH=$(pwd)/Godeps/_workspace

%ifarch ppc64le
make all GOLDFLAGS="-linkmode external" KUBE_BUILD_PPC64LE=y
%else
make all
%endif

# generate the documents - both md files and man pages
hack/generate-docs.sh

# convert md to man
pushd docs
pushd admin
cp kube-apiserver.md kube-controller-manager.md kube-proxy.md kube-scheduler.md kubelet.md ..
popd
cp %{SOURCE2} genmanpages.sh
bash genmanpages.sh
popd
popd

%install
pushd src/k8s.io/kubernetes/
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
mkdir -p %{buildroot}/run
install -d -m 0755 %{buildroot}/run/%{name}/

# enable CPU and Memory accounting
install -d -m 0755 %{buildroot}/%{_sysconfdir}/systemd/system.conf.d
install -p -m 0644 -t %{buildroot}/%{_sysconfdir}/systemd/system.conf.d %{SOURCE3}

# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done
%endif

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif

popd

%if 0%{?with_devel}
mv src/k8s.io/kubernetes/devel.file-list .
%endif

mv src/k8s.io/kubernetes/*.md .
mv src/k8s.io/kubernetes/LICENSE .


# place files for unit-test rpm
install -d -m 0755 %{buildroot}%{_sharedstatedir}/kubernetes-unit-test/
# basically, everything from the root directory is needed
# unit-tests needs source code
# integration tests needs docs and other files
# test-cmd.sh atm needs cluster, examples and other
cp -a src %{buildroot}%{_sharedstatedir}/kubernetes-unit-test/
rm -rf %{buildroot}%{_sharedstatedir}/kubernetes-unit-test/src/k8s.io/kubernetes/_output
cp -a *.md %{buildroot}%{_sharedstatedir}/kubernetes-unit-test/src/k8s.io/kubernetes/

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

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
# empty as it depends on master and node

%files master
%license LICENSE
%doc *.md
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
%verify(not size mtime md5) %attr(755, kube,kube) %dir /run/%{name}

%files node
%license LICENSE
%doc *.md
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
%config(noreplace) %{_sysconfdir}/systemd/system.conf.d/kubernetes-accounting.conf
%{_tmpfilesdir}/kubernetes.conf
%verify(not size mtime md5) %attr(755, kube,kube) %dir /run/%{name}

%files client
%license LICENSE
%doc *.md
%{_mandir}/man1/kubectl.1*
%{_mandir}/man1/kubectl-*
%{_bindir}/kubectl
%{_datadir}/bash-completion/completions/kubectl

%files unit-test
%{_sharedstatedir}/kubernetes-unit-test/

%if 0%{?with_devel}
%files devel -f devel.file-list
%doc *.md
%dir %{gopath}/src/k8s.io
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
# If accounting is not currently enabled systemd reexec
if [[ `systemctl show docker kubelet | grep -q -e CPUAccounting=no -e MemoryAccounting=no; echo $?` -eq 0 ]]; then
  systemctl daemon-reexec
fi

%preun node
%systemd_preun kubelet kube-proxy

%postun node
%systemd_postun

%changelog
