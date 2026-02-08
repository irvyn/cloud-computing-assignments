"""
Lee una lista de números desde un archivo y calcula estadísticas descriptivas:
media, mediana, moda, varianza poblacional y desviación estándar poblacional.
"""
import sys
import time


def leer_datos(nombre_archivo):
    """Lee números desde un archivo, ignorando líneas inválidas."""
    numeros = []
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        for linea_num, linea in enumerate(archivo, start=1):
            linea = linea.strip()

            if not linea:
                continue

            try:
                numero = float(linea)
                numeros.append(numero)
            except ValueError:
                print(
                    f"[ERROR] Línea {linea_num}: '{linea}' no es un número válido. "
                    "Se ignora."
                )

    return numeros


def calcular_media(datos):
    """Calcula la media (promedio) usando suma / N."""
    suma = 0.0
    for num in datos:
        suma += num
    return suma / len(datos)


def calcular_mediana(datos):
    """Calcula la mediana ordenando los datos."""
    datos_ordenados = sorted(datos)
    n = len(datos_ordenados)

    if n % 2 == 1:
        return datos_ordenados[n // 2]

    mid1 = datos_ordenados[n // 2 - 1]
    mid2 = datos_ordenados[n // 2]
    return (mid1 + mid2) / 2


def calcular_moda(datos):
    """Calcula la moda (el valor más frecuente) usando un conteo."""
    frecuencias = {}

    for num in datos:
        if num in frecuencias:
            frecuencias[num] += 1
        else:
            frecuencias[num] = 1

    max_frecuencia = 0
    moda = None

    for num, freq in frecuencias.items():
        if freq > max_frecuencia:
            max_frecuencia = freq
            moda = num

    return moda


def calcular_varianza_poblacional(datos, media):
    """Calcula la varianza poblacional: sum((x - media)^2) / N."""
    suma_cuadrados = 0.0
    for num in datos:
        suma_cuadrados += (num - media) ** 2
    return suma_cuadrados / len(datos)


def calcular_desviacion_estandar(varianza):
    """Calcula la desviación estándar poblacional: sqrt(varianza)."""
    return varianza ** 0.5


def guardar_resultados(resultados_texto):
    """Guarda los resultados en el archivo StatisticsResults.txt."""
    with open("StatisticsResults.txt", "w", encoding="utf-8") as archivo:
        archivo.write(resultados_texto)


def main():
    """Punto de entrada principal del programa."""
    if len(sys.argv) < 2:
        print("Uso correcto: python computeStatistics.py archivoConDatos.txt")
        sys.exit(1)

    nombre_archivo = sys.argv[1]
    inicio = time.time()

    datos = leer_datos(nombre_archivo)

    if not datos:
        print("El archivo no contiene datos válidos. No se puede continuar.")
        sys.exit(1)

    media = calcular_media(datos)
    mediana = calcular_mediana(datos)
    moda = calcular_moda(datos)
    varianza = calcular_varianza_poblacional(datos, media)
    desviacion = calcular_desviacion_estandar(varianza)

    fin = time.time()
    tiempo_total = fin - inicio

    resultados = (
        f"Archivo analizado: {nombre_archivo}\n"
        f"Cantidad de datos válidos: {len(datos)}\n\n"
        f"MEDIA: {media}\n"
        f"MEDIANA: {mediana}\n"
        f"MODA: {moda}\n"
        f"VARIANZA POBLACIONAL: {varianza}\n"
        f"DESVIACION ESTANDAR POBLACIONAL: {desviacion}\n\n"
        f"Tiempo de ejecución: {tiempo_total} segundos\n"
    )

    print(resultados)
    guardar_resultados(resultados)


if __name__ == "__main__":
    main()
