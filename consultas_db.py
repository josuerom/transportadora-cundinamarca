import sqlite3

def mostrar_registros():
    try:
        conexion = sqlite3.connect('transportadora-cun.db')
        cursor = conexion.cursor()

        print("\nRegistros de la tabla 'buses':")
        cursor.execute("SELECT * FROM buses")
        buses = cursor.fetchall()
        for bus in buses:
            print(bus)

        print()

    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
    finally:
        if conexion:
            conexion.close()

if __name__ == '__main__':
    mostrar_registros()

