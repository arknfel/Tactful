import datetime as dt
import uuid
from functools import wraps

import jwt
from flask import request, make_response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db
from app.models import User



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            print(token)
        
        if not token:
            return jsonify({"message": 'missing token'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({"message": 'token is invalid'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

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
@token_required
def list_users(current_user):
    print(current_user.name, current_user.is_admin)
    if not current_user.is_admin:
        return jsonify({"message": "not allowed"})

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
@token_required
def get_user(current_user, public_id):

    if not current_user.is_admin:
        return jsonify({"message": "not allowed"})

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
@token_required
def create_user(current_user):

    if not current_user.is_admin:
        return jsonify({"message": "not allowed"})

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
@token_required
def update_user(current_user, public_id):

    if not current_user.is_admin:
        return jsonify({"message": "not allowed"})

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
@token_required
def delete_user(current_user, public_id):

    if not current_user.is_admin:
        return jsonify({"message": "not allowed"})

    user = User.query.filter_by(public_id=public_id).first()
    print(user)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"deleted user {user.public_id}"})
    return jsonify({"message": "not found"})


