from app import create_app
from extensiones import db
from models import Usuario  # Asegúrate de importar tus modelos aquí

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

