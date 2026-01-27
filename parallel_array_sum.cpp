#include <iostream> // Librería estándar para el manejo de flujos de entrada y salida (cout)
#include <omp.h>    // Librería de OpenMP para habilitar funciones y directivas de multinúcleo

// Macros: Definiciones que el preprocesador reemplaza antes de la compilación
#define N 1000      // Cantidad total de elementos en los arreglos
#define chunk 100   // Tamaño del bloque (cantidad de iteraciones) asignado a cada hilo
#define mostrar 10  // Límite de elementos a imprimir en pantalla

// Prototipo de función: Se declara antes de main para que el compilador sepa que existe
void imprimeArreglo(float *d);

int main()
{
    // std::cout: Objeto de flujo de salida estándar para imprimir en consola
    std::cout << "Sumando Arreglos en Paralelo con OpenMP!\n";

    // Declaración de arreglos de punto flotante de tamaño fijo asignados en el stack
    float a[N], b[N], c[N];
    int pedazos = chunk;

    // Directiva OpenMP: Divide el ciclo for entre los hilos disponibles
    // schedule(static, pedazos): Reparte el trabajo en bloques fijos de tamaño 'pedazos'
    #pragma omp parallel for schedule(static, pedazos)
    for (int i = 0; i < N; i++) {
        a[i] = i + 1;
        b[i] = i + 11;
    }

    // Nueva región paralela para realizar la suma de vectores
    // Los hilos se sincronizan automáticamente al finalizar el ciclo
    #pragma omp parallel for schedule(static, pedazos)
    for (int i = 0; i < N; i++) {
        c[i] = a[i] + b[i];
    }

    // std::endl: Inserta un salto de línea y limpia el búfer de salida
    std::cout << "Resultados (mostrando primeros " << mostrar << " elementos):" << std::endl;

    // Llamadas a la función pasando el puntero al inicio del arreglo
    std::cout << "Arreglo a: "; imprimeArreglo(a);
    std::cout << "Arreglo b: "; imprimeArreglo(b);
    std::cout << "Arreglo c: "; imprimeArreglo(c);

    return 0; // Indica al sistema operativo que el programa finalizó correctamente
}

// Definición de la función: Recibe un puntero a float (dirección de memoria del arreglo)
void imprimeArreglo(float *d)
{
    for (int x = 0; x < mostrar; x++)
        std::cout << d[x] << " - ";

    std::cout << std::endl;
}