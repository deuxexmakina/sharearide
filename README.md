
# Commands

```bash
virtualenv -p python3 env
source env/bin/activate

pip install -r requirements.txt

python3 app.py

### Docker
docker build -t www . ; docker run -p 8080:8080 www
```