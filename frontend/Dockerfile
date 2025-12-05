# Multi-stage build for React frontend
FROM node:20-alpine as builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build application
RUN npm run build


# Production stage with nginx
FROM nginx:alpine

# Copy built files from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Create non-root user
RUN adduser -D -u 1000 monolith && \
    chown -R monolith:monolith /usr/share/nginx/html && \
    chown -R monolith:monolith /var/cache/nginx && \
    chown -R monolith:monolith /var/log/nginx && \
    touch /var/run/nginx.pid && \
    chown -R monolith:monolith /var/run/nginx.pid

USER monolith

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
