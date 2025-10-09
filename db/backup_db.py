import subprocess

usuario = "postgres"
basedatos = "evo_sim"
archivo_salida = "evo_sim_backup.sql"

comando = [
    "pg_dump",
    "-U", usuario,
    "-h", "localhost",
    "-F", "p",
    "-f", archivo_salida,
    basedatos
]

try:
    # Ejecuta el comando pg_dump
    resultado = subprocess.run(comando, check=True)
    print(f"✅ Backup creado: {archivo_salida}")
except Exception as e:
    print("❌ Error al crear el backup:", e)