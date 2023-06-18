
# Commands

```bash
virtualenv -p python3 env
source env/bin/activate

pip install -r requirements.txt

python3 app.py

## Docker
docker build -t www . ; docker run -p 8080:8080 www
```

## Git
```bash
git clone https://github.com/deuxexmakina/sharearide.git
git fetch --all
git reset --hard origin/master
```

## Curl
```bash
curl -X POST -H "Content-Type: application/json" -d '{"email":"admin@ron.com","password":"password123"}' http://localhost:5000/login
curl -X POST -H "Content-Type: application/json" -d '{"email": "1@ronwork.com"}' http://127.0.0.1:5000/add_email

curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NzEwMTU4OSwianRpIjoiNjI1NDBkOTItNmE4ZS00MDc3LWJjMTctN2JkZDIwZGUxZjk1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluQHJvbi5jb20iLCJuYmYiOjE2ODcxMDE1ODksImV4cCI6MTY4NzEwMjQ4OX0.JU2mF5RicLrEbZfxgqQvC5k8pW_cHk17JiJza70H600" -d '{"email": "1@ronwork.com"}' http://127.0.0.1:5000/add_email

```