"""
Lee un archivo con palabras separadas por espacios y calcula:
- Todas las palabras distintas.
- La frecuencia de aparición de cada una.
"""

import sys
import time


OUTPUT_FILE = "WordCountResults.txt"


def strip_non_alnum_edges(token):
    """Quita caracteres no alfanuméricos al inicio y/o final del token."""
    if not token:
        return ""

    start = 0
    end = len(token) - 1

    # Avanzar inicio mientras no sea alfanumérico
    while start <= end and not token[start].isalnum():
        start += 1

    # Retroceder final mientras no sea alfanumérico
    while end >= start and not token[end].isalnum():
        end -= 1

    if start > end:
        return ""

    return token[start:end + 1]


def normalize_word(token):
    """Limpia símbolo en extremos y convierte a minúscula."""
    cleaned = strip_non_alnum_edges(token)
    return cleaned.lower()


def count_words(input_path):
    """Regresa (frecuencias, total_tokens, total_valid_words)."""
    frequencies = {}
    total_tokens = 0
    total_valid_words = 0

    with open(input_path, "r", encoding="utf-8") as file:
        for line_num, line in enumerate(file, start=1):
            if not line.strip():
                continue

            tokens = line.split()
            for token in tokens:
                total_tokens += 1

                word = normalize_word(token)

                if not word:
                    print(
                        f"[ERROR] Línea {line_num}: token inválido '{token}'. Se ignora."
                    )
                    continue

                total_valid_words += 1

                if word in frequencies:
                    frequencies[word] += 1
                else:
                    frequencies[word] = 1

    return frequencies, total_tokens, total_valid_words


def build_output(input_path, frequencies, total_tokens, total_valid_words, elapsed):
    """Construye el texto final a imprimir y guardar."""
    lines = []
    lines.append(f"Archivo analizado: {input_path}")
    lines.append(f"Tokens leídos: {total_tokens}")
    lines.append(f"Palabras válidas: {total_valid_words}")
    lines.append(f"Palabras distintas: {len(frequencies)}")
    lines.append("")
    lines.append("WORD\tCOUNT")

    for word in sorted(frequencies.keys()):
        lines.append(f"{word}\t{frequencies[word]}")

    lines.append("")
    lines.append(f"Tiempo de ejecución: {elapsed:.6f} segundos")

    return "\n".join(lines) + "\n"


def main():
    """Punto de entrada principal."""
    if len(sys.argv) < 2:
        print("Uso: python wordCount.py fileWithData.txt")
        sys.exit(1)

    input_path = sys.argv[1]

    start = time.perf_counter()
    frequencies, total_tokens, total_valid_words = count_words(input_path)
    end = time.perf_counter()

    elapsed = end - start

    output_text = build_output(
        input_path, frequencies, total_tokens, total_valid_words, elapsed
    )

    print(output_text)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(output_text)


if __name__ == "__main__":
    main()
