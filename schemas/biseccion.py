
from typing import List, Union, Literal, Optional
from pydantic import BaseModel, Field


class BisectionRequest(BaseModel):
    function: str = Field(
        ..., 
        description="Mathematical expression as a string, e.g., 'x**3 - x - 2'"
    )
    xi: float = Field(
        ..., 
        description="Lower bound of the interval"
    )
    xs: float = Field(
        ..., 
        description="Upper bound of the interval"
    )
    decimals: int = Field(
        ..., 
        gt=0, 
        lt=10, 
        description="Number of decimal places (must be > 0 and < 10)"
    )
    criterion: Literal[
        "error_absoluto", 
        "error_relativo", 
        "tolerancia", 
        "max_iter"
    ] = Field(
        ..., 
        description="Stopping criterion for the method"
    )
    criterion_value: Union[float, int] = Field(
        ..., 
        description="Value for the stopping criterion. Must be int if criterio is 'max_iter'"
    )


class BisectionRow(BaseModel):
    iteration: int
    xi: float
    xs: float
    xr: float
    fxi: float
    fxs: float
    fxr: float
    error: Optional[float]  # Puede ser None en la primera iteración


class BisectionStep(BaseModel):
    step1: str
    step2: str
    step3: str
    step4: str
    step5: str
    step6: str
    step7: str
    step8: str


class BisectionData(BaseModel):
    root: float                               # Valor final de la raíz encontrada
    headers: List[str]                        # Nombres de las columnas para tabla
    rows: List[BisectionRow]                  # Iteraciones con sus datos
    steps: List[BisectionStep]                # Explicación paso a paso
    message_detention: str                    # Mensaje que explica por qué se detuvo


class BisectionResponse(BaseModel):
    success: bool                             # Indica si se ejecutó correctamente
    message: str                              # Mensaje general de éxito o error
    data: Optional[BisectionData]             # Información detallada (puede ser None en errores)


