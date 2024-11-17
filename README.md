# Patlytics Infringement Checker

## Overview

The **Patlytics Infringement Checker** is a web application that helps users analyze and detect potential patent infringements. It consists of a **Flask** backend and a **React** frontend, both containerized using Docker and orchestrated with Docker Compose.

## Prerequisites

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: Included with Docker Desktop installation.
- Verify installation by running:

  ```bash
  docker --version
  docker-compose --version
  ```

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

   **Note:** The first time you run this command, it may take several minutes as Docker downloads necessary images and builds the application.

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
   - Modify the `ports` section and `REACT_APP_API_URL` argument in `docker-compose.yml` to use different ports.

     ```yaml
     services:
       backend:
         ports:
           - "5001:5000"
       frontend:
         build:
           context: ./frontend
           args:
             REACT_APP_API_URL: http://localhost:5001
         ports:
           - "3001:3000"
     ```

## Notes

- **Project Purpose:**
  - This project is developed as a take-home assignment for Patlytics.
- **OpenAI API Key:**
  - The OpenAI API key is required for the backend to function.
  - The API key should be kept secure and should not be shared publicly.
  - For the purpose of this assignment, the API key is included in the `.env` file, but ensure it's kept confidential.

## Thank You

Thank you for the opportunity to work on this project. I look forward to hearing your feedback.

For questions or issues, please contact:

- **Name:** Shijie Gan
- **Email:** shijiegan.gs@gmail.com
- **Phone/WhatsApp:** +6012-6383016
- **LinkedIn:** [Shijie Gan](https://www.linkedin.com/in/shijie-gan-968926197/)