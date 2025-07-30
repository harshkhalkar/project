# Flask + MySQL Docker App

This is a simple Flask application running inside Docker, connected to a MySQL database using Docker Compose. It exposes an API endpoint that returns a greeting message stored in the database.

---

## Project Structure

```bash
.
├── README.md
└── flask-sql
    ├── app
    │ ├── Dockerfile
    │ ├── app.py
    │ └── requirements.txt
    ├── docker-compose.yml
    └── init.sql
```

---

## How to Run

### Prerequisites:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Steps:

1. Open a terminal and navigate to the `flask-sql` directory:

   ```bash
   cd flask-sql
   ```
2. Start the application using Docker Compose:

   ```bash
   docker-compose up -d
   ```
3. Output of Application

   ```bash
   {
     "message": "Hello from Flask + MySQL!"
   }
   ```
---

## Docker Components

### Flask App (`flask-app`)
- Runs a Flask server on port `5000`.
- Connects to MySQL using `mysql-connector-python`.
- Code lives in `app/app.py`.

### MySQL Database (`db-sql`)
- Based on the official `mysql` image.
- Initializes with `init.sql` on first run.
- Data persists using a named volume `volume1sql`.

---

## Files Overview

- `app/app.py`: Main Flask application.
- `app/requirements.txt`: Python dependencies.
- `app/Dockerfile`: Builds the Flask app image.
- `docker-compose.yml`: Orchestrates both containers.
- `init.sql`: Initializes the `myapp` database and inserts one greeting row.

