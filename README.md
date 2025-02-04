# VulnScanner 

Es una herramienta de automatización para realizar escaneos de vulnerabilidades en aplicaciones web utilizando OWASP ZAP, SQLmap, y Dependency-Check. También envía notificaciones por correo electrónico con los resultados de los escaneos.

Funcionalidad
Autenticación: Autentica a un usuario en una aplicación web.

Escaneo de Campos Inseguros: Verifica la existencia de campos de entrada inseguros en formularios.

Escaneo SQLi con SQLmap: Realiza escaneos de inyección SQL.

Escaneo con OWASP ZAP: Realiza escaneos de seguridad completos utilizando OWASP ZAP.

Escaneo de Dependencias: Utiliza OWASP Dependency-Check para escanear dependencias de software.

Notificaciones por Correo Electrónico: Envía notificaciones por correo electrónico con los resultados de los escaneos.

Programación de Escaneos: Programa la ejecución automática de los escaneos cada día.

Cómo Funciona
Instalar Dependencias: Instala todas las dependencias necesarias.

Configurar Parámetros: Modifica los parámetros y datos de configuración según tus necesidades.

Ejecutar el Script: Ejecuta el script para iniciar los escaneos.

Pasos para Hacerlo Funcionar
Paso 1: Instalar Dependencias
Necesitas tener instalado Python, así como las siguientes librerías:

requests

beautifulsoup4

python-owasp-zap-v2

apscheduler

smtplib

Puedes instalar las librerías con el siguiente comando:

pip install requests beautifulsoup4 python-owasp-zap-v2 apscheduler

Paso 2: Configurar Parámetros
Modifica las siguientes líneas en el código:

zap_api_key = 'API_KEY'  # Reemplaza con tu clave API de ZAP

Datos del Correo Electrónico:

from_email = 'tu_email@example.com'  # Reemplaza con tu email
password = 'tu_contraseña'  # Reemplaza con tu contraseña
with smtplib.SMTP('smtp.example.com', 587) as server:  # Reemplaza con el servidor SMTP correcto

URLs y Credenciales para Escanear:

urls_to_scan = [
    {'url': 'https://www.ejemplo1.com', 'auth': {'url': 'https://www.ejemplo1.com/login', 'username': 'user1', 'password': 'pass1'}},
    {'url': 'https://www.ejemplo2.com', 'auth': {'url': 'https://www.ejemplo2.com/login', 'username': 'user2', 'password': 'pass2'}}
]

Paso 3: Ejecutar el Script
Simplemente ejecuta el script en tu entorno de Python:

python vulnscanner.py

El script se mantendrá en ejecución y programará los escaneos para que se realicen automáticamente todos los días. ¡Y eso es todo! Tu herramienta "VulnScanner" estará funcionando y enviándote informes de vulnerabilidades automáticamente.
