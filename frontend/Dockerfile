FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy app code
COPY . .

# Expose port
EXPOSE 5173

# Environment
ENV VITE_API_URL=http://localhost:8000

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
