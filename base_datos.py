import sqlite3

con = sqlite3.connect('transportadora-cun.db')
cur = con.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS aparcaderos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    municipio TEXT UNIQUE,
    lat REAL,
    lon REAL,
    capacidad INTEGER,
    ocupacion INTEGER
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS buses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    origen TEXT,
    destino TEXT,
    hora_salida TEXT,
    hora_llegada TEXT,
    aparcadero_id INTEGER,
    FOREIGN KEY (aparcadero_id) REFERENCES aparcaderos(id)
)
''')

aparcaderos = [
    ("Chocontá", 5.146678, -73.687044, 2),
    ("Tibiritá", 5.051490, -73.504577, 3),
    ("Jerusalén", 4.562677, -74.695855, 2),
    ("Ricaurte", 4.282114, -74.767717, 3),
    ("Puerto Salgar", 5.466157, -74.654130, 2),
    ("La Vega", 4.992574, -74.338211, 3),
    ("Útica", 5.185815, -74.481177, 2),
    ("Villeta", 5.013166, -74.470477, 4),
    ("Guasca", 4.869582, -73.874693, 3),
    ("Choachí", 4.526448, -73.924819, 2),
    ("Pacho", 5.140074, -74.159068, 2),
    ("Yacopí", 5.463235, -74.338550, 2),
    ("Cogua", 5.066298, -73.979012, 2),
    ("Cota", 4.807059, -74.109258, 3),
    ("Sopó", 4.913516, -73.941829, 4),
    ("Tocancipá", 4.967864, -73.905176, 4),
    ("Facatativá", 4.819769, -74.366498, 4),
    ("El Colegio", 4.582815, -74.443732, 2),
    ("Simijaca", 5.507497, -73.848055, 2),
    ("Ubaté", 5.310340, -73.819161, 3),
    ("Bogotá D.C.", 4.677584, -74.147794, 8)
]

cur.executemany("INSERT OR IGNORE INTO aparcaderos (municipio, lat, lon, capacidad, ocupacion) VALUES (?, ?, ?, ?, ?)",
                [(m, lat, lon, cap, 1) for m, lat, lon, cap in aparcaderos])

con.commit()
con.close()