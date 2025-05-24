from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from math import radians, cos, sin, asin, sqrt

app = Flask(__name__)
app.secret_key = 'josuerom'
DB = 'transportadora-cun.db'

def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return R * 2 * asin(sqrt(a))

@app.route('/')
def index():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT * FROM aparcaderos")
    aparcaderos = cur.fetchall()
    cur.execute("SELECT * FROM buses")
    buses = cur.fetchall()
    con.close()
    ultimo_id = session.pop('ultimo_bus_id', None)
    return render_template('index.html', aparcaderos=aparcaderos, buses=buses, ultimo_bus_id=ultimo_id)

@app.route('/registrar_bus', methods=['POST'])
def registrar_bus():
    datos = request.form
    origen = datos['origen']
    destino = datos['destino']
    hora_salida = datos['hora_salida']

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("SELECT capacidad, ocupacion FROM aparcaderos WHERE municipio = ?", (origen,))
    cap_ori, ocu_ori = cur.fetchone()

    cur.execute("SELECT capacidad, ocupacion FROM aparcaderos WHERE municipio = ?", (destino,))
    cap_des, ocu_des = cur.fetchone()

    if ocu_ori <= 0:
        con.close()
        return render_template('index.html', error=f"No hay buses disponibles en {origen}", aparcaderos=get_aparcaderos(), buses=get_buses())

    if ocu_des >= cap_des:
        con.close()
        return render_template('index.html', error=f"El aparcadero en {destino} está lleno", aparcaderos=get_aparcaderos(), buses=get_buses())

    cur.execute("UPDATE aparcaderos SET ocupacion = ocupacion - 1 WHERE municipio = ?", (origen,))
    cur.execute("UPDATE aparcaderos SET ocupacion = ocupacion + 1 WHERE municipio = ?", (destino,))
    cur.execute("SELECT id FROM aparcaderos WHERE municipio = ?", (origen,))
    aparcadero_id = cur.fetchone()[0]

    cur.execute("INSERT INTO buses (origen, destino, hora_salida, hora_llegada, aparcadero_id) VALUES (?, ?, ?, ?, ?)",
                (origen, destino, hora_salida, '', aparcadero_id))
    bus_id = cur.lastrowid

    con.commit()
    con.close()

    session['ultimo_bus_id'] = bus_id
    return redirect(url_for('index'))

@app.route('/api/recorrido/<int:bus_id>')
def api_recorrido(bus_id):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("""
        SELECT o.lat, o.lon, d.lat, d.lon FROM buses b
        JOIN aparcaderos o ON b.origen = o.municipio
        JOIN aparcaderos d ON b.destino = d.municipio
        WHERE b.id = ?
    """, (bus_id,))
    data = cur.fetchone()
    con.close()
    if data:
        lat1, lon1, lat2, lon2 = data
        distancia = calcular_distancia(lat1, lon1, lat2, lon2)
        tiempo_total = distancia / 60 * 60 + 20
        return {
            "lat1": lat1, "lon1": lon1, "lat2": lat2, "lon2": lon2, "tiempo": tiempo_total
        }
    return {"error": "Bus no encontrado"}

def get_aparcaderos():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT * FROM aparcaderos")
    res = cur.fetchall()
    con.close()
    return res

def get_buses():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT * FROM buses")
    res = cur.fetchall()
    con.close()
    return res

if __name__ == '__main__':
    app.run(debug=True)
