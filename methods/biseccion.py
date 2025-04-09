from sympy import symbols, sympify, lambdify
from methods.util import teorema_bolzano, convert_to_decimal, error_absoluto, evaluate_function, tolerancia, error_relativo
from schemas.biseccion import BisectionRequest, BisectionRow, BisectionResponse
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ValidationError

MAX_ITER = 30

def calculate_xr_biseccion(a, b, decimales):
    return round((a + b) / 2, decimales)

def bisection_method(data: BisectionRequest ):
    
    try:
        #Bisection Request
        fn = data.function
        xi = data.xi
        xs = data.xs
        decimals = data.decimals
        criterion = data.criterion
        criterion_value = data.criterion_value

        #Inicializar datos
        iteration = 1
        xr_last = 0
        xr = 0
        steps = []
        rows = []
        error = None
        step = {}
        
        if criterion == "max_iter":
            if not criterion_value.is_integer():
                raise ValueError("El máximo de iteraciones debe ser un valor entero ")        

        if xi >= xs:
            raise ValueError("Xi debe ser menor que Xs")

        if not teorema_bolzano(fn, xi, xs, decimals)[0]:
            raise ValueError(teorema_bolzano(fn, xi, xs, decimals)[1])
        

        while True:
            xr_last = round(xr, decimals)
            xr = calculate_xr_biseccion(xi, xs, decimals)

            fxi = convert_to_decimal(evaluate_function(fn, xi, decimals), decimals)
            fxs = convert_to_decimal(evaluate_function(fn, xs, decimals), decimals)
            fxr = convert_to_decimal(evaluate_function(fn, xr, decimals), decimals)

            
            rows.append(BisectionRow(
                iteration= iteration,
                xi= float(xi),
                xs= float(xs),
                xr= xr,
                fxi = fxi,
                fxs = fxs,
                fxr = fxr, 
                error = -1 if iteration == 1 else error
            ))
            
            row = {
                "iteration":iteration, 
                "xi":float(xi), 
                "xs":xs, 
                "xr":xr, 
                "fxi": fxi, 
                "fxs": fxs, 
                "fxr":fxr, 
                "error": -1 if iteration == 1 else error
            }

            #rows.append(row)
            #step = {}
            step = {
                "step1": str(iteration),
                "step2": f"xi = {xi:.{decimals}f}, xs = {xs:.{decimals}f}, xr = {xr:.{decimals}f}",
                "step3": f"Intervalos de [{xi}, {xr}] y [{xr}, {xs}]",
                "step4": "f(Xi) =" + fn.replace('x',f"({xi})") + " = " + fxi,
                "step5": "f(Xs) =" + fn.replace('x',f"({xs})") + " = " + fxs,
                "step6": "f(Xr) =" + fn.replace('x',f"({xr})") + " = " + fxr,
                "step7": "",
                "step8": ""
            }

            if evaluate_function(fn, xi, decimals) *  evaluate_function(fn, xr, decimals)== 0:
                 xr = 0
            elif evaluate_function(fn, xi, decimals) * evaluate_function(fn, xr, decimals) < 0:
                xs = xr
                step["step7"] = f"La raiz se encuentra en el intervalo [{xi}, {xs}] porque f(xi)*f(xr) < 0"
                step["step8"] = f"Hacemos Xs = {xr}"
            elif evaluate_function(fn, xs, decimals) * evaluate_function(fn, xr, decimals) < 0:
                xi = xr
                step["step7"] = f"La raiz se encuentra en el intervalo [{xi}, {xs}] porque f(xi)*f(xr) no es < 0"
                step["step8"] = f"Hacemos Xi = {xr}"

            steps.append(step)
            

            #Criterios de Parada

            if iteration == MAX_ITER:
                 #error = error_relativo(xr_last, xr, decimals)
                 return BisectionResponse(
                      success=True,
                      message="Method completed",
                      data={
                           "root":xr,
                           "headers":["i","xi","xs","xr","fxi","fxs","fxr","error"],
                           "rows": rows,
                           "steps": steps,
                           "message_detention":f"El método realizo { MAX_ITER} iteraciones, el máximo soportado"
                        }
                 )
            
            
            finished = False
            message_detention = ""
            headers = []
            if criterion == "max_iter":
                if iteration > 1:
                    error = error_relativo(xr_last, xr, decimals)
                if iteration == criterion_value:
                    finished = True
                    message_detention =f"El método realizo { criterion_value } iteraciones"
                    headers = ["i","xi","xs","xr","fxi","fxs","fxr","Er"]
              

            if criterion == "error_relativo":
                if iteration > 1:
                    error = error_relativo(xr_last, xr, decimals)
                    relativo = error_relativo(xr_last, xr, decimals)
                    if relativo <= criterion_value:
                        finished = True
                        message_detention = f"El método realizo { iteration } iteraciones y un error relativo de {relativo} "
                        headers = ["i","xi","xs","xr","fxi","fxs","fxr","Er"]
                                            
            if criterion == "tolerancia":
                if iteration > 1:
                    error = tolerancia(xr_last, xr, decimals)
                    tol = error_relativo(xr_last, xr, decimals)
                    if tol <= criterion_value:
                        finished = True
                        message_detention = f"El método realizo { iteration } iteraciones y una tolerancia de {tol} "
                        headers = ["i","xi","xs","xr","fxi","fxs","fxr","Tolerancia"]
                        
            
            if finished:
                return BisectionResponse(
                    success=True,
                    message="Method completed",
                    data={
                        "root":xr,
                        "headers": headers,
                        "rows": rows,
                        "steps": steps,
                        "message_detention": message_detention 
                        }
                )

            iteration += 1
            
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=f"Error de validación: {e.errors()}"
        )

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=400, detail={"success": False, "message": str(e)})
        # return BisectionResponse(
        #       success=False,
        #       message=str(e),
        #       data=None
        #  )

