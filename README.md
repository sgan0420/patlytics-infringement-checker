# Patlytics Infringement Checker

## Overview

The **Patlytics Infringement Checker** is a web application that helps users analyze and detect potential patent infringements. It consists of a **Flask** backend and a **React** frontend, both containerized using Docker and orchestrated with Docker Compose.

## Prerequisites

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: Included with Docker Desktop installation.
- Verify by running `docker --version` and `docker-compose --version`

## Setup Instructions

1. **Navigate to the Project Directory**

   ```bash
   cd path/to/patlytics-infringement-checker
   ```

   Replace `path/to/` with the actual path where you extracted the project.

2. **Build and Run the Application**

   ```bash
   docker-compose up --build
   ```

   Note: The first time you run this command, it may take several minutes as Docker downloads necessary images and builds the application.

## Accessing the Application

Once the application is running, you can access it through your web browser:

- **Frontend (React Application):** [http://localhost:3000](http://localhost:3000)
- **Backend (Flask API):** [http://localhost:5000](http://localhost:5000)

## Stopping the Application

To stop the application and remove the containers, press `Ctrl+C` in the terminal where `docker-compose` is running.

## Troubleshooting

### Common Issues

1. **Docker Daemon Not Running**

   **Error Message:**

   ```
   error during connect: This error may indicate that the docker daemon is not running.
   ```

   **Solution:**

   - Ensure that Docker Desktop is installed and running.
   - Restart Docker Desktop if necessary.

2. **Port Already in Use**

   **Error Message:**

   ```
   Bind for 0.0.0.0:3000 failed: port is already allocated
   ```

   **Solution:**

   - Another application is using port `3000` or `5000`.
   - Modify the `ports` section in `docker-compose.yml` to use different ports.

     ```yaml
     services:
       frontend:
         ports:
           - "3001:3000"
       backend:
         ports:
           - "5001:5000"
     ```

   - Update `REACT_APP_API_URL` in the `args` field accordingly:

     ```env
     REACT_APP_API_URL=http://localhost:5001
     ```

## Notes

- This project is for the use of take home assignment of Patlytics.
- The openai api key is included in the .env file for the purpose of this assignment. It should be kept securely.

## Thank you

Thank you for the opportunity to work on this project. I look forward to hearing your feedback.

For questions or issues, please contact:

- **Name:** Shijie Gan
- **Email:** shijiegan.gs@gmail.com
