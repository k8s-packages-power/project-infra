#!/bin/bash

rm -rf rpmbuild
mkdir -p rpmbuild/SOURCES
mkdir -p rpmbuild/SPECS

cp etcd.spec rpmbuild/SPECS

for source_file in `spectool -l etcd.spec | cut -d : -f 2- | sed -e 's/^[[:space:]]*//'`; do
  if [[ $source_file =~ ^http.* ]];
  then
    spectool -g -A --directory rpmbuild/SOURCES etcd.spec
  else
    cp $source_file rpmbuild/SOURCES
  fi
done

rpmbuild -ba --define "_topdir `pwd`/rpmbuild" rpmbuild/SPECS/etcd.spec
