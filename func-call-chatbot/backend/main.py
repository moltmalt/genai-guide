from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os, json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = "../mock-db"

@app.get("/products")
def get_products():
    file_path = os.path.join(BASE_DIR, "shirt.json")
    with open(file_path, "r") as f:
        data = json.load(f)
    return JSONResponse(data)

@app.get("/cart")
def get_cart():
    file_path = os.path.join(BASE_DIR, "cart.json")
    with open(file_path, "r") as f:
        data = json.load(f)
    return JSONResponse(data)

@app.get("/order")
def get_order():
    file_path = os.path.join(BASE_DIR, "order.json")
    with open(file_path, "r") as f:
        data = json.load(f)
    return JSONResponse(data)