FROM node:17-alpine

RUN apk add --no-cache libc6-compat git
WORKDIR /app

COPY docker/images/scripts/entrypoint.sh /bin/entrypoint.sh
RUN chmod +x /bin/entrypoint.sh

ENTRYPOINT ["/bin/sh", "/bin/entrypoint.sh"]

CMD ["yarn"]
