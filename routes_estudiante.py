from flask import Blueprint, render_template, request, redirect, url_for
import requests
import matplotlib.pyplot as plt
import io
import base64
from flask_login import login_required, current_user

estudiante_bp = Blueprint('estudiante', __name__)

@estudiante_bp.route('/', methods=['GET', 'POST'])
@login_required
def panel_estudiante():
    # Verificar que el usuario tenga el rol de "Estudiante"
    if not current_user.is_authenticated or current_user.rol != 'Estudiante':
        return redirect(url_for('auth.login'))

    grafico = None
    datos_api = None

    if request.method == 'POST':
        # País seleccionado por el usuario (puedes dejarlo fijo si quieres)
        pais = request.form.get('pais', 'Colombia')  # Por defecto Colombia

        # Consultar API disease.sh
        url = f'https://disease.sh/v3/covid-19/countries/{pais}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # Extraer datos relevantes
            casos = data['cases']
            muertes = data['deaths']
            recuperados = data['recovered']
            activos = data['active']
            fecha_actualizacion = data['updated']

            # Guardar para mostrar en HTML
            datos_api = {
                'pais': data['country'],
                'casos': casos,
                'muertes': muertes,
                'recuperados': recuperados,
                'activos': activos,
                'fecha_actualizacion': fecha_actualizacion
            }

            # Crear gráfico circular
            labels = ['Activos', 'Recuperados', 'Muertes']
            values = [activos, recuperados, muertes]

            plt.figure(figsize=(6, 6))
            plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
            plt.title(f'Distribución de casos COVID-19 - {data["country"]}')
            plt.axis('equal')

            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            grafico = base64.b64encode(img.getvalue()).decode()
            plt.close()
        else:
            return "Error al consultar la API de disease.sh", 500

    return render_template('estudiante.html', grafico=grafico, datos_api=datos_api)
