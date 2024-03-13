from io import BytesIO
from bson import ObjectId
from pymongo import MongoClient
import pandas as pd
from fastapi import APIRouter, UploadFile
from fastapi.responses import StreamingResponse
from datetime import date
import time
import os
import numpy as np
import ast

router = APIRouter()

from Database.Database import db
rooms = db['rooms']
modules = db['modules']
dozents = db['dozent']
studyCourseCollection = db["studycourse"]
calendars = db["calendar"]
calendarentry = db["calendarEntry"]

def removeID(items):
    tmp = []

    for item in items:
        if "id" in item:
            item.pop("id")
              
        tmp.append(item)
    return tmp

@router.get("/export/excel/basicdata/", summary="Export Basicdata to xlsx",
        description="Export Dozent, Module, StudyCourse and Room to a xlsx file",
        tags=["Export"],)
async def export_data():
    modulesData = modules.find()
    dozentsData = dozents.find()
    roomsData = rooms.find()
    studyCourseData = studyCourseCollection.find()
    calendarsData = calendars.find()
    calendarentryData = calendarentry.find()

    modulesData = removeID(modulesData)
    dozentsData = removeID(dozentsData)
    roomsData = removeID(roomsData)
    studyCourseData = removeID(studyCourseData)
    calendarsData = removeID(calendarsData)
    calendarentryData = removeID(calendarentryData)

    pandaModule = pd.DataFrame(modulesData)
    pandaDozent = pd.DataFrame(dozentsData)
    pandaRoom = pd.DataFrame(roomsData)   
    pandastudyCourse = pd.DataFrame(studyCourseData)  
    pandaCalendars = pd.DataFrame(calendarsData)   
    pandaCalendarEntries = pd.DataFrame(calendarentryData)  

    buffer = BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        pandaModule.to_excel(writer, sheet_name='modules', index=False)
        pandaDozent.to_excel(writer, sheet_name='dozent', index=False)
        pandaRoom.to_excel(writer, sheet_name='rooms', index=False)
        pandastudyCourse.to_excel(writer, sheet_name='studycourse', index=False)
        pandaCalendars.to_excel(writer, sheet_name='calendar', index=False)
        pandaCalendarEntries.to_excel(writer, sheet_name='calendarEntry', index=False)
    writer.close()

    filename = str(date.today()) + "_" + str(time.strftime("%H-%M-%S", time.localtime())) + "_basicdata" + ".xlsx"

    return StreamingResponse(
        BytesIO(buffer.getvalue()),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={"Content-Disposition": f"attachment; filename={filename}"}
)

@router.post("/import/excel/basicdata/replace/",summary="Import Basicdata as xlsx",
        description="Import Dozent, Module, StudyCourse and Room to a xlsx file",
        tags=["Export"],)
async def create_upload_file(file: UploadFile):
    file_extension = os.path.splitext(file.filename)[1]
    if file_extension.lower() not in ['.xlsx', '.xls']:
        return {"error": "Uploaded file must be an Excel file with .xlsx or .xls extension."}
    
    try:
        dataframe = pd.read_excel(file.file, sheet_name=None, )
    except Exception as e:
        return {"error": f"An error occurred while reading the Excel file: {str(e)}"}


    for table_name, table_data in dataframe.items():
        table_data.replace({np.nan: None}, inplace=True)
        
        data = convert(table_data)

        for dict in data:
            dict['_id'] = ObjectId(dict['_id'])
      
        collection = db[table_name]
        collection.drop()
        collection.insert_many(data)

    return {"filename": file.filename}

def convert(data):
    countItems = 0

    for key, value in data.items():
        countItems = len(value)
        break

    itemList = []

    for i in range(0, countItems):
        dictTmp = {}
        for key, value in data.items():
            newValue = value[i]
            try:
                newValue = eval(newValue)
            except:
                pass
            if isinstance(newValue, np.int64):
                v = int(newValue)
                newValue = v
            if isinstance(newValue, np.bool_):
                v = bool(newValue)
                newValue = v
            if key == "module_id":
                newValue = str(newValue)
            if key == "title":
                if value[i] is None:
                    newValue = ""
                else:
                    newValue = str(newValue)
            dictTmp[key] = newValue
        itemList.append(dictTmp)
    return itemList

