import sys
import os
import pandas as pd
import joblib

def cargar_artefactos():
    """Carga el modelo y el escalador de forma local."""
    ruta_modelo = 'modelo_anomalias.pkl'
    ruta_scaler = 'scaler.pkl'
    
    if not os.path.exists(ruta_modelo) or not os.path.exists(ruta_scaler):
        print("[-] Error: No se encontraron los archivos 'modelo_anomalias.pkl' o 'scaler.pkl' en esta carpeta.")
        print("    Ejecute primero por completo el Jupyter Notebook en este directorio.")
        sys.exit(1)
        
    modelo = joblib.load(ruta_modelo)
    scaler = joblib.load(ruta_scaler)
    return modelo, scaler

def preprocesar_datos(df, scaler):
    """Aplica ingeniería de características y normalización."""

    df['ratio_bytes'] = df['bytes_sent'] / (df['bytes_recv'] + 1)
    df['bytes_por_segundo'] = (df['bytes_sent'] + df['bytes_recv']) / (df['duration_sec'] + 0.001)
    

    features_cols = ['dst_port', 'bytes_sent', 'bytes_recv', 'duration_sec', 'packets', 'ratio_bytes', 'bytes_por_segundo']
    

    for col in features_cols[:-2]:
        if col not in df.columns:
            print(f"[-] Error: Al dataset proporcionado le falta la columna requerida: '{col}'")
            sys.exit(1)
            
    X = df[features_cols]
    X_scaled = scaler.transform(X)
    return X_scaled

def main():

    if len(sys.argv) < 2:
        print("[!] Uso correcto: python predecir.py <ruta_del_archivo_csv>")
        print("[*] Ejemplo: python predecir.py network_traffic.csv")
        sys.exit(1)
        
    input_csv = sys.argv[1]
    
    if not os.path.exists(input_csv):
        print(f"[-] Error: El archivo '{input_csv}' no existe.")
        sys.exit(1)
        
    print(f"[*] Analizando tráfico de red local: {input_csv}...")
    df_nuevo = pd.read_csv(input_csv)

    modelo, scaler = cargar_artefactos()
    X_nuevo_scaled = preprocesar_datos(df_nuevo, scaler)

    df_nuevo['pred_code'] = modelo.predict(X_nuevo_scaled)
    df_nuevo['pred_label'] = df_nuevo['pred_code'].map({1: 'normal', -1: 'anomaly'})

    total_registros = len(df_nuevo)
    anomalias_detectadas = (df_nuevo['pred_code'] == -1).sum()
    porcentaje_anomalo = (anomalias_detectadas / total_registros) * 100
    
    print("\n==================================================")
    print("        Resultado del analisis de seguridad       ")
    print("==================================================")
    print(f" Total de conexiones analizadas : {total_registros}")
    print(f" Anomalías de red detectadas     : {anomalias_detectadas} ({porcentaje_anomalo:.2f}%)")
    print("==================================================")
    
    # Listar una muestra corta de las alertas más críticas si existen
    if anomalias_detectadas > 0:
        print("\n[ALERTA] Conexiones anómalas críticas identificadas:")
        cols_alerta = ['src_ip', 'dst_ip', 'dst_port', 'bytes_sent', 'pred_label']
        cols_visibles = [c for c in cols_alerta if c in df_nuevo.columns]
        print(df_nuevo[df_nuevo['pred_code'] == -1][cols_visibles].head(5).to_string(index=False))
        print("==================================================\n")

if __name__ == '__main__':
    main()