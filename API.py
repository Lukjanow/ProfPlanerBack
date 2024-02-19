#run with "python -m uvicorn API:app --reload" to ensure uvicorn uses correct python version and restart when changes are detected
from fastapi import Body, FastAPI

from routes import *

from routes.modules import router as modulesrouter
from routes.dozent import router as dozentrouter
from routes.room import router as roomrouter
from routes.calender import router as calenderrouter
from routes.absence import router as absencerouter
from routes.studysemester import router as studysemesterrouter


# https://fastapi.tiangolo.com/tutorial/bigger-applications/

app = FastAPI(    
    title="Profplaner API",
    description="You don't need to know more, it's the best.<br> Just accept it. You'll never beat it.",
    summary="The best. Nuff said.",
    version="V1",
    terms_of_service="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    contact={
        "name": "My Website",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    },
    license_info={
        "name": "To be selected",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    },
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}  #Hide schemas at bottom of page
    )

app.include_router(modulesrouter)
app.include_router(dozentrouter)
app.include_router(roomrouter)
app.include_router(calenderrouter)
app.include_router(absencerouter)
app.include_router(studysemesterrouter)