#!/bin/bash

# docker pull grammatech/ddisasm:latest

docker run -v $PWD/bindump:/bindump -it grammatech/ddisasm:latest ls
docker ps
# pwd