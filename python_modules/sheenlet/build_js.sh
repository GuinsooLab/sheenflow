#! /bin/bash
ROOT=$(git rev-parse --show-toplevel)
pushd "$ROOT/js_modules/sheenlet"
set -eux

yarn install
yarn build
