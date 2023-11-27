from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import schema
import model

def get_detail_product(db: Session, product_id: int):
    return db.query(model.Product).filter(model.Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Product).offset(skip).limit(limit).all()

def create_products(db: Session, product: schema.ProductCreate):
    db_product = model.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int) -> bool:
    try:
        # Optional: Check if the product exists before deleting
        product = db.query(model.Product).filter(model.Product.id == product_id).first()
        if not product:
            return False  # Product not found

        # Delete the product
        db.query(model.Product).filter(model.Product.id == product_id).delete()
        db.commit()
        return True  # Successfully deleted
    except SQLAlchemyError as e:
        print("An error occurred:", e)
        db.rollback()
        return False  # Deletion failed
