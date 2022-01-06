#!/bin/bash -e

cd "$(dirname "$0")"

echo ---- Starting Backend
docker compose build
docker compose up -d
cd vue

npm install
npm run serve