# Step 1 — Build Angular
FROM node:18-alpine AS build

WORKDIR /app

# Copy package files first (better caching)
COPY package*.json ./

RUN npm install

# Copy full Angular project
COPY . .

# Build Angular in production mode
RUN npm run build --prod


# Step 2 — Serve using Nginx
FROM nginx:alpine

# Remove default Nginx site
RUN rm -rf /usr/share/nginx/html/*

# Copy Angular dist output
COPY --from=build /app/dist/sop-django-ui /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]