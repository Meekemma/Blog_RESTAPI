# Blog API

## Project Overview
This is a Django REST Framework-based API for managing blog posts and comments with filtering, pagination, caching, and authentication.

## Installation

### 1. Clone the repository
```sh
$ git clone https://github.com/Meekemma/Blog_RESTAPI.git
$ cd blog_api
```

### 2. Create and activate a virtual environment
```sh
$ python -m venv env
$ source env/bin/activate  # On Windows use `env\Scripts\activate`
```

### 3. Install dependencies
```sh
$ pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the project root and add:
```sh
SECRET_KEY='your_secret_key_here'
DEBUG=True
ALLOWED_HOSTS=*
```
To generate a new secret key, you can use:
```sh
$ python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 5. Apply migrations
```sh
$ python manage.py migrate
```

### 6. Create a superuser
```sh
$ python manage.py createsuperuser
```

### 7. Run the development server
```sh
$ python manage.py runserver
```

## API Endpoints

- `GET /blog/posts/` - Fetch all published posts (supports filtering & pagination)
- `GET /blog/posts/<post_id>/` - Fetch details of a single post

## Caching Configuration
This project uses database caching. Ensure you have set up caching correctly:
```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache_table",
    }
}
```
To create the cache table:
```sh
$ python manage.py createcachetable
```

## Authentication
- JWT Authentication is required for protected endpoints.
- Include the `Authorization: Bearer <token>` header in requests.

## License
MIT

