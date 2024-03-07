import pandas as pd
from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse
import io
from Database.Database import db

router = APIRouter()

dozents = db["dozent"]
rooms = db["rooms"]
modules = db["modules"]

@router.get("/rooms/csv/", response_class=StreamingResponse)
async def export_data():
    roomsData = rooms.find()

    df = pd.DataFrame(list(roomsData))
    stream = io.StringIO()

    df.to_csv(stream, index=False)
    response = StreamingResponse(
        iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=export_rooms.csv"
    return response

@router.get("/dozents/csv/", response_class=StreamingResponse)
async def export_data():
    dozentsData = dozents.find()

    df = pd.DataFrame(list(dozentsData))
    stream = io.StringIO()

    df.to_csv(stream, index=False)
    response = StreamingResponse(
        iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=export_dozents.csv"
    return response

@router.get("/modules/csv/", response_class=StreamingResponse)
async def export_data():
    modulesData = modules.find()

    df = pd.DataFrame(list(modulesData))
    stream = io.StringIO()

    df.to_csv(stream, index=False)
    response = StreamingResponse(
        iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=export_modules.csv"
    return response

@router.get("/excel/")
async def export_data(response: Response):
    modulesData = modules.find()
    dozentsData = dozents.find()
    roomsData = rooms.find()

    pandaModule = pd.DataFrame(modulesData)
    pandaDozent = pd.DataFrame(dozentsData)
    pandaRoom = pd.DataFrame(roomsData)

    excel_writer = pd.ExcelWriter('exported_data.xlsx', engine='xlsxwriter')

    pandaModule.to_excel(excel_writer, sheet_name='Modules', index=False)
    pandaDozent.to_excel(excel_writer, sheet_name='Dozents', index=False)
    pandaRoom.to_excel(excel_writer, sheet_name='Rooms', index=False)

    excel_writer.save()

    with open('exported_data.xlsx', 'rb') as file:
        excel_data = file.read()

    response.headers["Content-Disposition"] = "attachment; filename=exported_data.xlsx"

    return Response(content=excel_data, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")