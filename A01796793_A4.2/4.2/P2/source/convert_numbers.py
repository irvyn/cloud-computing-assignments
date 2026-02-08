"""
Lee un archivo con una lista de elementos (normalmente enteros) y convierte
cada número a base binaria y hexadecimal.
"""

import sys
import time

HEX_DIGITS = "0123456789ABCDEF"

def to_binary_positive(value):
    """Convierte un entero >= 0 a binario (sin prefijo) con divisiones."""
    if value == 0:
        return "0"

    bits = []
    number = value
    while number > 0:
        bits.append(str(number % 2))
        number //= 2

    bits.reverse()
    return "".join(bits)

def to_hex_positive(value):
    """Convierte un entero >= 0 a hexadecimal (sin prefijo) con divisiones."""
    if value == 0:
        return "0"

    digits = []
    number = value
    while number > 0:
        digits.append(HEX_DIGITS[number % 16])
        number //= 16

    digits.reverse()
    return "".join(digits)

def to_binary(value):
    """Convierte un entero a binario (maneja negativos con ancho fijo)."""
    if value >= 0:
        return to_binary_positive(value)

    width_bits = 10
    modulus = 1 << width_bits
    twos_comp = modulus + value  # value es negativo

    # Si el número es más pequeño que -512, el resultado no cabría en 10 bits.
    # Aun así, lo calculamos con el módulo para mantener el comportamiento.
    return to_binary_positive(twos_comp).zfill(width_bits)

def to_hex(value):
    """Convierte un entero a hexadecimal (negativos con ancho fijo)."""
    if value >= 0:
        return to_hex_positive(value)

    width_bits = 40
    width_hex = 10
    modulus = 1 << width_bits
    twos_comp = modulus + value

    return to_hex_positive(twos_comp).zfill(width_hex)

def parse_integer(text):
    """Intenta convertir texto a int. Regresa (ok, valor_o_texto)."""
    cleaned = text.strip()
    if not cleaned:
        return False, None

    try:
        return True, int(cleaned)
    except ValueError:
        return False, cleaned

def process_file(input_path):
    """Procesa el archivo y regresa una lista de filas (item, value, bin, hex)."""
    rows = []
    item = 0

    with open(input_path, "r", encoding="utf-8") as file:
        for line_num, line in enumerate(file, start=1):
            if not line.strip():
                continue

            item += 1
            ok, value_or_text = parse_integer(line)

            if ok:
                value = value_or_text
                rows.append((item, value, to_binary(value), to_hex(value)))
            else:
                bad = value_or_text
                print(
                    f"[ERROR] Línea {line_num}: '{bad}' no es un entero válido. "
                    "Se coloca #VALUE! y se continúa."
                )
                rows.append((item, bad, "#VALUE!", "#VALUE!"))

    return rows

def build_output(input_path, rows, elapsed_seconds):
    """Construye el texto de salida para consola y archivo."""
    lines = []
    lines.append(f"Archivo analizado: {input_path}")
    lines.append("")
    lines.append("ITEM	VALUE	BIN	HEX")

    for item, original, bin_str, hex_str in rows:
        lines.append(f"{item}	{original}	{bin_str}	{hex_str}")

    lines.append("")
    lines.append(f"Tiempo de ejecución: {elapsed_seconds:.6f} segundos")
    return "".join(lines) + ""

def save_output(text_output):
    """Guarda el texto en ConvertionResults.txt."""
    with open("ConvertionResults.txt", "w", encoding="utf-8") as file:
        file.write(text_output)

def main():
    """Entrada principal."""
    if len(sys.argv) < 2:
        print("Uso: python convertNumbers.py fileWithData.txt")
        sys.exit(1)

    input_path = sys.argv[1]

    start = time.perf_counter()
    rows = process_file(input_path)
    end = time.perf_counter()

    elapsed = end - start
    output_text = build_output(input_path, rows, elapsed)

    print(output_text)
    save_output(output_text)

if __name__ == "__main__":
    main()
