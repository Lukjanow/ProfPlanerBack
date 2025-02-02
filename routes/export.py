from io import BytesIO
from bson import ObjectId
from pymongo import MongoClient
import pandas as pd
from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from datetime import date
import time
import os
from models.common import *
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



def checkExcelFormat(table_name, table_data):
    expected_columns = None
    print("----------------------")
    print(table_name)
    print(table_data)
    print("---------------------------------")
    if(table_data.empty):
        return True, True
    
    if table_name == "modules":
        expected_columns = set([
            "_id", "module_id", "name", "code", "dozent", "room",
            "study_semester", "duration", "approximate_attendance",
            "frequency", "selected", "color"
            ])
    elif table_name == "dozent":
        expected_columns = set([
            "_id", "prename", "lastname", "email", "title", "salutation", "absences"
            ])
    elif table_name == "rooms":
        expected_columns = set([
            "_id", "roomNumber", "capacity", "roomType"
            ])
    elif table_name == "studycourse": 
        expected_columns = set([
            "_id", "name", "semesterCount", "content"
            ])
    elif table_name == "calendar":
        expected_columns = set([
            "_id", "name", "entries", "frequency", "last_opening"
            ])
    elif table_name == "calendarEntry":
        expected_columns = set([
            "_id", "module", "time_stamp", "comment"
            ])
    if expected_columns == None:
        return False, False
    
    df_columns = set(table_data.columns)
    
    if expected_columns != df_columns:
        return False, False
    
    return True, False

def getFileData(file):
    file_extension = os.path.splitext(file.filename)[1]
    if file_extension.lower() not in ['.xlsx', '.xls']:
        raise HTTPException(415, detail=f"Uploaded file must be an Excel file with .xlsx or .xls extension.",)
    
    try:
        dataframe = pd.read_excel(file.file, sheet_name=None, )
    except Exception as e:
        raise HTTPException(400, detail=f"An error occurred while reading the Excel file: {str(e)}",)
    return dataframe

def mergeData(collection, data):
    newDataList = []

    collectionData = collection.find()

    dataIds = {item['_id'] for item in data}

    for item in collectionData:
        if(item["_id"] not in dataIds):
            newDataList.append(item)
    
    for item in data:
        newDataList.append(item)

    return newDataList
    

def checkNewData(table_name, newDataList):
    if(table_name == "modules"):
        for module in newDataList:
            for dozent_id in module["dozent"]:
                if(dozents.find_one(ObjectId(dozent_id)) == None):
                    return False
            for room_id in module["room"]:
                if(rooms.find_one(ObjectId(room_id)) == None):
                    return False
            for study_semester in module["study_semester"]:
                if(studyCourseCollection.find_one(ObjectId(study_semester["studyCourse"])) == None):
                    return False
                
    if(table_name == "calendarEntry"):
        for entry in newDataList:
            if(modules.find_one(ObjectId(entry["module"])) == None):
                return False
            
    if(table_name == "calendar"):
        for calendar in newDataList:
            for entry_id in calendar["entries"]:
                if(calendarentry.find_one(ObjectId(entry_id)) == None):
                    return False
    
    return True



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
        tags=["Export"],
        responses={
            415: {"model": HTTPError, "detail": "str"},
            400: {"model": HTTPError, "detail": "str"}
            })
async def create_upload_file(file: UploadFile):
    dataframe = getFileData(file)

    for table_name, table_data in dataframe.items():
        format, empty = checkExcelFormat(table_name, table_data)
        if empty:
            collection = db[table_name]
            collection.drop()
            continue

        if not format:
            raise HTTPException(400, detail=f"An error occurred while Excel file has wrong format.",)

        table_data.replace({np.nan: None}, inplace=True)
        data = convert(table_data)

        for dict in data:
            dict['_id'] = ObjectId(dict['_id'])
      
        collection = db[table_name]
        collection.drop()
        collection.insert_many(data)

    return {"filename": file.filename}


@router.post("/import/excel/basicdata/merge/",summary="Import Basicdata as xlsx",
        description="Import Data to a xlsx file",
        tags=["Export"],
        responses={
            415: {"model": HTTPError, "detail": "str"},
            400: {"model": HTTPError, "detail": "str"}
            })
async def create_upload_file(file: UploadFile):
    dataframe = getFileData(file)

    sortDataFrame = {}

    if("studycourse" in dataframe.keys()):
        sortDataFrame["studycourse"] = dataframe["studycourse"]
    
    if("rooms" in dataframe.keys()):
        sortDataFrame["rooms"] = dataframe["rooms"]

    if("dozent" in dataframe.keys()):
        sortDataFrame["dozent"] = dataframe["dozent"]

    if("modules" in dataframe.keys()):
        sortDataFrame["modules"] = dataframe["modules"]

    if("calendarEntry" in dataframe.keys()):
        sortDataFrame["calendarEntry"] = dataframe["calendarEntry"]

    if("calendar" in dataframe.keys()):
        sortDataFrame["calendar"] = dataframe["calendar"]

    for table_name, table_data in sortDataFrame.items():
        format, empty = checkExcelFormat(table_name, table_data)

        if empty:
            continue

        if not format:
            raise HTTPException(400, detail=f"An error occurred while Excel file has wrong format.",)

        table_data.replace({np.nan: None}, inplace=True)
        data = convert(table_data)

        for dict in data:
            dict['_id'] = ObjectId(dict['_id'])
      
        collection = db[table_name]

        newData = mergeData(collection, data)

        if(not checkNewData(table_name, newData)):
            return {"ERROR": table_name}

        collection.drop()
        collection.insert_many(newData)

    return {"filename": file.filename}