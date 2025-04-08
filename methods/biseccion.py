from sympy import symbols, sympify, lambdify
from methods.util import teorema_bolzano, convert_to_decimal, error_absoluto, evaluate_function, tolerancia
from schemas.biseccion import BisectionRequest, BisectionRow, BisectionResponse

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

            error = -1 if iteration == 1 else error
            
            row = {
                "iteration":iteration, 
                "xi":float(xi), 
                "xs":xs, 
                "xr":xr, 
                "fxi": fxi, 
                "fxs": fxs, 
                "fxr":fxr, 
                "error":error
            }

            rows.append(row)
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
            iteration += 1

            if iteration == 4:
                 return BisectionResponse(
                      success=True,
                      message="Method completed",
                      data={
                           "root":xr,
                           "headers":["i","xi","xs","xr","fxi","fxs","fxr","error"],
                           "rows": rows,
                           "steps": steps,
                           "message_detention":"message_detention",
                        }
                 )

    except Exception as e:
         return BisectionResponse(
              success=False,
              message=str(e),
              data=None
         )

