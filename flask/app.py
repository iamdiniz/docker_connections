from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)
app.config["DEBUG"] = True

# Configurações do MySQL
DB_CONFIG = {
    "host": "mysql_api_container",  # Nome do contêiner MySQL
    "user": "root",
    "password": "",
    "database": "flaskdocker"
}

@app.route("/", methods=["GET"])
def index():
    try:
        # Conexão com o banco de dados
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        
        # Consultar dados de exemplo (tabela precisa existir)
        cursor.execute("SELECT * FROM users;")
        users = cursor.fetchall()
        
        # Fechar conexão
        cursor.close()
        connection.close()
        
        return jsonify({"users": users}), 200
    except mysql.connector.Error as e:
        return jsonify({"error": "Failed to connect to the database", "details": str(e)}), 500

@app.route("/add-user", methods=["POST"])
def add_user():
    try:
        # Conexão com o banco de dados
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Dados do corpo da requisição
        data = request.json
        name = data.get("name")
        email = data.get("email")
        
        # Inserir novo usuário
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        connection.commit()
        
        # Fechar conexão
        cursor.close()
        connection.close()
        
        return jsonify({"message": "User added successfully"}), 201
    except mysql.connector.Error as e:
        return jsonify({"error": "Failed to add user", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
