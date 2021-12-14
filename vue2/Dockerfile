# Build stage
FROM node:16-alpine as builder

WORKDIR /app

COPY . .
# install node modules and build assets
RUN npm install && npm run build:production

# nginx state for serving content
FROM nginx:alpine
# Set working directory to nginx asset directory
WORKDIR /usr/share/nginx/html
# Remove default nginx static assets
RUN rm -rf ./*
# Copy static assets from builder stage
COPY --from=builder /app/dist .
# Containers run nginx with global directives and daemon off
ENTRYPOINT ["nginx", "-g", "daemon off;"]
