#run with "python -m uvicorn API:app --reload" to ensure uvicorn uses correct python version and restart when changes are detected
from fastapi import Body, FastAPI

from routes import *

from routes.modules import router as modulesrouter
from routes.dozent import router as dozentrouter
from routes.room import router as roomrouter
from routes.calendar import router as calendarrouter
from routes.absence import router as absencerouter
from routes.notes import router as notesrouter
from routes.export import router as exportrouter
from routes.studycourse import router as studycourserouter
from routes.algorithm import router as algorithmrouter


#test
# https://fastapi.tiangolo.com/tutorial/bigger-applications/

app = FastAPI(    
        title="Profplaner API",
        swagger_ui_parameters={"defaultModelsExpandDepth": -1}  #Hide schemas at bottom of page
    )

app.include_router(modulesrouter)
app.include_router(dozentrouter)
app.include_router(roomrouter)
app.include_router(calendarrouter)
app.include_router(absencerouter)
app.include_router(notesrouter)
app.include_router(studycourserouter)
app.include_router(exportrouter)
app.include_router(algorithmrouter)

