import sqlite3
import serial
import time

# Code BDD
MAX_DATA = 100000 # Nombre de données max dans la table AirNodeData
CHECK_EVERY = 100 # Vérifie si on dépasse toutes les X messages
DB_PATH = "/home/lennea/sqlite/xbee_data.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

def create_database():
	# Créer la table des données
	cursor.execute('''
		CREATE TABLE IF NOT EXISTS AirNode(
			id INTEGER PRIMARY KEY,
			name  TEXT DEFAULT 'NoName'
		)
	''')
	cursor.execute('''
		CREATE TABLE IF NOT EXISTS AirNodeData (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			node_id INTEGER REFERENCES AirNode(id),
			co2 REAL,
			temp REAL,
			humi REAL,
			timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
		)
	''')

	conn.commit()

def count_message():
	cursor.execute('SELECT COUNT(*) FROM AirNodeData')
	return cursor.fetchone()[0]

def clear_old_data():
	nb_msg = count_message()
	if nb_msg > MAX_DATA:	
		nb_remove = nb_msg - MAX_DATA

		cursor.execute('''
			DELETE FROM AirNodeData
			WHERE id IN (
				SELECT id FROM AirNodeData
				ORDER BY timestamp ASC
				LIMIT ?
		''', (nb_remove,))

		conn.commit()

def node_exists(node_id):
	cursor.execute('SELECT id FROM AirNode Where id = ?',(node_id,))
	node = cursor.fetchone()
	
	if node:
		return node[0]
	return None

def insert_airnode(node_id):
	cursor.execute('INSERT INTO AirNode(id) VALUES(?)',(node_id,))
	conn.commit()
	return cursor.lastrowid # Retourne l'id du noeud creer

check_nb = 1
def insert_airnode_data(node_id, co2, temp, humi):
	global check_nb
	node_id = node_exists(node_id)
	
	if node_id is None:
		node_id = insert_airnode(node_id)
		print(f"Nouveau noeud ajoute :  {node_id}")
	
	cursor.execute('''
		INSERT INTO AirNodeData (node_id, co2, temp, humi)
		VALUES (?, ?, ?, ?)
	''', (node_id, co2, temp, humi))
	
	conn.commit()
	
	check_nb += 1
	if check_nb > CHECK_EVERY:
		check_nb = 0
		clear_old_data()

# Initialise la base de donnée et sa connection
create_database()
clear_old_data() #  Clear si trop de donnees

# Parsing des donnees
def parse_data(data):
	data = data.split(',')
	if len(data) != 4:
		raise ValueError(f"Parsing : Taille data de ({len(data)}) differente de 4.")
	
	id = data[0].split('-')
	co2 = data[1]
	temp = data[2]
	humi = data[3]
	
	try:
		if len(id) != 2:
			raise ValueError("ID Node non valide")
		id = int(id[1])
		co2 = float(co2)
		temp = float(temp)
		humi = float(humi)
	except ValueError as e:
		raise ValueError(str(e))
	
	return id, co2, temp, humi

# Initialise Ecoute GPIO
PORT = "/dev/ttyS0"
BAUD_RATE = 9600
def open_serial():
	return serial.Serial(PORT, BAUD_RATE, timeout=1)

ser = open_serial()

print("XBEE CONNECTER VIA GPIO")

while True:
	try:
		if ser.in_waiting > 0:
			data = ""
			try:
				data = ser.readline().decode('utf-8').strip()
			except:
				continue
			if data:
				try:
					id, co2, temp, humi = parse_data(data)
					print("Reçoit Donnes:", id, co2, temp, humi)
					insert_airnode_data(id, co2, temp, humi)
				except Exception as e:
					print("Erreur lecture donnees :", data, str(e))
		
			time.sleep(1)
	except OSError as e:
		print("Erreur de communication :", str(e))
		ser.close()
		time.sleep(1)
		ser = open_serial()
		ser.reset_input_buffer()
