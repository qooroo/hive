#!/bin/bash
set -euo pipefail

build="<% args.build %>"
image="<% image.hive %>:<% version.hive.major %>.<% version.hive.minor %>"

docker push ${image}
docker push ${image}.${build}
