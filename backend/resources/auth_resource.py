# login
# signup
# logout

from flask import Blueprint, request, jsonify, current_app as app
from flask_security import login_user, logout_user, current_user
from flask_security.utils import verify_and_update_password, hash_password
from backend.models import User
from backend.extensions import db




auth_bp = Blueprint( 'auth', __name__, url_prefix='/auth')
api_bp = Blueprint( 'api', __name__, url_prefix='/api')


@auth_bp.route('/login1', methods=['POST'])
def login():
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400


    user = app.datastore.find_user(email=email)
    

    if not user or not verify_and_update_password(password, user):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    # login_user(user)
    # logout_user(user)
    return jsonify({
        'message': 'Login successful',
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'token': user.get_auth_token()  
    }), 200    



@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    contact_number = data.get('contact_number')
    role = data.get('role')

    active = True

    # if patient then active true else False

    if not name or not email or not password or not role in ['patient', 'doctor']:
        return jsonify({'message': 'Name, email, and password are required'}), 400
    
    if role == "doctor":
        active = False

    existing_user = app.datastore.find_user(email=email)
    if existing_user:
        return jsonify({'message': 'User with this email already exists'}), 409


    # creatinng a user
    user = app.datastore.create_user(
        name=name,
        email=email,
        password=hash_password(password),
        contact_number=contact_number,
        role=role,
        active=active
    )
    try:
        db.session.commit()
    except:
        return {'message': 'Error'}, 405

    # assigning role to user
    role = app.datastore.find_role(role)
    user = app.datastore.find_user(email=email)
    app.datastore.add_role_to_user(user, role)
    try:
        db.session.commit()
    except:
        return {'message': 'Error'}, 405

    return jsonify({
        'message': 'User registered successfully', 
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'role': role.name

        }), 201


# @auth_bp.route("/users")
# def get_users():
#     role = request.args.get("doctor")
#     query = User.query
#     d = {}
#     if role:
#         query = query.filter_by(role=role)
#     users = query.all()
#     for user in users:
#         d[user.id] = {
#             "name": user.name,
#             "email": user.email,
#             "role": user.role
#         }
#     return jsonify(d), 200

# 