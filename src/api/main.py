from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from typing import List, Optional
import numpy as np

# Carrega variáveis de ambiente
load_dotenv()

app = FastAPI(
    title="E-commerce Recommendation API",
    description="API para sistema de recomendação e análise de sentimento",
    version="1.0.0"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de dados
class Product(BaseModel):
    id: int
    name: str
    category: str
    price: float
    description: str

class User(BaseModel):
    id: int
    name: str
    email: str

class Review(BaseModel):
    id: int
    user_id: int
    product_id: int
    rating: int
    text: str
    sentiment: Optional[float] = None

# Rotas da API
@app.get("/")
async def root():
    return {"message": "Bem-vindo à API de Recomendação de E-commerce"}

@app.get("/products/", response_model=List[Product])
async def get_products():
    # TODO: Implementar busca de produtos do banco de dados
    return []

@app.get("/products/{product_id}/recommendations", response_model=List[Product])
async def get_recommendations(product_id: int, limit: int = 5):
    # TODO: Implementar sistema de recomendação
    return []

@app.post("/reviews/", response_model=Review)
async def create_review(review: Review):
    # TODO: Implementar análise de sentimento e armazenamento
    return review

@app.get("/users/{user_id}/recommendations", response_model=List[Product])
async def get_user_recommendations(user_id: int, limit: int = 5):
    # TODO: Implementar recomendações personalizadas
    return []

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=True
    ) 