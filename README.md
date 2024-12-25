# Patent Infringement Checker

Prepared by Shijie Gan (shijiegan.gs@gmail.com).

## Overview

The **Patlytics Infringement Checker** is a web-based application designed to analyze patent claims and detect potential infringements efficiently.

## Features

- **Modern Tech Stack**: Built with a **React** frontend, **Flask** backend, and a **MongoDB** database. All components are containerized using **Docker** and orchestrated with **Docker Compose**.
- **AI-Powered Analysis**: Utilizes the OpenAI API with the pre-trained **GPT-4o-mini model** to perform patent claim analysis.
- **Flexible Deployment**: Can be run locally using Docker or accessed online (subject to hosting limitations).

## Running the Application

You can run the application locally using Docker Compose, referring to the setup instructions below.

Alternatively, access the hosted version at [https://patlytics-infringement-checker-frontend.onrender.com](https://patlytics-infringement-checker-frontend.onrender.com). Be aware that the hosted version may have a slightly longer loading time due to free hosting constraints.

> Note: The databases for the local and hosted versions are separate and do not share data.

## Setup Instructions

### 1. Prerequisites

Ensure the following tools are installed on your system:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: Usually included with Docker Desktop.

Verify the installations with:

```bash
docker --version
docker-compose --version
```

### 2. Navigate to the Project Directory

Replace `path/to/` with the directory where the project is located:

```bash
cd path/to/patlytics-infringement-checker
```

### 3. Build and Run the Application

Run the following command to build and start the application:

```bash
docker-compose up --build
```

> Note: The initial build process may take a few minutes as necessary images are downloaded and the application is compiled.

## Accessing the Application

After starting the application, use the following URLs to access its components:

- **Frontend (React):** [http://localhost:3000](http://localhost:3000)
- **Backend (Flask API):** [http://localhost:5000](http://localhost:5000)

## Stopping the Application

To stop the application and remove the containers, press `Ctrl+C` in the terminal where the `docker-compose` command is running.

## Troubleshooting

### 1. Docker Daemon Not Running

**Error Message:**

```plaintext
error during connect: This error may indicate that the docker daemon is not running.
```

**Solution:**

- Ensure Docker Desktop is installed and running.
- Restart Docker Desktop if needed.

### 2. Port Already in Use

**Error Message:**

```plaintext
Bind for 0.0.0.0:3000 failed: port is already allocated
```

**Solution:**

- A different application is using port `3000` or `5000`.
- Update the `ports` section in `docker-compose.yml` and adjust the `REACT_APP_API_URL` environment variable:

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

## Additional Information

### Project Purpose

This application was developed as a take-home assignment for Patlytics, showcasing AI-powered tools for patent analysis.

### OpenAI API Key

- The backend requires an OpenAI API key for functionality.
- The API key is included in the `.env` file for convenience. It should be kept secure and private.

## Contact

For questions, feedback, or support, feel free to reach out!

- **Name:** Shijie Gan
- **Email:** [shijiegan.gs@gmail.com](mailto:shijiegan.gs@gmail.com)
- **Phone/WhatsApp:** +6012-6383016
- **LinkedIn:** [Shijie Gan](https://www.linkedin.com/in/shijie-gan-968926197/)

## Thank You

Thank you for reviewing this project. I look forward to your feedback!
