import shutil
import os

# Ruta del proyecto
origen = os.getcwd()
destino = os.path.join(origen, "backup")

# Copia toda la carpeta del proyecto (excepto el backup anterior)
try:
    if os.path.exists(destino):
        shutil.rmtree(destino)
    shutil.copytree(origen, destino, ignore=shutil.ignore_patterns('backup', '*.zip'))
    print(f"Backup de archivos creado en: {destino}")
except Exception as e:
    print("Error al copiar archivos:", e)

# Comprime el backup en un ZIP
try:
    zip_path = os.path.join(origen, "backup.zip")
    shutil.make_archive(os.path.splitext(zip_path)[0], 'zip', destino)
    print(f"Backup comprimido en: {zip_path}")
except Exception as e:
    print("Error al comprimir el backup:", e)