import sys

# Precedencia de operadores
PRECEDENCE = {
    '|': 2,  # Unión
    '.': 3,  # Concatenación
    '?': 4,  # Cero o uno
    '*': 4,  # Cero o más
    '+': 4,  # Uno o más
    '^': 5  # Potencia
}


# Verifica la necesidad de un operador de concatenación
def needs_concat(c1, c2):
    if c1 == '(' or c2 == ')':
        return False
    if c2 in PRECEDENCE and c2 not in ['?', '*', '+']:
        return False
    if c1 in PRECEDENCE and c1 not in ['|', '^']:
        return False
    return True


# Inserta operadores de concatenación explícitos
def format_regex(regex):
    formatted = []
    i = 0
    print("\n[PASO 1] Formateando expresión:")
    while i < len(regex):
        c = regex[i]

        # Manejar caracteres escapados
        if c == '\\':
            if i + 1 < len(regex):
                print(f"- Carácter escapado: '\\{regex[i + 1]}'")
                formatted.append(c + regex[i + 1])
                i += 2
                continue
            else:
                formatted.append(c)
                i += 1
                continue

        formatted.append(c)
        print(f"- Procesando: '{c}'")

        # Verificar si necesita concatenación
        if i + 1 < len(regex):
            next_c = regex[i + 1]
            if needs_concat(c, next_c):
                print(f"  → Insertando '.' entre '{c}' y '{next_c}'")
                formatted.append('.')
        i += 1

    result = ''.join(formatted)
    print(f"[RESULTADO FORMATEO] {result}")
    return result


# Convierte expresión de infix a postifx
def infix_to_postfix(regex):
    output = []
    operator_stack = []
    formatted_re = format_regex(regex)

    print("\n[PASO 2] Conversión a postfix:")
    print("Carácter\tPila\t\tSalida\t\tAcción")
    print("-" * 60)

    i = 0
    while i < len(formatted_re):
        c = formatted_re[i]
        action = ""

        # Manejar caracteres escapados
        if c == '\\':
            if i + 1 < len(formatted_re):
                output.append(c + formatted_re[i + 1])
                action = f"Añadir '{c + formatted_re[i + 1]}'"
                i += 2
            else:
                output.append(c)
                action = f"Añadir '{c}'"
                i += 1
            print(f"'{c}'\t\t{''.join(operator_stack)}\t\t{''.join(output)}\t\t{action}")
            continue

        if c == '(':
            operator_stack.append(c)
            action = "Apilar '('"

        elif c == ')':
            action = "Desapilar hasta '('"
            while operator_stack and operator_stack[-1] != '(':
                output.append(operator_stack.pop())
            operator_stack.pop()  # Remover el '('

        elif c in PRECEDENCE:
            action = f"Procesar '{c}'"
            while (operator_stack and operator_stack[-1] != '(' and
                   PRECEDENCE.get(operator_stack[-1], 0) >= PRECEDENCE[c]):
                output.append(operator_stack.pop())
            operator_stack.append(c)

        else:
            output.append(c)
            action = f"Añadir '{c}'"

        print(f"'{c}'\t\t{''.join(operator_stack)}\t\t{''.join(output)}\t\t{action}")
        i += 1

    # Vaciar lo que quede en la pila
    while operator_stack:
        c = operator_stack.pop()
        output.append(c)
        print(f" \t\t{''.join(operator_stack)}\t\t{''.join(output)}\t\tDesapilar '{c}'")

    result = ''.join(output)
    print(f"\n[RESULTADO POSTFIX] {result}")
    return result


def main():
    archivo_expresiones = "expresiones.txt"

    try:
        with open(archivo_expresiones, 'r') as file:
            print("\nIniciando procesamiento de expresiones regulares")
            print("=" * 60)

            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                print(f"\n>>> Procesando línea {line_num}: {line}")
                print("-" * 60)

                try:
                    # Paso 1: Formatear la expresión
                    formatted = format_regex(line)

                    # Paso 2: Convertir a postfix
                    postfix = infix_to_postfix(line)

                    print("\n[RESUMEN]")
                    print(f"Expresión original: {line}")
                    print(f"Notación postfix: {postfix}")
                    print("=" * 60)

                except Exception as e:
                    print(f"[ERROR] Línea {line_num}: {str(e)}")
                    print("=" * 60)

    except FileNotFoundError:
        print(f"[ERROR] Archivo no encontrado: {archivo_expresiones}")


if __name__ == "__main__":
    main()