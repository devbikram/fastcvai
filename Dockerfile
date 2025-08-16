# Multi-stage Docker build for Frontend + Python FastAPI Backend
FROM node:18-alpine AS frontend-base
RUN apk add --no-cache libc6-compat
WORKDIR /app/frontend

# Stage 1: Build Frontend (Next.js)
FROM frontend-base AS frontend-deps
COPY frontend/package*.json ./
RUN npm ci --only=production

FROM frontend-base AS frontend-builder
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
ENV NEXT_TELEMETRY_DISABLED 1
RUN npm run build

# Stage 2: Python Backend Base
FROM python:3.11-alpine AS backend-base
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev \
    tesseract-ocr \
    tesseract-ocr-data-eng \
    poppler-utils
WORKDIR /app/backend

# Stage 3: Build Backend (FastAPI)
FROM backend-base AS backend-builder
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Stage 4: Production Runtime with nginx
FROM python:3.11-alpine AS runner
WORKDIR /app

# Install runtime dependencies
RUN apk add --no-cache \
    nginx \
    supervisor \
    tesseract-ocr \
    tesseract-ocr-data-eng \
    poppler-utils

# Create application user
RUN addgroup --system --gid 1001 appgroup
RUN adduser --system --uid 1001 appuser

# Copy built frontend
COPY --from=frontend-builder --chown=appuser:appgroup /app/frontend/.next/standalone ./frontend/
COPY --from=frontend-builder --chown=appuser:appgroup /app/frontend/.next/static ./frontend/.next/static
COPY --from=frontend-builder --chown=appuser:appgroup /app/frontend/public ./frontend/public

# Copy Python backend
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin
COPY --chown=appuser:appgroup backend/ ./backend/

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy supervisor configuration
COPY supervisord.conf /etc/supervisord.conf

# Create necessary directories and set permissions
RUN mkdir -p /var/log/supervisor /var/log/nginx /var/cache/nginx /var/run/nginx /tmp/uploads
RUN chown -R appuser:appgroup /var/log/supervisor /var/log/nginx /var/cache/nginx /var/run/nginx /etc/nginx /tmp/uploads

# Set environment variables
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PYTHONPATH=/app/backend
ENV PORT=8080

# Expose port
EXPOSE 8080

# Use supervisor to run both services
USER appuser
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
