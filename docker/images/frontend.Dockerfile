FROM node:16-alpine AS deps
RUN apk add --no-cache libc6-compat git
WORKDIR /deps

RUN mkdir /app/.yarn-global && mkdir app/.yarn-cache
ENV YARN_GLOBAL_FOLDER=/app/.yarn-global
ENV YARN_CACHE_FOLDER=/app/.yarn-cache

COPY frontend/package.json frontend/yarn.lock* frontend/package-lock.json* frontend/pnpm-lock.yaml* ./
RUN \
  if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm ci; \
  elif [ -f pnpm-lock.yaml ]; then yarn global add pnpm && pnpm i; \
  else echo "Lockfile not found." && exit 1; \
  fi


FROM node:16-alpine AS builder
WORKDIR /deps
COPY --from=deps /deps/node_modules ./node_modules

WORKDIR /app
ENTRYPOINT ["/bin/sh", "-c"]