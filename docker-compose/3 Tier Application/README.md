# 3-Tier Web Application using Docker Compose (PHP, MySQL, Nginx)

This project sets up a simple 3-tier architecture using Docker Compose:
- **MySQL** as the database
- **PHP-FPM** as the backend application layer
- **Nginx** as the web server

The application allows users to submit a form which is stored in a MySQL database.

---

## Project Structure
```bash
.
├── 3arch
│   ├── app
│   │ └── code              ############################################################
│   │ ├── submit.php        # PHP script to handle form submissions and insert into DB #
│   │ └── test.php          # Optional test PHP script                                 #
│   ├── db                  
│   │ ├── Dockerfile        # Builds a MySQL image with preloaded schema               #
│   │ └── init.sql          # SQL script to initialize the 'info' DB and 'users' table #
│   ├── web
│   │ ├── code
│   │ │ ├── form.html       # Simple HTML form to collect user input                   #
│   │ │ └── index.html      # Landing page                                             #
│   │ └── config
│   │ └── default.conf      # Custom Nginx configuration                               #
│   └── docker-compose.yml  # Orchestrates all services                                #
└── README.md               # Project documentation (this file)                        #
```
---

## How It Works

### Database (MySQL)
- Built using a custom `Dockerfile`.
- Initializes a database called `info` and creates a table `users` using `init.sql`.
- Exposes default MySQL port `3306`.

### Application (PHP-FPM)
- Uses the Bitnami `php-fpm` image.
- Mounts the PHP source code from `/app/code/`.
- Handles form submissions and inserts data into MySQL.

### Web Server (Nginx)
- Uses the official Nginx image.
- Serves the HTML files and proxies `.php` requests to PHP-FPM.
- Configured via `default.conf`.
