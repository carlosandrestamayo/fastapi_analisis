from sympy import sympify, symbols, lambdify, diff
from sympy.core.sympify import SympifyError

def convert_to_decimal(n, decimales):
    
    formato = f"{{:.{decimales}f}}"
    return formato.format(n)
    
def evaluate_function(fn, a, decimales = 4):
    try:
        x = symbols('x')
        f = lambdify(x,fn)
        return round(f(a), decimales)
    except TypeError as e:
        print(e)
    
    
def teorema_bolzano(fn, a, b, decimales):
    fa = evaluate_function(fn, a, decimales)
    fb = evaluate_function(fn, b, decimales)
    
    if fa * fb < 0:
        return True, "Existen Raices en el intervalo"
    else:
        return False, "No existe raices en este intervalo"

def error_absoluto(xr_anterior, xr):
  return abs((xr - xr_anterior) / xr)

def tolerancia(xr_last, xr):
    return abs(xr- xr_last)