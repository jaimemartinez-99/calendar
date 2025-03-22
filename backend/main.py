import os
import uuid
from pymongo import MongoClient
from typing import List
from datetime import datetime
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)


db = client[db]
collection = db[db_collection]

class Event(BaseModel):
    title: str
    dates: List[str]

class DateRequest(BaseModel):
    uuid: str
    events: List[Event]

async def save_dates(uuid: str, events: List[Event]):
    existing_entry = collection.find_one({"uuid": uuid})
    
    if existing_entry:
        # Si ya existe el uuid, actualizamos los eventos
        updated_events = existing_entry["events"]
        
        for event in events:
            # Verificamos si el evento ya existe, si no, lo agregamos
            existing_event = next((e for e in updated_events if e["title"].lower() == event.title.lower()), None)
            if existing_event:
                # Si el evento ya existe, actualizamos las fechas
                existing_event["dates"] = list(set(existing_event["dates"] + event.dates))
            else:
                updated_events.append(event.dict())  # Añadir nuevo evento
        
        # Actualizamos la base de datos
        collection.update_one({"uuid": uuid}, {"$set": {"events": updated_events}})
        return {"uuid": uuid, "events": updated_events}
    
    else:
        # Si no existe, creamos una nueva entrada
        logger.info(f"Inserting new document with uuid: {uuid}")

        document = {
            "uuid": uuid,
            "events": [event.dict() for event in events],
        }
        collection.insert_one(document)
        return document

@app.post("/save-dates/")
async def save_dates_endpoint(request: DateRequest):
    document = await save_dates(request.uuid, request.events)
    return {"message": "Fechas guardadas o actualizadas"}

@app.get("/retrieve-dates/{uuid}")
async def get_map(uuid: str):
    document = collection.find_one({"uuid": uuid})
    if document:
        return {"uuid": document["uuid"], "events": document["events"]}
    else:
        raise HTTPException(status_code=404, detail="Map not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)