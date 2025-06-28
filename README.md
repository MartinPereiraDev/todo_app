# Todo APP with FastAPI

## Setup
1. Create virtual environment: `python -m venv venv`
2. Activate: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `uvicorn app.main:app --reload`

## Testing
`pytest --cov=app`

## Docker
`docker-compose up --build`
`docker build -t todo-app .`
`docker run -p 8000:8000 todo-app`
`docker-compose up -d`  # Run in detached mode

## docs http://localhost:8000/docs


## create users 
`http://localhost:8000/users/`
{
    "name": "Martin",
    "surname": "Gonzalez",
    "email": "martin@example.com",
    "role": "admin"
}