from fastapi import APIRouter, HTTPException
from schemas.biseccion import BisectionRequest, BisectionResponse
from schemas.bolzano import BolzanoRequest, BolzanoResponse
from methods.bolzano import teorema_bolzano
from methods.biseccion import bisection_method

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
        return bisection_method(request)
    
    except Exception as e:
        print(e)
        return BisectionResponse(
            success= False,
            message= str(e),
            data= None
        )
