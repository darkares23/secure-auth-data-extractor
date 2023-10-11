# Use an official Node runtime as the parent image
FROM node:18-slim

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy the current directory contents into the container
COPY . .

# Build the Next.js app
RUN npm run build

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Define the command to run the app using the Next.js CLI
CMD ["npm", "start"]
