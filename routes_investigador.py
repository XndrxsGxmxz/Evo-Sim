from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
import numpy as np
from scipy.integrate import odeint
import matplotlib
matplotlib.use('Agg')  # Configurar Matplotlib para usar el backend no interactivo
import matplotlib.pyplot as plt
import os
import requests
from matplotlib.ticker import FuncFormatter

investigador = Blueprint('investigador', __name__)

def obtener_datos_reales():
    # Obtener datos históricos de Colombia
    url_historico = "https://disease.sh/v3/covid-19/historical/Colombia?lastdays=all"
    url_poblacion = "https://disease.sh/v3/covid-19/countries/Colombia"

    try:
        # Datos históricos
        response_historico = requests.get(url_historico)
        response_historico.raise_for_status()
        datos_historicos = response_historico.json()

        # Datos de población
        response_poblacion = requests.get(url_poblacion)
        response_poblacion.raise_for_status()
        datos_poblacion = response_poblacion.json()

        # Extraer datos históricos
        casos_diarios = list(datos_historicos['timeline']['cases'].values())
        muertes_diarias = list(datos_historicos['timeline']['deaths'].values())
        recuperaciones_diarias = list(datos_historicos['timeline']['recovered'].values())

        # Extraer población total
        poblacion_total = datos_poblacion['population']

        return casos_diarios, muertes_diarias, recuperaciones_diarias, poblacion_total
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos de la API: {e}")
        return None, None, None, None

@investigador.route('/', methods=['GET', 'POST'])
@login_required
def panel_investigador():
    if not current_user.is_authenticated or current_user.rol != 'Investigador':
        return redirect(url_for('auth.login'))

    valores = {
        'beta': '',
        'gamma': '',
        'S0': '',
        'I0': '',
        'R0': '',
        'dias': '',
        'delta': ''  # Agregamos delta al diccionario
    }

    imagen = None
    error = None

    if request.method == 'POST':
        # Procesar valores del formulario
        valores['beta'] = request.form.get('beta', '')
        valores['gamma'] = request.form.get('gamma', '')
        valores['S0'] = request.form.get('S0', '')
        valores['I0'] = request.form.get('I0', '')
        valores['R0'] = request.form.get('R0', '')
        valores['dias'] = request.form.get('dias', '')
        valores['delta'] = request.form.get('delta', '0.01')  # Valor predeterminado para delta

        try:
            # Convertir valores a números
            beta = float(valores['beta'])
            gamma = float(valores['gamma'])
            S0 = float(valores['S0'])
            I0 = float(valores['I0'])
            R0 = float(valores['R0'])
            dias = int(valores['dias'])
            delta = float(valores['delta'])  # Convertir delta a número

            # Validar que los valores no sean negativos
            if beta < 0 or gamma < 0 or S0 < 0 or I0 < 0 or R0 < 0 or dias <= 0 or delta < 0:
                raise ValueError("No se permiten valores negativos o días menores o iguales a 0.")

            # Obtener datos reales
            casos_reales, muertes_reales, recuperaciones_reales, poblacion_total = obtener_datos_reales()
            if not casos_reales or not muertes_reales or not recuperaciones_reales:
                raise ValueError("No se pudieron obtener datos reales de la API.")

            # Configurar población inicial
            S0 = poblacion_total - I0 - R0
            N = S0 + I0 + R0

            # Ajustar el rango de días a los datos reales
            dias_disponibles = len(casos_reales)
            if dias > dias_disponibles:
                dias = dias_disponibles

            # Definir el modelo SIR con mortalidad
            def deriv(y, t, N, beta, gamma, delta):
                S, I, R, D = y  # D es la población fallecida
                dSdt = -beta * S * I / N
                dIdt = beta * S * I / N - gamma * I - delta * I
                dRdt = gamma * I
                dDdt = delta * I
                return dSdt, dIdt, dRdt, dDdt

            # Resolver el sistema de ecuaciones diferenciales
            t = np.linspace(0, dias - 1, dias)
            y0 = S0, I0, R0, 0  # Inicializamos D (muertes) en 0
            ret = odeint(deriv, y0, t, args=(N, beta, gamma, delta))
            S, I, R, D = ret.T  # Extraemos también las muertes (D)

            # Crear el gráfico
            plt.figure(figsize=(10, 6))

            # Cambiar de días a meses si los días son mayores a 364
            if dias > 364:
                t = t / 30  # Convertir días a meses
                plt.xlabel('Meses desde el inicio de la pandemia')
                x_reales = np.array(range(dias)) / 30  # Convertir días reales a meses
            else:
                plt.xlabel('Días desde el inicio de la pandemia')
                x_reales = range(dias)

            # Simulación
            plt.plot(t, I, label='Infectados (Simulado)', color='orange')
            plt.plot(t, R, label='Recuperados (Simulado)', color='green')
            plt.plot(t, D, label='Muertes (Simulado)', color='red')

            # Datos reales
            plt.plot(x_reales, casos_reales[:dias], '--', label='Casos (Reales)', color='orange')
            plt.plot(x_reales, recuperaciones_reales[:dias], '--', label='Recuperados (Reales)', color='green')
            plt.plot(x_reales, muertes_reales[:dias], '--', label='Muertes (Reales)', color='red')

            # Configuración del eje y para mostrar en millones
            def millones(x, pos):
                return f'{int(x / 1_000_000)}M'

            plt.gca().yaxis.set_major_formatter(FuncFormatter(millones))

            # Configuración del gráfico
            plt.ylabel('Población (millones)')
            plt.title('Comparación de Simulación SIR con Datos Reales')
            plt.legend()
            plt.grid(True)

            # Guardar el gráfico
            output_path = os.path.join('static', 'grafico.png')
            plt.savefig(output_path)
            plt.close()

            imagen = output_path
        except ValueError as e:
            error = str(e)

    return render_template('investigador.html', valores=valores, imagen=imagen, error=error)
