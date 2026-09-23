FROM node:22-alpine AS builder

WORKDIR /app

COPY frontend/package.json frontend/yarn.lock ./
# Vue CLI's transitive node-ipc package has stale engine metadata capped at
# Node 17. It is build-time-only; keep a supported Node and ignore that check.
RUN yarn install --frozen-lockfile --non-interactive --ignore-engines

COPY frontend/ ./
RUN yarn build && mv dist_tmp dist

FROM nginx:1.28-alpine
COPY docker/nginx/oci.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html
