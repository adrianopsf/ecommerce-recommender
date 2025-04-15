from database.config import get_db
from database.models import Product, Review, Purchase, PurchaseItem
from sqlalchemy import func
import pandas as pd

def check_database_data():
    db = next(get_db())
    try:
        # Verifica dados de compras
        print("\n=== Dados de Compras ===")
        purchases = db.query(Purchase).all()
        print(f"Total de compras: {len(purchases)}")
        for purchase in purchases:
            print(f"ID: {purchase.id}, Data: {purchase.created_at}, Usuário: {purchase.user_id}")

        # Verifica dados de itens de compra
        print("\n=== Dados de Itens de Compra ===")
        purchase_items = db.query(PurchaseItem).all()
        print(f"Total de itens: {len(purchase_items)}")
        for item in purchase_items:
            print(f"ID: {item.id}, Compra: {item.purchase_id}, Produto: {item.product_id}, Quantidade: {item.quantity}, Preço: {item.price}")

        # Verifica dados de avaliações
        print("\n=== Dados de Avaliações ===")
        reviews = db.query(Review).all()
        print(f"Total de avaliações: {len(reviews)}")
        for review in reviews:
            print(f"ID: {review.id}, Produto: {review.product_id}, Sentimento: {review.sentiment}, Score: {review.sentiment_score}")

        # Verifica dados de produtos
        print("\n=== Dados de Produtos ===")
        products = db.query(Product).all()
        print(f"Total de produtos: {len(products)}")
        for product in products:
            print(f"ID: {product.id}, Nome: {product.name}, Categoria: {product.category}, Preço: {product.price}")

    finally:
        db.close()

if __name__ == "__main__":
    check_database_data() 