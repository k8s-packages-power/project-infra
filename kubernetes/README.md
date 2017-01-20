
1. $ sudo yum install rpm-build
2. $ sudo yum groupinstall "Development Tools" -y
3. Install golang
4. $ export GOPATH=~/k8s_ws
5. $ mkdir -p $GOPATH
6. $ export PATH=$GOPATH/bin:$PATH
7. $ go get -u github.com/jteeuwen/go-bindata/go-bindata
8. $ go get github.com/cpuguy83/go-md2man
9. $ ./build_k8s.sh <kubernetes source path>  # Kubernetes source path is git cloned code with target release checked out
