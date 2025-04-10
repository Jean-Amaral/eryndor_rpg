import random
import re

def roll_dice(expression):
    """
    Interpreta e executa uma rolagem de dados no formato composto.
    Exemplos:
      'd20'         -> Interpreta como '1d20'
      '2d6'         -> Rola 2 dados de 6 lados
      '2d6+3'       -> Rola 2 dados de 6 lados e soma 3
      '3d8-2'       -> Rola 3 dados de 8 lados e subtrai 2
    Retorna um dicionário com os resultados:
      {
         'expressao': <a expressão original>,
         'rolagens': [resultado1, resultado2, ...],
         'modificador': <valor do modificador>,
         'total': <soma total dos dados + modificador>
      }
    Se a expressão for inválida, retorna:
      { 'error': 'Expressão inválida', 'expressao': <expressão> }
    """
    expression = expression.strip()
    # Aceita expressões do tipo: [n]dX[+/-Y]
    match = re.match(r'^(\d*)d(\d+)([+-]\d+)?$', expression)
    if not match:
        return {'error': 'Expressão inválida', 'expressao': expression}

    qtd_str, faces_str, mod_str = match.groups()
    qtd = int(qtd_str) if qtd_str and qtd_str != "" else 1
    faces = int(faces_str)
    mod = int(mod_str) if mod_str else 0

    # Permitimos apenas dados: d4, d6, d8, d10, d12, d20
    if faces not in [4, 6, 8, 10, 12, 20]:
        return {
            'error': 'Tipo de dado inválido. Só são permitidos d4, d6, d8, d10, d12 e d20.',
            'expressao': expression
        }

    if qtd < 1 or qtd > 100:
        return {'error': 'Quantidade de dados inválida (deve ser entre 1 e 100).', 'expressao': expression}

    rolagens = [random.randint(1, faces) for _ in range(qtd)]
    total = sum(rolagens) + mod

    return {
        'expressao': expression,
        'rolagens': rolagens,
        'modificador': mod,
        'total': total
    }
