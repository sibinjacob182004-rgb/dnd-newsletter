from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr

from backend.utils.supabase_client import get_supabase_client

app = FastAPI()


class Subscriber(BaseModel):
    email: EmailStr


@app.get("/")
def root():
    return {"message": "Newsletter API running"}


@app.post("/subscribe")
def subscribe(user: Subscriber):
    supabase = get_supabase_client()

    existing = supabase.table("subscribers") \
        .select("*") \
        .eq("email", user.email) \
        .execute()

    if existing.data:
        return {"message": "Already subscribed"}

    supabase.table("subscribers") \
        .insert({
            "email": user.email,
            "subscribed": True
        }) \
        .execute()

    return {"message": "Subscribed successfully"}


@app.get("/unsubscribe")
def unsubscribe(email: str = Query(...)):
    supabase = get_supabase_client()

    response = supabase.table("subscribers") \
        .update({"subscribed": False}) \
        .eq("email", email) \
        .execute()

    if not response.data:
        raise HTTPException(status_code=404, detail="Email not found")

    return {"message": f"{email} unsubscribed successfully"}