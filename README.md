# TactfulTask
Implementing a simple REST API with basic CRUD and Authentication functionality using python flask.

# Clone Repo
git clone https://github.com/arknfel/Tactful.git

# Development Environment
```shell
$python3 -m venv venv
$source venv/bin/activate

$pip install -r requirements

$export FLASK_APP=app.py
# set FLASK_APP=app.py  # for Windows

$flask run
```
# Docker
To deploy environment, Docker is required on a host machine with 105 MB of free space

Change directory to the Dockerfile's directory

Building the image:
```shell
docker build -t api:1.0 .
```
output should look similar to:
```shell
[+] Building 17.4s (14/14) FINISHED
 => [internal] load build definition from Dockerfile                                         0.9s
 => => transferring dockerfile: 32B                                                          0.2s
 => [internal] load .dockerignore                                                            1.2s
 => => transferring context: 124B                                                            0.1s
 => [internal] load metadata for docker.io/library/python:3.6.6-alpine3.6                    2.4s
 => [internal] load build context                                                            0.4s
 => => transferring context: 2.79kB                                                          0.0s
 => [1/9] FROM docker.io/library/python:3.6.6-alpine3.6@sha256:79ece62efc421dda703ccae5ec23  0.0s
 => CACHED [2/9] RUN mkdir /code                                                             0.0s
 => CACHED [3/9] WORKDIR /code                                                               0.0s
 => CACHED [4/9] COPY requirements.txt /code/                                                0.0s
 => CACHED [5/9] RUN pip install -r requirements.txt                                         0.0s
 => [6/9] COPY . /code/                                                                      0.6s
 => [7/9] RUN flask db init && flask db migrate && flask db upgrade                          4.9s
 => [8/9] RUN python createadmin.py                                                          2.6s
 => [9/9] RUN rm createadmin.py                                                              1.6s
 => exporting to image                                                                       3.1s
 => => exporting layers                                                                      2.5s
 => => writing image sha256:414c7032b639300914fe3bbcc694f77a5060ef1175fa1d7bc52fe9c93e9e4c9  0.1s
 => => naming to docker.io/library/api:1.0
```
Run a new container:
```shell
docker run -it -p 5000:5000 api:1.0
```
output:
```shell
* Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: <some PIN number>
```

# Testing endpoints

```python
import requests, json
```
Admin login, acquire token
```python
url = "http://127.0.0.1:5000/login"
headers = {'Content-type': 'application/json'}
res = requests.get(url, auth=('Admin', '1234'))
token = res.json()['token']
headers = {'Content-type': 'application/json', 'x-access-token': token}
print(token)
```
output:
```python
eyJ0eXAiOiJKV1Qi....
```
Get users
```python
url = "http://127.0.0.1:5000/users"
headers = {'Content-type': 'application/json', 'x-access-token': token}
res = requests.get(url, headers=headers)
print(res.json())
admin_pid = res.json()['users'][0]['public_id']
print(admin_pid)
```
output:
```python
{'users': [{'date_joined': 'Mon, 16 Nov 2020 18:12:26 GMT', 'name': 'Admin', 'public_id': '808e2e58-ff64-47d4-8f17-a11811f6d03c'}]}
808e2e58-ff64-47d4-8f17-a11811f6d03c
```
Create user
```python
url = "http://127.0.0.1:5000/users"
data = json.dumps({"name": "dummy_user_1", "password": "1234"})
res = requests.post(url, data=data, headers=headers)
print(res.json())
pid1 = res.json()['user']['id']
print(pid)
```
output:
```python
{'message': 'Added new user - 2020-11-16 18:40:32.268215', 'user': {'id': 'cc07860c-b646-4fe2-9071-b8683c09adb6', 'name': 'dummy_user_1'}}
cc07860c-b646-4fe2-9071-b8683c09adb6
```
Update user
```python
# rename dummy_user_1 to User1
url = f"http://127.0.0.1:5000/users/{admin_pid}"
data = json.dumps({"name": "User1"})
res = requests.put(url, data=data, headers=headers)
print(res.json())
```
output:
```python
{'fields': {'name': 'User1'},
 'message': 'updated fileds for user cc07860c-b646-4fe2-9071-b8683c09adb6'}
```
Get User1 by public_id to validate the update
```python
url = f"http://127.0.0.1:5000/users/{pid1}"
res = requests.get(url, headers=headers)
print(res.json())
```
output:
```python
{'user': {'date_joined': 'Mon, 16 Nov 2020 18:40:32 GMT',
  'name': 'User1',
  'public_id': 'cc07860c-b646-4fe2-9071-b8683c09adb6'}}
```
Delete User1
```python
url = f"http://127.0.0.1:5000/users/{pid1}"
res = requests.delete(url, headers=headers)
print(res.json())

# Try to get deleted user

url = f"http://127.0.0.1:5000/users/{pid1}"
res = requests.get(url, headers=headers)
print(res.json())
```
output:
```python
{'message': 'deleted user cc07860c-b646-4fe2-9071-b8683c09adb6'}
{'message': 'not found'}
```
