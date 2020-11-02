# TactfulTask
Implementing a simple REST API with basic CRUD and Authentication functionality using python flask.

# Clone Repo
git clone https://github.com/arknfel/TactfulTask.git

# Development Environment
python3 -m venv venv
source venv/bin/activate

pip install -r requirements

export FLASK_APP=app.py (Linux)
set FLASK_APP=app.py (Windows)

flask run

# Testing endpoints

```python
import requests, json

# List users

url = "http://127.0.0.1:5000/users"
headers = {'Content-type': 'application/json'}
res = requests.get(url)
res.json()

# Get user

url = "http://127.0.0.1:5000/users/593a188a-c745-44c5-84c5-a51edfeac1bb"
headers = {'Content-type': 'application/json'}
res = requests.get(url)
res.json()

# Create user

url = "http://127.0.0.1:5000/users"
headers = {'Content-type': 'application/json'}
data = json.dumps({"name": "Yuri", "password": "sa"})
res = requests.post(url, data=data, headers=headers)
res.json()

# Update user

url = "http://127.0.0.1:5000/users/f90dc198-a7cf-4262-bd88-7085ada770ed"
headers = {'Content-type': 'application/json'}
data = json.dumps({"name": "Mosty", "is_admin": True})
res = requests.put(url, data=data, headers=headers)
res.json()

# Delete user

url = "http://127.0.0.1:5000/users/593a188a-c745-44c5-84c5-a51edfeac1bb"
res = requests.delete(url)
res.json()
```
