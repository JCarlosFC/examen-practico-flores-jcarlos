# examen-practico-flores-jcarlos
EVALUACIÓN PRÁCTICA FINAL DE UNIDAD  - Monitoreo de Seguridad, SIEM e Inteligencia Artificial

# Examen Práctico - Seguridad Informática

## Información general

**Curso:** Seguridad Informática

**Estudiante:** Jhan Carlos Flores Chaiña

**Repositorio:** Examen Práctico de Seguridad Informática

## Descripción

Este repositorio contiene el desarrollo del examen práctico del curso de Seguridad Informática. El objetivo es implementar diferentes técnicas de análisis de registros (logs), correlación de eventos en Wazuh, detección de anomalías mediante Machine Learning.

---

# Estructura del proyecto

examen-practico-flores-jcarlos/
│
├── README.md
├── lab1/
│   ├── access.log
│   ├── auth.log
│   ├── analizar_ssh.py
│   ├── analizar_web.py
│   ├── visualizar.py
│   ├── reporte_ssh.json
│   ├── reporte_web.json
│   └── graficas/
|   └── evidencias/
│
├── lab2/
│   ├── local_rules_ssh.xml
│   ├── local_rules_exfil.xml
│   └── simular_bruteforce.sh
|   └── evidencias/
│
├── lab3/
│   ├── network_traffic.csv
│   ├── deteccion_anomalias.ipynb
│   ├── modelo_anomalias.pkl
│   └── predecir.py
|   └── evidencias/

```

---

# Laboratorio 1 - Análisis Forense de Logs

## Objetivos

* Analizar registros de autenticación SSH.
* Detectar intentos de fuerza bruta.
* Analizar registros HTTP.
* Detectar posibles ataques de SQL Injection.
* Generar reportes en formato JSON.
* Generar visualizaciones estadísticas.

### Archivos principales

* analizar_ssh.py
* analizar_web.py
* visualizar.py

### Archivos generados

* reporte_ssh.json
* reporte_web.json
* top10_ssh.png
* timeline_http.png
* heatmap_http.png

---

# Laboratorio 2 - Correlación de Eventos con Wazuh

## Objetivos

* Crear reglas personalizadas para Wazuh.
* Detectar ataques de fuerza bruta SSH.
* Detectar posibles eventos de exfiltración de información.
* Validar las reglas mediante simulaciones.

---

# Laboratorio 3 - Detección de Anomalías

## Objetivos

* Analizar tráfico de red.
* Aplicar técnicas de Machine Learning.
* Detectar tráfico anómalo utilizando Isolation Forest.
* Exportar el modelo entrenado para futuras predicciones.

---

# Requisitos

* Python 3.14
* Wazuh
* Pandas
* Matplotlib
* Scikit-learn
* Jupyter Notebook

## Instalación de dependencias

```bash
pip install pandas matplotlib scikit-learn jupyter
```

---

# Ejecución

## Laboratorio 1

```bash
cd lab1

python analizar_ssh.py
python analizar_web.py
python visualizar.py
```

## Laboratorio 2

Copiar las reglas XML al directorio de Wazuh:

```bash
sudo cp local_rules_ssh.xml /var/ossec/etc/rules/
sudo cp local_rules_exfil.xml /var/ossec/etc/rules/
```

Reiniciar Wazuh:

```bash
sudo systemctl restart wazuh-manager
```

---

# Autor

**Jhan Carlos Flores Chaiña**

Curso de Seguridad Informática

