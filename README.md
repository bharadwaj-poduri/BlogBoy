# BlogBoy

BlogBoy is a robust, Flask-powered blogging platform designed with a RESTful architecture. It features secure JWT-based authentication, a flexible blogging system with support for nested comments, and a seamless deployment workflow using Docker, Nginx, and Supervisor.

## 🚀 Key Features

- **User Management (UMS)**: Complete registration and login system with JWT authentication and token blacklisting.
- **Blogging System**: Create, update, and manage blog posts with ease.
- **Advanced Commenting**: Support for nested comments (threaded discussions) and blog-level commenting.
- **Engagement**: Like system for both blog posts and individual comments.
- **Scalable Architecture**: Integrated with Celery for asynchronous task management.
- **Containerized Deployment**: Ready for production with Docker, Docker Compose, Nginx, and Gunicorn.

## 🛠️ Technology Stack

- **Backend**: [Flask](https://flask.palletsprojects.com/) (1.1.1)
- **Database**: [PostgreSQL](https://www.postgresql.org/) with [SQLAlchemy](https://www.sqlalchemy.org/) ORM
- **Authentication**: [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- **API**: [Flask-RESTful](https://flask-restful.readthedocs.io/)
- **Task Queue**: [Celery](https://docs.celeryproject.org/)
- **Process Manager**: [Supervisor](http://supervisord.org/)
- **WSGI Server**: [Gunicorn](https://gunicorn.org/)
- **Reverse Proxy**: [Nginx](https://www.nginx.com/)
- **Deployment**: [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

## 📂 Project Structure

```text
BlogBoy/
├── BlogBoy/               # Main application directory
│   ├── Blogs/             # Blog and Comment logic (Models, Resources)
│   ├── UMS/               # User Management System (Auth, Users)
│   ├── Config/            # Application settings and server config
│   ├── migrations/        # Database migration files (Alembic)
│   ├── manage.py          # Management CLI script
│   └── requirements.txt   # Python dependencies
├── nginx/                 # Nginx configuration
├── docker-compose.yml     # Docker orchestration
└── README.md              # Project documentation
```

## 🏗️ Getting Started

### Prerequisites

- Python 3.5+
- Docker & Docker Compose (for containerized setup)
- PostgreSQL (if running locally without Docker)

### Local Setup (Development)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd BlogBoy/BlogBoy
   ```

2. **Create a virtual environment and install dependencies**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure the Database**:
   Update `Config/Settings/dev.py` with your PostgreSQL credentials.

4. **Run Migrations**:
   ```bash
   python manage.py db init
   python manage.py db migrate
   python manage.py db upgrade
   ```

5. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

### Running with Docker (Recommended)

The easiest way to run the full stack (Frontend, Backend, and Database) is using Docker Compose.

1. **Build and start the services**:
   ```bash
   docker-compose up --build
   ```

2. **Access the application**:
   - **Frontend**: [http://localhost](http://localhost) (Served by Nginx)
   - **API (Backend)**: [http://localhost/api](http://localhost/api) (Proxied via Frontend)
   - **Database**: PostgreSQL is running internally on port `5432`.

3. **Database Migrations (First Run)**:
   To initialize the database schema, run the following command while the containers are running:
   ```bash
   docker-compose exec BlogBoy python manage.py db upgrade
   ```

## 📡 API Endpoints

### Authentication (UMS)
- `POST /registration`: Register a new user.
- `POST /login`: Authenticate and receive JWT tokens.
- `POST /token/refresh`: Refresh expired access tokens.
- `POST /logout/access`: Revoke current access token.

### Blogs
- `GET/POST /blogresource`: List or create blog posts.
- `GET/POST /commentresource`: Fetch or add comments.
- `POST /likeresource`: Like a blog or comment.

## 📝 License

This project is licensed under the MIT License.
