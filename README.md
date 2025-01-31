# Hakkaten Server

This is a simple FastAPI backend project. Just follow these steps to get it up and running!

## 🚀 What it does
- User login/logout
- JWT authentication
- Database with SQLAlchemy (SQLite by default)
- Auto-generated API docs (`/docs`)

## 🛠 What you need
- Python 3.9+
- PostgreSQL or SQLite (or just stick with SQLite for now)
- `pip` (Python package manager)
- Git

## 📦 How to set it up
### 1️⃣ Clone the repo
```bash
git clone https://github.com/yourusername/Hakkaten-server.git
cd Hakkaten-server
```

### 2️⃣ Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

## 🔑 Setting up the environment
Make a `.env` file and add:
```ini
DATABASE_URL=sqlite:///./test.db  # Change to PostgreSQL if needed
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 📂 Setting up the database
### 1️⃣ Run migrations
```bash
alembic upgrade head
```

### 2️⃣ (Optional) Reset the database
```bash
rm test.db  # Only for SQLite
alembic upgrade head
```

## 🚀 Run the server
```bash
uvicorn main:app --reload
```
Check it out at:
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc UI:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 📝 Some useful API endpoints
### Auth
- `POST /api/v1/register` - Sign up
- `POST /api/v1/login` - Get a token

### Users
- `GET /api/v1/users/me` - Get your profile

## 🐞 Troubleshooting
- `.env` file missing? Make sure it exists.
- Virtual environment not active? Run `source venv/bin/activate`.
- Database issues? Try `alembic upgrade head`.

## 🛠 For development
### 1️⃣ Run with auto-reload
```bash
uvicorn main:app --reload
```
### 2️⃣ Running in production (if needed)
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

## 🤝 Contributing (if you care)
1. Fork it
2. Make a branch (`git checkout -b my-branch`)
3. Commit stuff (`git commit -m 'some changes'`)
4. Push it (`git push origin my-branch`)
5. Open a PR

## 📧 Need help?
Just ping me or drop a message in the group chat!

