from fastapi import FastAPI, Depends, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import database

app = FastAPI()

# Automatically initialize local database tables on launch
database.init_db()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def read_dashboard():
    """Reads the static visual interface layout and serves it straight to the user browser"""
    with open("index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())

@app.post("/api/v1/prescriptions/save")
def save_prescription(
    customer_name: str = Form(...),
    mobile: str = Form(...),
    od_sph: float = Form(...),
    os_sph: float = Form(...),
    db: Session = Depends(get_db)
):
    """Processes entry forms directly from your screen and writes data logs cleanly"""
    # 1. Store clean customer entries
    new_customer = database.Customer(first_name=customer_name, mobile=mobile)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    
    # 2. Append biometric prescriptions right onto profile matching tables
    new_rx = database.Prescription(
        customer_id=new_customer.id,
        od_sph=od_sph,
        os_sph=os_sph
    )
    db.add(new_rx)
    db.commit()
    
    return {"status": "Success", "message": f"Prescription recorded for profile ID: {new_customer.id}"}
