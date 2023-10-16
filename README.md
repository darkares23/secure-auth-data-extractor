# OPENID AND DATA EXTRACTION

This Django-React project is designed to provide an efficient, scalable, and extendable platform for user authentication through OpenID-based OAuth providers and data extraction from unstructured text.

## Key Features:
OpenID Authentication:

1. Employed an abstract factory pattern for the authentication system. This choice provides flexibility and scalability, ensuring easy integrations with more providers in the future, such as Facebook, LinkedIn, among others.
Utilizes Google as the primary authentication provider.
Data Extraction:

2. Incorporated the strategy pattern for data extraction, optimized for the identification and extraction of patterns that vary mainly in quantities and dates.
3. Utilizes regular expressions for precise data extraction, while considering other alternatives like Natural Language Processing.

4. Data Storage:
Models were established to store user information (like name and email) and extracted data.
The extracted data is stored in Base64 encoding for security. When retrieved through the endpoint, it's decoded for transparency.
Development & Deployment:

5. Used Docker for containerization, ensuring consistency between development and production environments.
6. Integrated an environment similar to production for development, using SSL locally. The script create_certs can be utilized to generate local SSL certificates for this purpose.
7. Frontend developed using React with Next.js and TypeScript for type safety and efficient rendering.
Code Quality:

8. Prioritized clean, reusable, and maintainable code.
9. Employed linters and formatters like Black, Rubocop, and Prettier to maintain code uniformity and best practices.

10. Nginx Configuration: A basic Nginx configuration is included (./nginx/default.conf). Nginx serves the Django application via the uwsgi protocol. For specific configurations, adjust the default.conf accordingly.


## Prerequisites

- Docker
- Docker Compose
- mkcert

## Setup

Install mkcert on your system. Please refer to the official documentation for installation instructions for your operating system.

- `sudo make create_certs` Is used to generate local certs for using ssl request locally, You need to install mkcert in order to run this command
- `make build`: Builds the Docker containers.
- `make migrate`: run migrations on db
- `make superuser`: Creates a Django superuser allowed to access the admin panel where you can visualize all character data and images.
- `make up`: Starts dockers containers

In this project, we use docker-compose to manage multiple services, each responsible for a specific part of the application. The services included are:

- web: This service runs the Django web application using the Gunicorn WSGI server. It serves the web interface and handles incoming requests from users.

- db: This service runs a PostgreSQL database server, which is responsible for storing the application data. Django interacts with the database server to perform CRUD (Create, Read, Update, Delete) operations on the character data.

- nginx: This service runs an Nginx web server, which acts as a reverse proxy for the Django web application. Nginx is responsible for handling incoming requests, serving static files, and forwarding requests to the Django application. It can also provide SSL termination for secure HTTPS connections.

## Usage

Navigate to the main application in your web browser. If running locally, it's typically:

`https://app.benny.com`

Use the application's features:

Authenticate using the integrated OpenID OAuth provider.
Extract data elements from provided unstructured text inputs.

The Django admin panel can be accessed at:

`https://app.benny.com/admin/`

## Nginx Configuration

The project includes a basic Nginx configuration file located at `./nginx/default.conf`. The Nginx container is set up to serve the Django application using the `uwsgi` protocol. To customize the Nginx configuration, modify the `default.conf` file as needed.

This project includes a local SSL/TLS certificate generation using mkcert to enable secure HTTPS connections during development. Mkcert is a simple tool for creating locally-trusted certificates that are recognized by your system and browsers, allowing you to develop and test your application with HTTPS locally.

To set up a local certificate using mkcert, follow these steps:

Install mkcert on your system. Please refer to the official documentation for installation instructions for your operating system.

## Makefile Commands

- `sudo make create_certs` Is used to generate local certs and add a cert to your local etc/host for app.benny.com for using ssl request locally, You need to install mkcert in order to run this command
- `make build`: Builds the Docker containers.
- `make up`: Starts the Docker containers.
- `make down`: Stops the Docker containers.
- `make makemigrations`: Creates the Django migrations files.
- `make migrate`: Applies the Django migrations.
- `make superuser`: Creates a Django superuser allowed to access the admin panel where you can visualize all character data and images.
- `make test`: Runs the Django test suite.
