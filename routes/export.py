from io import BytesIO
from pymongo import MongoClient
import pandas as pd
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from datetime import date
import time

router = APIRouter()

from Database.Database import db
rooms = db['rooms']
modules = db['modules']
dozents = db['dozent']

def removeID(items):
    tmp = []

    for item in items:
        if "id" in item:
            item.pop("id")
        if "absences" in item:
            item.pop("absences")
              
        tmp.append(item)
    return tmp

@router.get("/export/excel/basicdata/", summary="Export Basicdata to xlsx",
        description="Export Dozent, Module and Room to a xlsx file",
        tags=["Export"],)
async def export_data():
    modulesData = modules.find()
    dozentsData = dozents.find()
    roomsData = rooms.find()

    modulesData = removeID(modulesData)
    dozentsData = removeID(dozentsData)
    roomsData = removeID(roomsData)

    pandaModule = pd.DataFrame(modulesData)
    pandaDozent = pd.DataFrame(dozentsData)
    pandaRoom = pd.DataFrame(roomsData)    

    buffer = BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        pandaModule.to_excel(writer, sheet_name='Modules', index=False)
        pandaDozent.to_excel(writer, sheet_name='Dozents', index=False)
        pandaRoom.to_excel(writer, sheet_name='Rooms', index=False)

    writer.close()

    filename = str(date.today()) + "_" + str(time.strftime("%H-%M-%S", time.localtime())) + "_basicdata" + ".xlsx"

    return StreamingResponse(
        BytesIO(buffer.getvalue()),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={"Content-Disposition": f"attachment; filename={filename}"}
)