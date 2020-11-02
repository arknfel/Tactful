import os
import datetime as dt
import uuid
import jwt
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


##############################################################
# CONFIGURATIONS, Initializing Flask app ##################### 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data.sqlite')
app.config['SECRET_KEY'] = 'just-forget-it'

db = SQLAlchemy(app)

##############################################################
# MODELS #####################################################
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    date_joined = db.Column(db.DateTime())
    is_admin = db.Column(db.Boolean)


class Course(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer())

##############################################################
# ROUTES #####################################################
@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not varify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})
    
    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not varify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})
    
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp': dt.datetime.utcnow() + dt.timedelta(minutes=60)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('utf-8')})
    
    return make_response('Could not varify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})


@app.route('/users', methods=['GET'])
def list_users():
    return jsonify({
        "users": [
            {
                'public_id': user.public_id,
                'name': user.name,
                'date_joined': user.date_joined
            } for user in User.query.all()
        ]
    })


# get user by public_id
@app.route('/users/<public_id>', methods=['GET'])
def get_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    # return user data, if user exists
    if user:
        return jsonify({
            "user": {
                "public_id": user.public_id,
                "name": user.name,
                "date_joined": user.date_joined
            }
        })
    
    # notify if user is None
    return jsonify({"message": "not found"})


# create new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    # init user object
    user = User(
        public_id=str(uuid.uuid4()),  # populated by system
        name=data['name'],  # populated from payload 
        password=generate_password_hash(data['password'], method='sha256'),  # populated from payload
        date_joined=dt.datetime.utcnow(),  # populated by system
        is_admin=False  # default
    )

    # creating new user, commiting changes to Database
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": f"Added new user - {user.date_joined}",
        "user": {
            "id": f"{user.public_id}",
            "name": f"{user.name}"
        }
    })


# update an existing user, by public_id
@app.route('/users/<public_id>', methods=['PUT'])
def update_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if user:  # if query returns a user object
        updated_fields = {}
        data = request.get_json()

        # update only fields that are relevant to user object
        for attribute in data:
            if attribute in user.__dict__:
                setattr(user, attribute, data[attribute])
                updated_fields.update({attribute: data[attribute]})
        
        # commiting updates to Database
        db.session.commit()
        
        # notify which fields were updated
        return jsonify({
            "message": f"updated fileds for user {public_id}",
            "fields": updated_fields
        })
    
    # notify if user is None
    return jsonify({"message": "not found"})


# delete user by public_id
@app.route('/users/<public_id>', methods=['DELETE'])
def delete_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    print(user)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"deleted user {user.public_id}"})
    return jsonify({"message": "not found"})


##############################################################
# MAIN THREAD
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')