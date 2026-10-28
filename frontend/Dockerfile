FROM node:20-alpine

WORKDIR /app

# Copy package configuration
COPY package*.json ./

# Install production dependencies
RUN npm install --omit=dev

# Copy application file
COPY server.js ./
COPY public ./public

ENV NODE_ENV=production
ENV PORT = 3000

EXPOSE 3000

CMD [ "npm" , "start" ]

