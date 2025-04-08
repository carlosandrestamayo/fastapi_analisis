from fastapi import APIRouter, HTTPException
from schemas.biseccion import BisectionRequest, BisectionResponse

router = APIRouter()

@router.post("/", response_model=BisectionResponse)
def calcular_biseccion(request: BisectionRequest):
    return {
        
    }