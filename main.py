import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Service, Project, TeamMember, Inquiry

app = FastAPI(title="Geo Transect API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Geo Transect API running"}

# CMS-like content endpoints
@app.get("/api/services", response_model=List[Service])
def list_services():
    docs = get_documents("service")
    return [Service(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]

@app.post("/api/services", status_code=201)
def create_service(service: Service):
    try:
        inserted_id = create_document("service", service)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/projects", response_model=List[Project])
def list_projects():
    docs = get_documents("project")
    return [Project(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]

@app.post("/api/projects", status_code=201)
def create_project(project: Project):
    try:
        inserted_id = create_document("project", project)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/team", response_model=List[TeamMember])
def list_team():
    docs = get_documents("teammember")
    return [TeamMember(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]

@app.post("/api/team", status_code=201)
def create_team_member(member: TeamMember):
    try:
        inserted_id = create_document("teammember", member)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Contact form endpoint
class InquiryResponse(BaseModel):
    status: str
    message: str

@app.post("/api/contact", response_model=InquiryResponse)
def submit_inquiry(inquiry: Inquiry):
    # Basic spam prevention: minimal content length and required fields are already validated
    if len(inquiry.message.strip()) < 10:
        raise HTTPException(status_code=400, detail="Message too short")

    # Store inquiry in DB
    try:
        create_document("inquiry", inquiry)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store inquiry: {str(e)}")

    # Email sending could be added here; for now we just acknowledge
    return InquiryResponse(status="ok", message="Thanks for reaching out. We'll get back to you shortly.")

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = os.getenv("DATABASE_NAME") or "❌ Not Set"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
