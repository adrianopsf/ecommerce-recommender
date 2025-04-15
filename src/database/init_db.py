from src.database.config import engine, Base
from src.database.models import Product, Review, User, Purchase, PurchaseItem
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

def init_db():
    """Initialize the database by creating all tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def seed_db():
    """Popula o banco de dados com dados iniciais para teste"""
    from sqlalchemy.orm import Session
    from datetime import datetime, timedelta
    import random

    # Cria uma sessão
    db = Session(bind=engine)

    try:
        # Cria usuários de teste
        users = [
            User(name="João Silva", email="joao@exemplo.com"),
            User(name="Maria Santos", email="maria@exemplo.com"),
            User(name="Pedro Oliveira", email="pedro@exemplo.com")
        ]
        db.add_all(users)
        db.commit()

        # Cria produtos de teste
        products = [
            Product(
                name="Smartphone XYZ",
                description="Último modelo com câmera de alta resolução",
                price=2999.99,
                category="Eletrônicos",
                stock=50
            ),
            Product(
                name="Notebook ABC",
                description="Notebook potente para trabalho e jogos",
                price=4999.99,
                category="Eletrônicos",
                stock=30
            ),
            Product(
                name="Fone de Ouvido Bluetooth",
                description="Áudio de alta qualidade e cancelamento de ruído",
                price=499.99,
                category="Acessórios",
                stock=100
            )
        ]
        db.add_all(products)
        db.commit()

        # Cria reviews de teste
        reviews = []
        sentiments = ["POSITIVE", "NEUTRAL", "NEGATIVE"]
        for user in users:
            for product in products:
                rating = random.randint(1, 5)
                sentiment = random.choice(sentiments)
                sentiment_score = random.uniform(0, 1)
                
                reviews.append(Review(
                    user_id=user.id,
                    product_id=product.id,
                    rating=rating,
                    text=f"Review do produto {product.name} pelo usuário {user.name}",
                    sentiment=sentiment,
                    sentiment_score=sentiment_score
                ))
        db.add_all(reviews)
        db.commit()

        # Cria compras de teste
        for user in users:
            purchase = Purchase(
                user_id=user.id,
                total_amount=0,
                status="completed"
            )
            db.add(purchase)
            db.commit()

            # Adiciona itens à compra
            total = 0
            for product in random.sample(products, random.randint(1, len(products))):
                quantity = random.randint(1, 3)
                price = product.price * quantity
                total += price

                item = PurchaseItem(
                    purchase_id=purchase.id,
                    product_id=product.id,
                    quantity=quantity,
                    price=price
                )
                db.add(item)

            # Atualiza o total da compra
            purchase.total_amount = total
            db.commit()

        print("Dados iniciais inseridos com sucesso!")

    except Exception as e:
        print(f"Erro ao inserir dados iniciais: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    seed_db() 