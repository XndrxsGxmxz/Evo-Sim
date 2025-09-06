import psycopg2 # type: ignore

try:
    conn = psycopg2.connect(
        dbname="evo_sim",
        user="postgres",
        password="Juan5880#",   # tu contraseña real
        host="localhost"
    )
    print("✅ Conexión exitosa")
    conn.close()
except Exception as e:
    print("❌ Error al conectar:", e)
