# Build stage
FROM ubuntu as build-stage

WORKDIR /code/ui

RUN apt-get update && apt-get install -y nodejs && apt-get install -y npm

RUN npm install -g @vue/cli @vue/cli-service @vue/cli-service-global

COPY package.json .
RUN npm install --quiet

COPY . .
RUN npm run build:staging
# RUN npm run serve

# # Production stage
# FROM nginx:1.16.1-alpine as production-stage
# COPY --from=build-stage /code/ui/dist /usr/share/nginx/html
# EXPOSE 80
# CMD [ "nginx", "-g", "daemon off;"]