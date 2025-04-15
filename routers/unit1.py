from fastapi import APIRouter, HTTPException, Request
from schemas.biseccion import BisectionRequest, BisectionResponse
from schemas.bolzano import BolzanoRequest, BolzanoResponse
from methods.bolzano import teorema_bolzano
from methods.biseccion import bisection_method
from pydantic import BaseModel, ValidationError
from typing import List, Optional
from sympy import symbols, sympify, lambdify

router = APIRouter()

@router.post('/bolzano', response_model=BolzanoResponse)
def bolzano(request: BolzanoRequest):
    try:
        return teorema_bolzano(request)
    except Exception as e:
        return BisectionResponse(
            success= False,
            message= str(e),
            data= None
        )

@router.post('/biseccion', response_model=BisectionResponse)
async def bisection(request: Request)-> BisectionRequest:

    try:
        body = await request.json()

        #Crear en util la validacion de funciones de sympy para una sola variable

        try:
            x = symbols("x")
            expr = sympify(body.get("function"))
            f = lambdify(x, expr, modules=["math"])
        except Exception as e:
            return BisectionResponse(success=False, message=f"Función no válida: {e}", data=None)

        # Validación de los valores del request de la clase BisectionRequest
        try:
            request_data = BisectionRequest(**body)
        except ValidationError as e:
            return BisectionResponse(
                success=False,
                message=f"Error de validación: {str(e)}",
                data=None
            )
        
        #Validar que criterion_value sea mayor que cero sin embargo esa condición esta dada en el schema
        #Validar que criterion_value sea entero si criterion es "max_iter"

        # # ✅ Validación adicional: si criterion es max_iter, el valor debe ser entero
        # if request_data.criterion == "max_iter" and not isinstance(request_data.criterion_value, int):
        #     return BisectionResponse(
        #         success=False,
        #         message="El valor de 'criterion_value' debe ser un entero si el criterio es 'max_iter'.",
        #         data=None
        #     )



        # Ejecución del método
        response = await bisection_method(request_data)
        #return await bisection_method(request_data)
        return response 
        # return BisectionResponse(
        #     success=True,
        #     message="Method completed!",
        #     data= None
        # )    
    
    except Exception as e:
        return BisectionResponse(
            success=False, 
            message=f"Error inesperado: {str(e)}", 
            data=None
        )


