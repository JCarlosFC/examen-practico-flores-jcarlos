import re
import json
from collections import Counter
from datetime import datetime

LOG_FILE = "auth.log"
OUTPUT_FILE = "reporte_ssh.json"

ip_regex = re.compile(r"Failed password.*from (\d+\.\d+\.\d+\.\d+)")

contador_ips = Counter()

with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as archivo:
    for linea in archivo:
        coincidencia = ip_regex.search(linea)
        if coincidencia:
            ip = coincidencia.group(1)
            contador_ips[ip] += 1

print("=" * 50)
print("TOP 10 IPs CON MÁS INTENTOS FALLIDOS")
print("=" * 50)

top10 = contador_ips.most_common(10)

for posicion, (ip, intentos) in enumerate(top10, start=1):
    print(f"{posicion:2d}. {ip:15} -> {intentos} intentos")

print()

ips_sospechosas = []

for ip, intentos in contador_ips.items():

    alerta = intentos > 50

    if alerta:
        print(f"[ALERTA] IP: {ip} - {intentos} intentos fallidos - Posible ataque de fuerza bruta")

    ips_sospechosas.append({
        "ip": ip,
        "intentos": intentos,
        "alerta": alerta
    })

reporte = {
    "fecha_analisis": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "total_intentos_fallidos": sum(contador_ips.values()),
    "ips_sospechosas": sorted(
        ips_sospechosas,
        key=lambda x: x["intentos"],
        reverse=True
    )
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as archivo_json:
    json.dump(reporte, archivo_json, indent=4)

print()
print(f"Reporte generado: {OUTPUT_FILE}")