# Node.js + MongoDB Dockerized App

This is a simple full-stack application demonstrating how to use **Node.js**, **Express**, and **MongoDB**, all containerized using **Docker** and managed via **Docker Compose**.

When you access the root route `/`, it creates a new user named `"harsh"` in the MongoDB database and responds with a JSON message confirming the addition.

---

## Project Structure

```bash
nodejs-mongodb/
├── app/
│ ├── Dockerfile
│ ├── app.js
│ └── package.json
├── docker-compose.yml
└── README.md
```

---

## How to Run

### 1. Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### 2. Start the Application

```bash
docker-compose up -d
```
This will:

- Start a MongoDB container named mongo-db

- Build and start a Node.js app container named node-js

- Create a Docker network (node-mongo) to allow communication between containers

- Create a persistent volume (mongodb) to store MongoDB data even after container restarts

Access the App
Expected response:
```bash
{
  "message": "User added!",
  "user": {
    "_id": "some-id",
    "name": "harsh",
    "__v": 0
  }
}
```
Included Technologies
- Node.js with Express

- MongoDB with Mongoose

- Docker and Docker Compose
