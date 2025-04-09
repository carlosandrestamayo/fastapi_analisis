from fastapi import FastAPI

from routers import unit1

app = FastAPI()
app.include_router(unit1.router)

@app.get("/")
def read_root():
    return {"FASTAPI Análisis Numérico"}



