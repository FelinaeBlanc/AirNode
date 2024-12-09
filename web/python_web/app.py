from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)
DATABASE = '/home/lennea/sqlite/xbee_data.db'  # Remplacez par le chemin de votre base de données

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Récupère les données sous forme de dictionnaires
    return conn

# Route pour rendre la page HTML
@app.route('/')
def index():
    return render_template('index.html')  # Rendu de la page HTML

# API pour obtenir les noeuds
@app.route('/nodes', methods=['GET'])
def get_nodes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM AirNode")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in rows])  # Convertit chaque ligne en dictionnaire pour JSON

# API pour obtenir les données de capteurs
@app.route('/data', methods=['GET'])
def get_data():
    node_ids = request.args.getlist('node_ids')
    conn = get_db_connection()
    cursor = conn.cursor()
    if node_ids:
        query = "SELECT * FROM AirNodeData WHERE node_id IN ({})".format(','.join('?' * len(node_ids)))
        cursor.execute(query, node_ids)
    else:
        cursor.execute("SELECT * FROM AirNodeData")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in rows])  # Convertit chaque ligne en dictionnaire pour JSON

# API pour mettre à jour le nom d'un noeud
@app.route('/nodes/<int:node_id>', methods=['PUT'])
def update_node_name(node_id):
    new_name = request.json.get('name')
    if not new_name:
        return jsonify({"error": "Name is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE AirNode SET name = ? WHERE id = ?", (new_name, node_id))
    conn.commit()
    conn.close()

    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
