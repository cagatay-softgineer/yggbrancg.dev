from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse  # noqa: F401
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine

app = FastAPI()

# Setup Jinja2 templates for rendering HTML
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates setup
templates = Jinja2Templates(directory="app/templates")

# Initialize the database
models.Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Homepage route
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# About page route
@app.get("/about/")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

# Contact page route
@app.get("/contact/")
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

# Handle feedback form submissions
@app.post("/send-feedback/")
async def send_feedback(
    request: Request, 
    name: str = Form(...), 
    email: str = Form(...), 
    message: str = Form(...),
    db: Session = Depends(get_db)
):
    # Store feedback in the database
    feedback = models.Feedback(name=name, email=email, message=message)
    db.add(feedback)
    db.commit()
    
    return templates.TemplateResponse("feedback_received.html", {"request": request, "name": name})

@app.get("/admin/feedback")
async def admin_feedback(request: Request, password: str, db: Session = Depends(get_db)):
    if password != "Cagatay233!":
        return {"error": "Unauthorized access"}
    feedbacks = db.query(models.Feedback).all()
    return templates.TemplateResponse("admin_feedback.html", {"request": request, "feedbacks": feedbacks})
