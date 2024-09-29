FROM node:20-alpine

WORKDIR /app

COPY package.json .
COPY package-lock.json .

RUN npm install -g parcel
RUN npm install

COPY . .

EXPOSE 3001

CMD ["npm", "run", "start"]