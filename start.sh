cd "$(dirname "$0")"

echo ---- Starting Backend
git pull
docker compose build
docker compose up -d
cd vue

npm install
npm run serve