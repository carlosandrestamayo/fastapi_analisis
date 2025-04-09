from fastapi import APIRouter, HTTPException
from schemas.biseccion import BisectionRequest, BisectionResponse
from schemas.bolzano import BolzanoRequest, BolzanoResponse
from methods.bolzano import teorema_bolzano
from methods.biseccion import bisection_method
from pydantic import BaseModel, ValidationError

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
def bisection(request: BisectionRequest):
    try:
        response = bisection_method(request)
        #print(response)
        return response
    
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=f"Error de validación: {e.errors()}"
        )
    
    except Exception as e:
        print(e)

        raise HTTPException(status_code=400, detail={"success": False, "message": str(e)})
        # return BisectionResponse(
        #     success= False,
        #     message= str(e),
        #     data= None
        # )
