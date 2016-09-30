#!/bin/bash

# sudo yum install rpm-build golang etcd -y
# sudo yum groupinstall "Development Tools" -y
# by default it builds the latest kubernetes version shown in git tag
# optionally you can specify ./build_latest_stable_kubernetes.sh v0.18.2

# Find the latest tagged stable release in the master branch, or use $1 tag

if [ $# -lt 1 ]
then
  echo "Usage: `basename "$0"` <kubernetes_path> [version]"
  exit 1
fi

# Remove existing kubernetes and contrib code.
rm -rf kubernetes;rm -rf contrib

echo "Copying kubernetes from \"$1\" to current directory..."
cp -r $1 .;cd kubernetes
echo "DONE"

if [ $# -eq 1 ]
  then
    latest_kubernetes_version=`git describe --tags|cut -c 2-`
  else
    if [ $2 = `git tag -l $2` ]
      then
        latest_kubernetes_version=`echo $2|cut -c 2-`
      else
        echo "That is not a valid kubernetes version tag."
        exit 1
    fi
fi
latest_stable_kubernetes_commit="`git rev-list v${latest_kubernetes_version}  | head -n 1`"
short_commit=`echo $latest_stable_kubernetes_commit | cut -c1-7`
cd ..;

# update the rpm spec file with the latest stable version and commit
version=$(echo ${latest_kubernetes_version} | cut -f1 -d-)
sub_version=$(echo ${latest_kubernetes_version} | cut -f2 -d- -s| sed -e 's/\.//g')

sed -i "s/^Version:.*/Version:        ${version}/" rpmbuild/SPECS/kubernetes.spec

if [ ! -z $sub_version ]; then
  sed -i "s/^Release:.*/Release:        1.${sub_version}.git%{shortcommit}%{?dist}/" rpmbuild/SPECS/kubernetes.spec
else
  sed -i "s/^Release:.*/Release:        1.git%{shortcommit}%{?dist}/" rpmbuild/SPECS/kubernetes.spec
fi

sed -i "s/^%global commit.*/%global commit          ${latest_stable_kubernetes_commit}/" rpmbuild/SPECS/kubernetes.spec
sed -i "s/^export KUBE_GIT_VERSION=.*/export KUBE_GIT_VERSION=${latest_kubernetes_version-${short_commit}}/" rpmbuild/SPECS/kubernetes.spec

# clean up any old builds. tar up the latest stable commit, and throw it into rpmbuild/SOURCES, and prepare for the build
cd kubernetes; git checkout $latest_stable_kubernetes_commit &> /dev/null; cd ..;
mkdir -p rpmbuild/SOURCES
rm -rf rpmbuild/BUILD rpmbuild/BUILDROOT rpmbuild/RPMS rpmbuild/SRPMS rpmbuild/SOURCES/kubernetes-*.tar.gz
tar -c kubernetes --transform s/kubernetes/kubernetes-$latest_stable_kubernetes_commit/ | gzip -9 &> "rpmbuild/SOURCES/kubernetes-${short_commit}.tar.gz"

git clone https://github.com/kubernetes/contrib.git
cd contrib
con_commit="`git rev-parse HEAD`"
con_short_commit=`echo $con_commit | cut -c1-7`
cd ..;

sed -i "s/^%global con_commit.*/%global con_commit          ${con_commit}/" rpmbuild/SPECS/kubernetes.spec
rm -rf rpmbuild/SOURCES/contrib-*.tar.gz
tar -c contrib --transform s/contrib/contrib-${con_commit}/ | gzip -9 &> "rpmbuild/SOURCES/contrib-${con_short_commit}.tar.gz"

# start compiling kubernetes
echo -e "Starting the compilation of kubernetes version: $latest_kubernetes_version \n\n\n"
rpmbuild -ba --define "_topdir `pwd`/rpmbuild" rpmbuild/SPECS/kubernetes.spec

if [ $? -eq 0 ]
then
  rpm_file=`ls rpmbuild/RPMS/*/kubernetes*`
  echo -e "\n\n\nFinished compiling kubernetes version: $latest_stable_kubernetes_version \nThe file is located here: ./$rpm_file"
else
  echo -e "\n\n\nKubernetes compilation failed.\n"
  exit 1
fi
