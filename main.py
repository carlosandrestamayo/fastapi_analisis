from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import unit1

app = FastAPI()

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#app = FastAPI()
app.include_router(unit1.router)

@app.get("/")
def read_root():
    return {"FASTAPI Análisis Numérico"}



