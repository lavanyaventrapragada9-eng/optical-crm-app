from fastapi import FastAPI, Depends, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import database

app = FastAPI()
database.init_db()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def read_dashboard(db: Session = Depends(get_db)):
    """Reads the static visual interface layout and serves it straight to the user browser"""
    with open("index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())

# 🆕 NEW: API to fetch all live inventory items
@app.get("/api/v1/inventory/list")
def get_inventory(db: Session = Depends(get_db)):
    items = db.query(database.InventoryItem).all()
    return items

# 🆕 NEW: API to add a new inventory frame item
@app.post("/api/v1/inventory/add")
def add_inventory(
    sku_code: str = Form(...),
    product_name: str = Form(...),
    brand: str = Form(...),
    category: str = Form(...),
    stock_count: int = Form(...),
    retail_price: float = Form(...),
    db: Session = Depends(get_db)
):
    new_item = database.InventoryItem(
        sku_code=sku_code,
        product_name=product_name,
        brand=brand,
        category=category,
        stock_count=stock_count,
        retail_price=retail_price
    )
    db.add(new_item)
    db.commit()
    return {"status": "Success", "message": f"Product {product_name} added to stock."}

@app.post("/api/v1/prescriptions/save")
def save_prescription(
    customer_name: str = Form(...),
    mobile: str = Form(...),
    od_sph: float = Form(...),
    os_sph: float = Form(...),
    db: Session = Depends(get_db)
):
    new_customer = database.Customer(first_name=customer_name, mobile=mobile)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    
    new_rx = database.Prescription(customer_id=new_customer.id, od_sph=od_sph, os_sph=os_sph)
    db.add(new_rx)
    db.commit()
    return {"status": "Success", "message": f"Prescription recorded successfully."}
