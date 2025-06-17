# How to run the project

This repository contains a Django web application configured to run with Docker containers.

## Prerequisites

Before you begin, ensure you have the following installed:
- Docker - [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose - [Install Docker Compose](https://docs.docker.com/compose/install/)
- Git 

### 1. Clone the repository
git clone https://github.com/V-tasya/HappyData.git
cd your-repo

### 2. Build and start containers
docker-compose up --build

### 3. In a new terminal apply database migrations
docker-compose exec web python manage.py migrate

### 4. Access the application
Web application: http://localhost:8000
