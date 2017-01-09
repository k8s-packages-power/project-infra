# etcd
### Prerequisite

Need following softwares installed before building it:

* Golang
* rpmdevtools package
* rpm-build package

### Build

```sh
Install the dependency:
# yum install libpcap-devel
# cd etcd
# ./build-ectd.sh
```

After the successful run build script, you should have rpms in etcd/rpmbuild/RPMS and etcd/rpmbuild/SRPMS folder
