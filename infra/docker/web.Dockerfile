# Multi-stage Dockerfile for EKCP React Web Frontend (Task 002)

# ==========================================
# Stage 1: Base Node setup
# ==========================================
FROM node:20-alpine AS base
WORKDIR /app

# ==========================================
# Stage 2: Install dependencies
# ==========================================
FROM base AS deps
COPY apps/web/package.json apps/web/package-lock.json* ./
RUN npm ci || npm install

# ==========================================
# Stage 3: Build static production assets
# ==========================================
FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY apps/web ./

ARG VITE_API_BASE_URL=http://localhost:8000/api/v1
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

RUN npm run build

# ==========================================
# Stage 4: Dev server runtime stage (target: dev)
# ==========================================
FROM base AS dev
ENV NODE_ENV=development \
    PORT=3000 \
    VITE_API_BASE_URL=http://localhost:8000/api/v1

RUN addgroup -g 10001 appgroup && \
    adduser -u 10001 -G appgroup -s /bin/sh -D appuser && \
    chown -R appuser:appgroup /app

COPY --from=deps --chown=appuser:appgroup /app/node_modules ./node_modules
COPY --chown=appuser:appgroup apps/web ./

USER appuser
EXPOSE 3000

CMD ["npx", "vite", "--host", "0.0.0.0", "--port", "3000"]

# ==========================================
# Stage 5: Production runner stage (default)
# ==========================================
FROM nginx:alpine AS runner

RUN addgroup -g 10001 appgroup && \
    adduser -u 10001 -G appgroup -s /bin/sh -D appuser

COPY infra/docker/nginx.conf /etc/nginx/nginx.conf
COPY --from=builder --chown=appuser:appgroup /app/dist /usr/share/nginx/html

RUN chown -R appuser:appgroup /usr/share/nginx/html /var/cache/nginx /var/log/nginx /etc/nginx /tmp

USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:3000/health || exit 1

CMD ["nginx", "-g", "daemon off;"]
