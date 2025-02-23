# News Aggregator - Containerized Web Application

## Overview

This project is a **containerized web application** designed to fetch and display the latest news articles related to the **Super Bowl 2025**. The system consists of multiple services running inside **Docker containers**:

- **FastAPI Backend** (`web`): Fetches news and serves them via REST API.
- **Celery Worker** (`worker`): Processes background tasks like fetching news.
- **Celery Beat** (`celery_beat`): Schedules periodic news-fetching tasks.
- **Redis** (`redis`): Acts as a message broker for Celery.
- **MongoDB** (`mongo`): Stores news articles.
- **Celery Flower** (`monitor`): Provides a UI to monitor Celery tasks.
- **Vite React Frontend** (`vite-react`): Displays the latest news.

## Setup Instructions

### **1. Clone the Repository**

```sh
git clone https://github.com/vikas-bhat-d/news-app.git
```

### **2. Build and Start the Containers**

```sh
docker-compose up --build
```

This will start all services defined in `docker-compose.yml`.

### **3. Verify Running Containers**

```sh
docker ps
```

Ensure all containers (`web`, `worker`, `celery_beat`, `monitor`, `redis`, `mongo`, `vite-react`) are running.

### **4. Access the Application**

- **Backend API (FastAPI):** `http://localhost:5001`
- **Celery Flower UI:** `http://localhost:5555`
- **Frontend (React App):** `http://localhost:5173`

---

## API Endpoints

### **FastAPI Backend**

| Method | Endpoint         | Description                        |
| ------ | ---------------- | ---------------------------------- |
| `GET`  | `/news?limit=10` | Fetch latest news (limit optional) |
| `GET`  | `/fetch_news`    | Manually trigger news fetching     |
| `GET`  | `/health_check`  | Check API health                   |

---

## Managing Services

### **Stop All Containers**

```sh
docker-compose down
```

### **Restart Specific Service**

```sh
docker-compose up --build <service-name>
```

Example:

```sh
docker-compose up --build worker
```

---

## Logs & Debugging

### **Check Logs for Backend**

```sh
docker logs web -f
```

### **Check Celery Worker Logs**

```sh
docker logs worker -f
```

### **Check MongoDB Data**

```sh
docker exec -it mongo_db mongosh
use news_db
show collections
```

---
