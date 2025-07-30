from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Clave secreta para JWT (cámbiala por algo seguro)
app.config["JWT_SECRET_KEY"] = "tu_clave_secreta_aqui"
jwt = JWTManager(app)

# Simulación base de datos usuarios (normalmente en BD real)
usuarios = {
    "usuario@example.com": generate_password_hash("123456")
}

# Ruta de login
@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not email or not password:
        return jsonify({"msg": "Faltan email o password"}), 400

    user_password_hash = usuarios.get(email, None)
    if user_password_hash and check_password_hash(user_password_hash, password):
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token)

    return jsonify({"msg": "Email o password incorrectos"}), 401

# Ruta protegida (requiere token válido)
@app.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == "__main__":
    app.run(debug=True)
