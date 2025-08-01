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
    while i < len(regex):
        c = regex[i]

        # Manejar caracteres escapados
        if c == '\\':
            if i + 1 < len(regex):
                formatted.append(c + regex[i + 1])
                i += 2
                continue
            else:
                formatted.append(c)
                i += 1
                continue

        formatted.append(c)

        # Verificar si necesita concatenación
        if i + 1 < len(regex):
            next_c = regex[i + 1]
            if needs_concat(c, next_c):
                formatted.append('.')
        i += 1

    return ''.join(formatted)

# Convierte expresión de infix a postifx
def infix_to_postfix(regex):

    output = []
    operator_stack = []
    formatted_re = format_regex(regex)

    i = 0
    while i < len(formatted_re):
        c = formatted_re[i]

        # Manejar caracteres escapados
        if c == '\\':
            if i + 1 < len(formatted_re):
                output.append(c + formatted_re[i + 1])
                i += 2
                continue
            else:
                output.append(c)
                i += 1
                continue

        # Si es paréntesis izquierdo, apilar
        elif c == '(':
            operator_stack.append(c)

        # Si es paréntesis derecho, desapilar hasta encontrar '('
        elif c == ')':
            while operator_stack and operator_stack[-1] != '(':
                output.append(operator_stack.pop())
            operator_stack.pop()  # Remover el '('

        # Si es un operador
        elif c in PRECEDENCE:
            while (operator_stack and operator_stack[-1] != '(' and
                   PRECEDENCE.get(operator_stack[-1], 0) >= PRECEDENCE[c]):
                output.append(operator_stack.pop())
            operator_stack.append(c)

        # Es un operando normal
        else:
            output.append(c)

        i += 1

    # Vaciar lo que quede en la pila
    while operator_stack:
        output.append(operator_stack.pop())

    return ''.join(output)


def main():

    archivo_expresiones = "expresiones.txt"

    try:
        with open(archivo_expresiones, 'r') as file:
            print("\nProcesando expresiones regulares:")
            print("=" * 40)

            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                print(f"\nExpresión original: {line}")

                # Paso 1: Formatear la expresión
                formatted = format_regex(line)
                print(f"Expresión formateada: {formatted}")

                # Paso 2: Convertir a postfix
                postfix = infix_to_postfix(line)
                print(f"Notación postfix: {postfix}")

                print("-" * 50)

    except FileNotFoundError:
        print(f"Error: No se pudo abrir el archivo {archivo_expresiones}")

if __name__ == "__main__":
    main()