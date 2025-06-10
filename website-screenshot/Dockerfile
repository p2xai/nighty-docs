# Simple Dockerfile to run the website screenshot app
FROM node:18-slim

# Install minimal dependencies for running Chromium
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libnss3 libatk1.0-0 libatk-bridge2.0-0 libx11-xcb1 \
        libxcomposite1 libxdamage1 libxrandr2 libxkbcommon0 \
        libgbm1 libasound2 libpangocairo-1.0-0 libpangoft2-1 \
        libdrm2 libgtk-3-0 ca-certificates fonts-liberation \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev
COPY screenshot.js ./

ENTRYPOINT ["node", "screenshot.js"]
CMD ["https://example.com", "screenshot.png"]
