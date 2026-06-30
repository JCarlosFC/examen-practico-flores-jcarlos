import re
import os
from collections import Counter, defaultdict
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt

SSH_LOG = "auth.log"
WEB_LOG = "access.log"

OUTPUT_DIR = "graficos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# grafico 1
ip_regex = re.compile(r"Failed password.*from (\d+\.\d+\.\d+\.\d+)")

contador = Counter()

with open(SSH_LOG, encoding="utf-8", errors="ignore") as f:
    for linea in f:
        m = ip_regex.search(linea)
        if m:
            contador[m.group(1)] += 1
top10 = contador.most_common(10)

ips = [x[0] for x in top10]
intentos = [x[1] for x in top10]

plt.figure(figsize=(10,5))
plt.bar(ips, intentos)
plt.title("Top 10 ips con más intentos fallidos ssh")
plt.xlabel("Dirección ip")
plt.ylabel("Intentos")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(os.path.join(OUTPUT_DIR, "top10_ssh.png"))
plt.close()

regex = re.compile(
    r'(\S+) \S+ \S+ \[(.*?)\] '
    r'"(\S+) (.*?) (\S+)" '
    r'(\d{3}) (\S+)'
)

eventos = []

with open(WEB_LOG, encoding="utf-8", errors="ignore") as f:

    for linea in f:
        m = regex.match(linea)
        if not m:
            continue
        fecha = datetime.strptime(
            m.group(2),
            "%d/%b/%Y:%H:%M:%S %z"
        )
        eventos.append({
            "hora": fecha.hour,
            "codigo": int(m.group(6))
        })

#Grafico 2
conteo_horas = defaultdict(int)

for e in eventos:
    conteo_horas[e["hora"]] += 1

horas = sorted(conteo_horas.keys())
peticiones = [conteo_horas[h] for h in horas]

plt.figure(figsize=(10,5))
plt.plot(horas, peticiones, marker="o")
plt.title("Peticiones http por hora")
plt.xlabel("Hora")
plt.ylabel("Cantidad")
plt.grid(True)

plt.savefig(os.path.join(OUTPUT_DIR, "timeline_http.png"))
plt.close()

#Grafico 3
df = pd.DataFrame(eventos)

tabla = pd.crosstab(
    df["hora"],
    df["codigo"]
)

plt.figure(figsize=(10,6))

plt.imshow(
    tabla,
    aspect="auto",
    interpolation="nearest"
)

plt.colorbar(label="Cantidad")

plt.xticks(
    range(len(tabla.columns)),
    tabla.columns
)

plt.yticks(
    range(len(tabla.index)),
    tabla.index
)

plt.title("Heatmap HTTP por hora y código")
plt.xlabel("Código HTTP")
plt.ylabel("Hora")

plt.tight_layout()

plt.savefig(os.path.join(OUTPUT_DIR, "heatmap_http.png"))
plt.close()

print("Gráficas generadas correctamente.")