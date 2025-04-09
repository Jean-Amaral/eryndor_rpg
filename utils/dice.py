import random
import re

def roll_dice(expression):
    """
    Interpreta e executa uma rolagem de dados no formato 'XdY+Z'.
    Exemplo de uso:
    - '1d20' → rola 1 dado de 20 lados
    - '2d6+3' → rola 2 dados de 6 lados e soma +3 ao total
    - '3d8-2' → rola 3 dados de 8 lados e subtrai 2

    Retorna um dicionário com:
    - rolagens: lista dos dados
    - modificador: valor numérico adicional
    - total: soma total com modificador
    - expressao: a expressão original
    """
    # Expressão regular para identificar 'XdY+Z'
    pattern = r'^(\\d*)d(\\d+)([+-]\\d+)?$'
    match = re.match(pattern, expression.replace(" ", ""))
    
    if not match:
        return {
            'erro': 'Expressão inválida',
            'expressao': expression
        }

    qtd = int(match.group(1)) if match.group(1) else 1
    faces = int(match.group(2))
    mod = int(match.group(3)) if match.group(3) else 0

    # Limites para evitar abuso do sistema
    if qtd > 100 or faces > 20 or qtd < 1 or faces < 2:
        return {
            'erro': 'Limite de dados excedido ou valor inválido',
            'expressao': expression
        }

    rolagens = [random.randint(1, faces) for _ in range(qtd)]
    total = sum(rolagens) + mod

    return {
        'expressao': expression,
        'rolagens': rolagens,
        'modificador': mod,
        'total': total
    }
