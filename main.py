from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from controller import get_products, create_products, delete_product
from db import SessionLocal, engine
from model import Base
import schema

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.post("/products/", response_model=schema.ProductCreate)
def create_product(request: Request, product: schema.ProductCreate, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    create_products(db=db, product=product)
    products = get_products(db, skip=skip, limit=limit)
    context = {"request": request, "products": products}
    return templates.TemplateResponse("table.html", context)


@app.get("/", response_class=HTMLResponse)
def read_products(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = get_products(db, skip=skip, limit=limit)
    context = {"request": request, "products": products}
    return templates.TemplateResponse("table.html", context)

@app.delete("/products/{product_id}")
def delete_product_api(request: Request, product_id: int, skip: int = 0, limit: int = 100,  db: Session = Depends(get_db)):
    success = delete_product(db=db, product_id=product_id)
    if success:
        products = get_products(db, skip=skip, limit=limit)
        context = {"request": request, "products": products}
        return templates.TemplateResponse("table.html", context)
    else:
        return {"message": "Product deletion failed"}, 404
