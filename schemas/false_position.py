from typing import List, Literal, Optional, Union
from pydantic import BaseModel, Field

# ===============================
# 📥 User Input for False Position Method
# ===============================

class FalsePositionRequest(BaseModel):
    function: str = Field(
        ..., 
        description="Mathematical expression as a string. E.g.: 'x**3 - x - 2'"
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
        description="Number of decimal places (must be between 1 and 9)"
    )
    criterion: Literal["error_relativo", "tolerancia"] = Field(
        ..., 
        description="Stopping criterion: 'error_relativo' or 'tolerancia'"
    )
    criterion_value: float = Field(
        ..., 
        gt=0,
        description="Value for stopping criterion. Must be > 0"
    )

# ===============================
# 📊 Iteration Result
# ===============================

class FalsePositionRow(BaseModel):
    iteration: int                                  # Iteration number
    xi: float                                       # Current xi
    xs: float                                       # Current xs
    xr: float                                       # New approximation using false position
    fxi: float                                      # f(xi)
    fxs: float                                      # f(xs)
    fxr: float                                      # f(xr)
    error: Optional[Union[float, str]] = None       # Error for the iteration (can be "---" on first row)

# ===============================
# 🧾 Step-by-Step Explanation
# ===============================

class FalsePositionStep(BaseModel):
    step1: str
    step2: str
    step3: str
    step4: str
    step5: str
    step6: str
    step7: str
    step8: str
    step9: str
    step10: str
    step11: str

# ===============================
# 📦 Full Success Response
# ===============================

class FalsePositionData(BaseModel):
    root: float                         # Final approximated root
    message_detention: str             # Message explaining why the method stopped
    headers: List[str]                 # Table headers
    rows: List[FalsePositionRow]       # Iteration table
    steps: List[FalsePositionStep]     # Detailed steps

# ===============================
# 📤 Final Response Model
# ===============================

class FalsePositionResponse(BaseModel):
    success: bool                              # True if method completed successfully
    message: str                               # General success or error message
    data: Optional[FalsePositionData] = None   # Detailed results (None if error)
