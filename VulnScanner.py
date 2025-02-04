import requests
from bs4 import BeautifulSoup
import os
from zapv2 import ZAPv2
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from email.mime.text import MIMEText

zap_api_key = 'API_KEY'  # Reemplaza con tu clave API de ZAP
zap = ZAPv2(apikey=zap_api_key)

def authenticate(session, url, username, password):
    payload = {'username': username, 'password': password}
    session.post(url, data=payload)

def check_insecure_inputs(session, url):
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    inputs = soup.find_all('input')
    insecure_fields = []
    for input_tag in inputs:
        if 'type' not in input_tag.attrs or input_tag['type'] in ['text', 'password']:
            insecure_fields.append(input_tag)
            print(f'[!] Campo de entrada inseguro encontrado en: {url} ({input_tag})')
    return insecure_fields

def run_sqlmap(url):
    print(f'[+] Iniciando escaneo SQLi con sqlmap en: {url}')
    os.system(f"python3 sqlmap/sqlmap.py -u {url} --batch --output-dir=sqlmap_output")
    print(f'[+] Escaneo SQLi con sqlmap completado para: {url}')

def run_owasp_zap(url):
    print(f'[+] Iniciando escaneo con OWASP ZAP en: {url}')
    zap.urlopen(url)
    scan_id = zap.ascan.scan(url)
    while int(zap.ascan.status(scan_id)) < 100:
        print(f"[+] Escaneando {url} con OWASP ZAP, progreso: {zap.ascan.status(scan_id)}%")
    print(f'[+] Escaneo de OWASP ZAP completado para {url}')
    report = zap.core.htmlreport()
    report_filename = f'owasp_zap_report_{datetime.now().strftime("%Y%m%d%H%M%S")}.html'
    with open(report_filename, 'w') as file:
        file.write(report)
    print(f'[+] Reporte de OWASP ZAP guardado en "{report_filename}"')

def send_email(subject, body, to_email):
    from_email = 'tu_email@example.com'  # Reemplaza con tu email
    password = 'tu_contraseña'  # Reemplaza con tu contraseña
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    
    with smtplib.SMTP('smtp.example.com', 587) as server:  # Reemplaza con el servidor SMTP correcto
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, [to_email], msg.as_string())
    print(f'[+] Notificación enviada a {to_email}')

def run_dependency_check():
    print(f'[+] Iniciando escaneo de dependencias con OWASP Dependency-Check')
    os.system(f"dependency-check --project 'Proyecto' --scan ./ --format 'JSON' --out ./dependency-check-report.json")
    print(f'[+] Escaneo de dependencias completado')

urls_to_scan = [
    {'url': 'https://www.ejemplo1.com', 'auth': {'url': 'https://www.ejemplo1.com/login', 'username': 'user1', 'password': 'pass1'}},
    {'url': 'https://www.ejemplo2.com', 'auth': {'url': 'https://www.ejemplo2.com/login', 'username': 'user2', 'password': 'pass2'}}
]

def run_full_scan():
    session = requests.Session()
    for target in urls_to_scan:
        url = target['url']
        auth = target['auth']
        print(f'[+] Escaneando {url}')
        
        authenticate(session, auth['url'], auth['username'], auth['password'])
        
        insecure_fields = check_insecure_inputs(session, url)
        run_sqlmap(url)
        run_owasp_zap(url)
        
        with open(f'report_{url.replace("https://", "").replace("/", "_")}.txt', 'w') as report_file:
            report_file.write(f'Escaneo para {url}\n\n')
            report_file.write('Campos de entrada inseguros:\n')
            for field in insecure_fields:
                report_file.write(f'{field}\n')
        
        print(f'[+] Escaneo completo para {url}')
    
    run_dependency_check()
    send_email('Informe de Escaneo Completo', 'El escaneo completo se ha completado. Los informes están disponibles.', 'destinatario@example.com')
    print('[+] Todos los escaneos completados')

scheduler = BackgroundScheduler()
scheduler.add_job(run_full_scan, 'interval', days=1)
scheduler.start()

try:
    while True:
        pass
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
