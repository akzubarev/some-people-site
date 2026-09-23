FROM node:22.23.2-bookworm-slim
RUN npm install --global pnpm@12.5.1
WORKDIR /app
RUN mkdir -p /pnpm && chown node:node /app /pnpm
COPY --chown=node:node frontend/package.json frontend/pnpm-lock.yaml frontend/pnpm-workspace.yaml ./
USER node
RUN pnpm install --frozen-lockfile --store-dir /pnpm
COPY --chown=node:node frontend/ ./
CMD ["pnpm", "dev"]
