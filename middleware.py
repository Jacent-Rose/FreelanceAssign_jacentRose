from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)

# Secret keys for signing JWTs (use environment variables in production)
SECRET_KEY = "your_secret_key"
REFRESH_SECRET_KEY = "your_refresh_secret_key"

# A simple in-memory "database" for users (replace with a real one)
users_db = {
    "user1": "password1",
    "user2": "password2"
}

# Function to generate access token
def generate_access_token(username):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    access_token = jwt.encode(
        {"sub": username, "exp": expiration_time}, SECRET_KEY, algorithm="HS256"
    )
    return access_token

# Function to generate refresh token
def generate_refresh_token(username):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=3)
    refresh_token = jwt.encode(
        {"sub": username, "exp": expiration_time}, REFRESH_SECRET_KEY, algorithm="HS256"
    )
    return refresh_token

# Function to verify and decode access token
def decode_access_token(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"leeway": 5})
        return decoded_token
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Function to verify and decode refresh token
def decode_refresh_token(token):
    try:
        decoded_token = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=["HS256"], options={"leeway": 5})
        return decoded_token
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Route to authenticate and generate tokens
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    if username in users_db and users_db[username] == password:
        access_token = generate_access_token(username)
        refresh_token = generate_refresh_token(username)
        return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Route to refresh access token using refresh token
@app.route('/refresh', methods=['POST'])
def refresh():
    refresh_token = request.json.get('refresh_token')
    
    decoded_refresh_token = decode_refresh_token(refresh_token)
    
    if decoded_refresh_token:
        username = decoded_refresh_token.get("sub")
        new_access_token = generate_access_token(username)
        return jsonify({"access_token": new_access_token}), 200
    else:
        return jsonify({"message": "Invalid or expired refresh token"}), 401

# Protected endpoint that requires access token
@app.route('/protected', methods=['GET'])
def protected():
    access_token = request.headers.get('Authorization')

    if access_token:
        # Remove the 'Bearer ' prefix
        access_token = access_token.split(" ")[1]
        
        decoded_access_token = decode_access_token(access_token)
        
        if decoded_access_token:
            return jsonify({"message": "This is a protected route!"}), 200
        else:
            return jsonify({"message": "Invalid or expired access token"}), 401
    else:
        return jsonify({"message": "Access token required"}), 403


if __name__ == '__main__':
    app.run(debug=True)
