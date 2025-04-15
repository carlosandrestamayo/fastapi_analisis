from fastapi import APIRouter, HTTPException, Response # type: ignore
from sympy import symbols, sympify, lambdify
from methods.util import teorema_bolzano, convert_to_decimal, error_absoluto, evaluate_function, tolerancia, error_relativo
from schemas.biseccion import BisectionRequest, BisectionRow, BisectionResponse, BisectionData, BisectionStep

from pydantic import BaseModel, ValidationError

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from sympy import symbols, sympify, lambdify
from typing import List, Optional


MAX_ITER = 30

def calculate_xr_biseccion(a, b, decimales):
    return round((a + b) / 2, decimales)

async def bisection_method(data: BisectionRequest ):
    try:
        
        ## Descomponer los valores del request
        fn = data.function
        xi = data.xi
        xs = data.xs
        decimals = data.decimals
        criterion = data.criterion
        criterion_value = data.criterion_value

        ## Inicializar variables de control
        iteration = 1
        xr_last = None
        xr = None
        headers = ["iteration", "xi", "xs", "xr", "fxi", "fxs", "fxr", "error"]
        rows: List[BisectionRow] = []
        steps: List[BisectionStep] = []
        error = None
        step = {}

        #isinstance(valor, int) or (isinstance(valor, float) and valor.is_integer())

        ## Validación específica para max_iter: debe ser entero
        if criterion == "max_iter":
            if not criterion_value.is_integer():
                return BisectionResponse(
                    success=False,
                    message="El máximo de iteraciones debe ser un valor entero ",
                    data=None
                )        

        ## Validar que xi sea menor que xs
        if xi >= xs:
            #raise ValueError("Xi debe ser menor que Xs")
            return BisectionResponse(
                    success=False,
                    message="Xi debe ser menor que Xs",
                    data=None
                )    

       
        ## Validar que se cumpla el Teorema de Bolzano
        value_bolzano, msg_bolzano = teorema_bolzano(fn, xi, xs, decimals)
        if not value_bolzano:
            return BisectionResponse(
                    success=False,
                    message=msg_bolzano,
                    data=None
                )    
        
        while True:
            ## Calcular nuevo xr
            xr = calculate_xr_biseccion(xi, xs, decimals)

            # fxi = convert_to_decimal(evaluate_function(fn, xi, decimals), decimals)
            # fxs = convert_to_decimal(evaluate_function(fn, xs, decimals), decimals)
            # fxr = convert_to_decimal(evaluate_function(fn, xr, decimals), decimals)

            ## Evaluar función en los puntos xi, xs y xr
            fxi = evaluate_function(fn, xi, decimals)
            fxs = evaluate_function(fn, xs, decimals)
            fxr = evaluate_function(fn, xr, decimals)
            
            ## Agregar la fila a la tabla de resultados
            rows.append(BisectionRow(
                iteration= iteration,
                xi= float(xi),
                xs= float(xs),
                xr= xr,
                fxi = convert_to_decimal(fxi, decimals),
                fxs = convert_to_decimal(fxs, decimals),
                fxr = convert_to_decimal(fxr, decimals), 
                error = -1 if iteration == 1 else error
            ))
          
            ## Construcción del paso a paso explicativo
            step = {
                "step1": str(iteration),
                "step2": f"xi = {xi:.{decimals}f}, xs = {xs:.{decimals}f}, xr = {xr:.{decimals}f}",
                "step3": f"Intervalos de [{xi}, {xr}] y [{xr}, {xs}]",
                "step4": "f(Xi) =" + fn.replace('x',f"({xi})") + " = " + convert_to_decimal(fxi, decimals),
                "step5": "f(Xs) =" + fn.replace('x',f"({xs})") + " = " + convert_to_decimal(fxs, decimals),
                "step6": "f(Xr) =" + fn.replace('x',f"({xr})") + " = " + convert_to_decimal(fxr, decimals),
                "step7": "",
                "step8": ""
            }


            ## Verificar si se encontró la raíz exacta
            if fxr == 0:
                return BisectionResponse(
                    success= True,
                    message="Method Completed",
                    data={
                           "root":xr,
                           "headers":headers,
                           "rows": rows,
                           "steps": steps,
                           "message_detention":f"El método encontro la raíz {xr}"
                        }
                )
            elif fxi * fxr < 0:
                xs = xr
                step["step7"] = f"La raiz se encuentra en el intervalo [{xi}, {xs}] porque f(xi)*f(xr) < 0"
                step["step8"] = f"Hacemos Xs = {xr}"
            else:
                xi = xr
                step["step7"] = f"La raiz se encuentra en el intervalo [{xi}, {xs}] porque f(xi)*f(xr) no es < 0"
                step["step8"] = f"Hacemos Xi = {xr}"

            steps.append(step)

            ## Verificar si se cumple el criterio de parada
            finished = False
            message_detention = ""
            ## Diccionario para asociar encabezado por criterio
            criterio_headers = {
                "max_iter": "Er",
                "error_relativo": "Er",
                "tolerancia": "Tolerancia"
            }

            # Calcular error solo si no es la primera iteración

            # if iteration == MAX_ITER:
            #      #error = error_relativo(xr_last, xr, decimals)
            #      return BisectionResponse(
            #           success=True,
            #           message="Method completed",
            #           data={
            #                "root":xr,
            #                "headers":["i","xi","xs","xr","fxi","fxs","fxr","----"],
            #                "rows": rows,
            #                "steps": steps,
            #                "message_detention":f"El método realizo { MAX_ITER} iteraciones, el máximo soportado"
            #             }
            #      )


            if iteration > 1:
                if criterion == "tolerancia":
                    error = tolerancia(xr_last, xr, decimals)
                else:
                    error = error_relativo(xr_last, xr, decimals)

            # Evaluar criterios de parada
            if criterion == "max_iter":
                if iteration == criterion_value:
                    finished = True
                    message_detention = f"El método realizó {criterion_value} iteraciones"
                    headers[-1] = criterio_headers[criterion]

            elif criterion == "error_relativo" and iteration > 1:
                if error <= criterion_value:
                    finished = True
                    message_detention = (
                        f"El método realizó {iteration} iteraciones y un error relativo de {error}"
                    )
                    headers[-1] = criterio_headers[criterion]

            elif criterion == "tolerancia" and iteration > 1:
                if error <= criterion_value:
                    finished = True
                    message_detention = (
                        f"El método realizó {iteration} iteraciones y una tolerancia de {error}"
                    )
                    headers[-1] = criterio_headers[criterion]

            ## Retornar si se cumplió algún criterio de parada
            if finished:
                return BisectionResponse(
                    success=True,
                    message="Method completed",
                    data={
                        "root": xr,
                        "headers": headers,
                        "rows": rows,
                        "steps": steps,
                        "message_detention": message_detention,
                    }
                )

            # Aumentar iteración si no se ha terminado, Preparar para la siguiente iteración
            iteration += 1
            xr_last = round(xr, decimals)

    except Exception as e:
        ## Captura de errores imprevistos
        return BisectionResponse(
            success=False,
            message=str(e),
            data= None
        )