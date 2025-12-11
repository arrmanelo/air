FROM node:20-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    make \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy package file (without lock to avoid npm bug with optional deps)
COPY package.json ./

# Install dependencies
RUN npm install --legacy-peer-deps --no-package-lock

# Copy ONLY locales first
COPY locales ./locales

# Copy the rest of the app
COPY . .

# === FIX: create /app/i18n/locales and copy locales there ===
RUN mkdir -p /app/i18n/locales \
    && cp -r ./locales/* /app/i18n/locales/ \
    || true

# Debug: show folder structure
RUN echo "=== /app ===" && ls -la /app || true
RUN echo "=== /app/locales ===" && ls -la /app/locales || true
RUN echo "=== /app/i18n/locales ===" && ls -la /app/i18n/locales || true

# Build the application
ENV NODE_ENV=production
RUN npm run build

# Expose port
EXPOSE 3000

# Start the application
CMD ["node", ".output/server/index.mjs"]
