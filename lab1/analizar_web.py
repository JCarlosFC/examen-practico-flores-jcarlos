import re
import json
from collections import defaultdict
from datetime import datetime
from collections import deque

LOG_FILE = "access.log"
OUTPUT_FILE = "reporte_web.json"

log_regex = re.compile(
    r'(\S+) \S+ \S+ \[(.*?)\] '
    r'"(\S+) (.*?) (\S+)" '
    r'(\d{3}) (\S+)'
)

eventos = []

with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as archivo:

    for linea in archivo:
        m = log_regex.match(linea)
        if not m:
            continue
        ip = m.group(1)
        fecha = datetime.strptime(
            m.group(2),
            "%d/%b/%Y:%H:%M:%S %z"
        )
        metodo = m.group(3)
        url = m.group(4)
        codigo = int(m.group(6))
        eventos.append({
            "ip": ip,
            "fecha": fecha,
            "metodo": metodo,
            "url": url,
            "codigo": codigo
        })
print(f"se cargaron {len(eventos)} eventos.")

escaneos = []
eventos_por_ip = defaultdict(list)

for evento in eventos:
    eventos_por_ip[evento["ip"]].append(evento)

for ip, lista in eventos_por_ip.items():
    lista.sort(key=lambda x: x["fecha"])
    ventana = deque()
    for evento in lista:
        ventana.append(evento)
        while (evento["fecha"] - ventana[0]["fecha"]).total_seconds() > 60:
            ventana.popleft()
        rutas = {e["url"] for e in ventana}
        if len(rutas) > 20:
            escaneos.append({
                "ip": ip,
                "inicio": ventana[0]["fecha"].strftime("%Y-%m-%d %H:%M:%S"),
                "fin": evento["fecha"].strftime("%Y-%m-%d %H:%M:%S"),
                "rutas_distintas": len(rutas)
            })
            break

print(f"Escaneos detectados: {len(escaneos)}")

errores_http = defaultdict(lambda: {
    "4xx": 0,
    "5xx": 0
})

for evento in eventos:
    codigo = evento["codigo"]
    if 400 <= codigo < 500:
        errores_http[evento["ip"]]["4xx"] += 1
    elif 500 <= codigo < 600:
        errores_http[evento["ip"]]["5xx"] += 1
print(f"IPs con errores HTTP: {len(errores_http)}")

patrones_sqli = [
    "UNION",
    "SELECT",
    "--",
    "OR 1=1",
    "'"
]
sqli = []

for evento in eventos:
    url = evento["url"].upper()
    for patron in patrones_sqli:
        if patron in url:
            sqli.append({
                "ip": evento["ip"],
                "fecha": evento["fecha"].strftime("%Y-%m-%d %H:%M:%S"),
                "url": evento["url"],
                "patron": patron
            })
            break

print(f"Posibles SQL Injection: {len(sqli)}")

reporte = {
    "fecha_analisis": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "total_eventos": len(eventos),
    "escaneos_directorios": escaneos,
    "errores_http": dict(errores_http),
    "posibles_sqli": sqli
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as archivo:

    json.dump(
        reporte,
        archivo,
        indent=4
    )
print()
print(f"Reporte generado: {OUTPUT_FILE}")