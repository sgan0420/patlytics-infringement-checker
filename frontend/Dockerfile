# Use an official Node.js image to build the React app
FROM node:16

# Build-time variable
ARG REACT_APP_API_URL

# Set environment variable for the build
ENV REACT_APP_API_URL=${REACT_APP_API_URL}

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json for dependency installation
COPY package*.json ./

# Install React dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the React app for production
RUN npm run build

# Install serve to serve the production build
RUN npm install -g serve

# Expose the port React will run on
EXPOSE 3000

# Start the React app
CMD ["serve", "-s", "build", "-l", "3000"]
