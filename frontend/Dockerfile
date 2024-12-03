FROM node:20-slim

WORKDIR /app

COPY package.json /app/package.json

RUN npm install

COPY . .

EXPOSE 3000

RUN npm run build

CMD ["npm", "run","build"]
