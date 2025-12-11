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

# Install dependencies with clean cache
RUN npm install --legacy-peer-deps --no-package-lock

# Copy application code
COPY . .

# Build the application
ENV NODE_ENV=production
RUN npm run build

# Expose port
EXPOSE 3000

# Start the application
CMD ["node", ".output/server/index.mjs"]
