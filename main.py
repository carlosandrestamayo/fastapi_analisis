from fastapi import FastAPI

from methods.biseccion import bisection_method
from schemas.biseccion import BisectionRequest, BisectionResponse
from schemas.bolzano import BolzanoRequest, BolzanoResponse
from methods.bolzano import verificar_teorema_bolzano

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello World"}

@app.post('/bolzano', response_model=BolzanoResponse)
def bolzano(request: BolzanoRequest):
    try:
        return verificar_teorema_bolzano(request)
    except Exception as e:
        return BisectionResponse(
            success= False,
            message= str(e),
            data= None
        )

@app.post('/biseccion', response_model=BisectionResponse)
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


