# InkDrop

A full-stack blogging platform built with Django. Supports post creation, editing, search, and user authentication — with a responsive Bootstrap frontend.

## Features

- User authentication (register / login / logout)
- Create, edit, and delete blog posts
- Search across posts
- Responsive UI with Bootstrap

## Tech Stack

| Layer     | Technology                       |
|-----------|----------------------------------|
| Backend   | Python, Django                   |
| Frontend  | HTML, CSS, JavaScript, Bootstrap |
| Database  | SQLite                           |
| Auth      | Django built-in auth             |

## Project Structure

```
InkDrop/
├── blog/              # Core app (models, views, URLs)
├── blog_project/      # Project settings and root URLs
├── templates/         # HTML templates
├── covers/            # Cover images
├── manage.py
├── requirements.txt
└── README.md
```

## Getting Started

```bash
git clone https://github.com/samiksha-2702/InkDrop.git
cd InkDrop

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Visit `http://127.0.0.1:8000`

## License

MIT