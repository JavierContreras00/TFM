from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    # Aquí harías la verificación del usuario en la base de datos
    # Esta es solo una simulación de autenticación
    if email == "usuario@ejemplo.com" and password == "1234":
        return jsonify({"success": True, "message": "Inicio de sesión exitoso"})
    return jsonify({"success": False, "message": "Credenciales incorrectas"})

@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    if password != confirm_password:
        return jsonify({"success": False, "message": "Las contraseñas no coinciden"})
    # Aquí registrarías al usuario en la base de datos
    return jsonify({"success": True, "message": "Registro exitoso"})