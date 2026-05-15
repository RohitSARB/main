'''
Docstring for phaseFourPractiseFastAPI
'''

'''
Let’s go.
**Phase 4 = Backend Engineer → Production API thinking** 🔥
From here on, everything we write looks like **real company code**.

---

# 🧠 PHASE 4 — AUTH, SECURITY & PRODUCTION PATTERNS

### Goal

By the end of this phase you will:

* implement **JWT authentication**
* hash passwords securely
* protect routes using `Depends`
* paginate data
* run background tasks
* version APIs cleanly

This is **mandatory** for expert-level FastAPI.

---

## 1️⃣ Authentication Flow (Real World)

### How it works

1. User registers (email + password)
2. Password is **hashed**
3. User logs in
4. Server returns **JWT token**
5. Client sends token in headers
6. Protected routes verify token

---

## 2️⃣ Install Security Packages

```bash
pip install python-jose passlib[bcrypt] pydantic-settings
```

---

## 3️⃣ Password Hashing (security.py)

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)
```

Never store raw passwords. Ever.

---

## 4️⃣ JWT Token Logic (auth.py)

```python
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
```

---

## 5️⃣ User Schemas (schemas/user.py)

```python
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr
```

---

## 6️⃣ User Routes (routes/user.py)

```python
from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate
from app.security import hash_password, verify_password
from app.auth import create_access_token
from app.database import db

router = APIRouter(prefix="/users", tags=["Users"])
user_collection = db["users"]

@router.post("/register")
async def register_user(user: UserCreate):
    existing = await user_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed = hash_password(user.password)
    result = await user_collection.insert_one({
        "email": user.email,
        "password": hashed
    })

    return {"id": str(result.inserted_id), "email": user.email}

@router.post("/login")
async def login_user(user: UserCreate):
    db_user = await user_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
```

---

## 7️⃣ Protect Routes Using Depends (CORE SKILL)

### Token Dependency

```python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

---

### Protect Task Routes

```python
@router.get("/")
async def get_tasks(user: str = Depends(get_current_user)):
    return {"message": f"Tasks for {user}"}
```

---

## 8️⃣ Pagination (Production Requirement)

```python
@router.get("/")
async def list_tasks(skip: int = 0, limit: int = 10):
    tasks = []
    cursor = task_collection.find().skip(skip).limit(limit)
    async for doc in cursor:
        tasks.append(doc)
    return tasks
```

---

## 9️⃣ Background Tasks (Email, Logs, Jobs)

```python
from fastapi import BackgroundTasks

def send_email(email: str):
    print(f"Sending email to {email}")

@router.post("/register")
async def register(user: UserCreate, bg: BackgroundTasks):
    bg.add_task(send_email, user.email)
    return {"status": "user created"}
```

Runs **after response**.

---

## 🔟 API Versioning (Clean)

```python
app.include_router(user_router, prefix="/api/v1")
app.include_router(task_router, prefix="/api/v1")
```

---

## 1️⃣1️⃣ Logging (Minimal but Pro)

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("User registered")
```

---

# PHASE 4 MINI TASK (DO THIS)

Implement:

1. Protect `POST /tasks`
2. Only logged-in users can create tasks
3. Save `user_email` with each task

---

## 🏁 You Are Now “Backend-Ready”

You can:

* design APIs
* secure them
* scale them
* deploy them

What’s left is **polish + project**.

---

## FINAL STEP OPTIONS 🔥

Reply with ONE of these:

### 👉 **“Build Final Project”**

We’ll build:

* clean repo
* full API
* Mongo
* auth
* docs
* best practices

### 👉 **“Phase 5”**

Advanced topics:

* rate limiting
* caching (Redis)
* testing
* async workers
* deployment (Docker)

Your call.

'''

















'''
🔥 Let’s do it.
**Phase 5 = Senior Backend / Real-Production FastAPI**

From this phase onward, you’ll be writing code that **scales**, **survives traffic**, and **passes system design reviews**.

---

# 🧩 PHASE 5 — PERFORMANCE, TESTING, DEPLOYMENT

### Goal

By the end of this phase you will know how to:

* protect APIs from abuse (rate limiting)
* cache intelligently (Redis)
* write real tests
* structure services for scale
* deploy FastAPI properly (Docker mindset)

---

## 1️⃣ Rate Limiting (Protect Your API)

### Why it matters

Without rate limiting:

* bots
* scraping abuse
* DDoS
* cost explosion

---

### Install

```bash
pip install slowapi
```

---

### Rate Limiter Setup

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
```

---

### Apply to App

```python
from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

app = FastAPI()
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
```

---

### Protect Endpoint

```python
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

@app.get("/health")
@limiter.limit("5/minute")
async def health(request: Request):
    return {"status": "ok"}
```

---

## 2️⃣ Caching with Redis (Read Optimization)

### Why Redis

* fast reads
* session storage
* rate limiting backend
* caching DB results

---

### Install

```bash
pip install redis
```

---

### Redis Client

```python
import redis

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
```

---

### Cache Example

```python
@app.get("/tasks")
async def get_tasks():
    cached = redis_client.get("tasks")
    if cached:
        return {"source": "cache", "data": cached}

    tasks = ["task1", "task2"]
    redis_client.setex("tasks", 60, str(tasks))
    return {"source": "db", "data": tasks}
```

---

## 3️⃣ Testing with Pytest (MANDATORY)

### Install

```bash
pip install pytest httpx
```

---

### Test Client

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
```

---

### Test Auth Flow

```python
def test_register_and_login():
    r = client.post("/users/register", json={
        "email": "test@test.com",
        "password": "123456"
    })
    assert r.status_code == 200
```

---

## 4️⃣ Dependency Overrides (Testing Power Move)

```python
app.dependency_overrides[get_current_user] = lambda: "test@test.com"
```

This lets you test protected routes **without real auth**.

---

## 5️⃣ Background Workers (Advanced Pattern)

FastAPI ≠ heavy workers.

Use:

* Celery
* RQ
* Dramatiq

FastAPI = API layer
Workers = async jobs

(We’ll keep FastAPI clean.)

---

## 6️⃣ Dockerizing FastAPI (Production Setup)

### Dockerfile

```dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 7️⃣ Environment Config (.env)

```env
MONGO_URL=mongodb://mongo:27017
SECRET_KEY=prod-secret
```

Load with `pydantic-settings`.

---

## 8️⃣ Logging & Monitoring

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
```

Production systems live on logs.

---

## 9️⃣ Common Expert Mistakes (Avoid These)

❌ business logic inside routes
❌ no pagination
❌ no tests
❌ no auth
❌ blocking code in async routes

You’re past this level now.

---

# 🏁 FINAL MINI TASK (LAST CHECK)

Make sure your app has:

* auth protected routes
* pagination
* rate limiting
* caching
* tests
* Dockerfile

If yes → you’re **industry-ready**.

---

# 🚀 NEXT STEP (IMPORTANT)

Now you have **two powerful options**:

### 👉 **“Build Final Project”** (RECOMMENDED)

We’ll build a **full production FastAPI app** from scratch:

* repo structure
* API design
* Mongo
* auth
* tests
* Docker
* real-world use case

### 👉 **“Advanced System Design”**

We go beyond code:

* microservices
* API gateways
* scaling FastAPI
* async task queues
* scraping APIs at scale

Say the word 👇

'''