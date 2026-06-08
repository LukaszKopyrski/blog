
FROM node:20-alpine AS build

WORKDIR /app


COPY package*.json ./


RUN apk add --no-cache python3 g++ make


RUN npm install
COPY . .
RUN npm run build

RUN chown -R node:node /app/node_modules

FROM node:20-alpine

WORKDIR /app

COPY --from=build /app/package*.json ./
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist

RUN chown -R node:node /app

EXPOSE 8080


CMD ["npm", "run", "serve"]
