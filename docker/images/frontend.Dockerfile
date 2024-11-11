FROM node:16-alpine AS deps
RUN apk add --no-cache libc6-compat git
WORKDIR /deps
COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./
RUN \
  if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm ci; \
  elif [ -f pnpm-lock.yaml ]; then yarn global add pnpm && pnpm i; \
  else echo "Lockfile not found." && exit 1; \
  fi


FROM node:16-alpine AS builder
WORKDIR /deps
COPY --from=deps /deps/node_modules ./node_modules

ENTRYPOINT ["/bin/sh", "/bin/entrypoint.sh"]
WORKDIR /app