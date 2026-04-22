# Ecommerce Django Project

Simple ecommerce project built with Django. The application includes product and category pages and can be connected to a MySQL database running in Docker.

## Features

- Product list and product detail pages
- Category list and category detail pages
- Product image support
- Django admin
- MySQL database with Docker Compose

## Project Structure

```text
ecommerce_project/
|-- ecommerce/
|   |-- manage.py
|   |-- db.sqlite3
|   |-- ecommerce/
|   |   |-- settings.py
|   |   |-- urls.py
|   |   `-- docker-compose.yaml
|   `-- products/
|       |-- models.py
|       |-- views.py
|       |-- urls.py
|       `-- templates/
|-- myenv/
`-- README.md
```

## Requirements

- Python 3
- Django
- Docker Desktop
- MySQL client driver for Python

## MySQL with Docker

The MySQL service is defined in [ecommerce/ecommerce/docker-compose.yaml](/c:/Users/dell/Desktop/DJANGO/ecommerce_project/ecommerce/ecommerce/docker-compose.yaml).

Start the database:

```powershell
cd ecommerce/ecommerce
docker compose up -d
```

Default database configuration:

- Database: `DB_ECOMMERCE`
- User: `root`
- Password: `root`
- Host: `127.0.0.1`
- Port: `3306`

## Django Database Settings

The Django project is configured to read database values from environment variables, with defaults matching the Docker MySQL setup in [ecommerce/ecommerce/settings.py](/c:/Users/dell/Desktop/DJANGO/ecommerce_project/ecommerce/ecommerce/settings.py:51).

Optional environment variables:

```powershell
$env:DB_NAME="DB_ECOMMERCE"
$env:DB_USER="root"
$env:DB_PASSWORD="root"
$env:DB_HOST="127.0.0.1"
$env:DB_PORT="3306"
```

## Installation

Move to the Django project directory:

```powershell
cd ecommerce
```

Install dependencies:

```powershell
pip install django mysqlclient pillow
```

If `mysqlclient` does not install on Windows, you can switch to `PyMySQL` instead.

## Run the Project

Apply migrations:

```powershell
python manage.py migrate
```

Start the development server:

```powershell
python manage.py runserver
```

Open in your browser:

```text
http://127.0.0.1:8000/
```

## Main App

The `products` app contains:

- `Category` model
- `Product` model
- Product listing and detail views
- Category listing and detail views

## Notes

- `db.sqlite3` is still present in the project, but the current Django configuration targets MySQL.
- Media files are stored in the `images/` directory.

## GitHub Push

If Git is installed on your machine, run these commands from the project root:

```powershell
git init
git add .
git commit -m "Add README and Docker MySQL setup"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

If the repository already exists locally, use:

```powershell
git add .
git commit -m "Add README"
git push
```
