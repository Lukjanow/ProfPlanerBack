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
        #description="You don't need to know more, it's the best.<br> Just accept it. You'll never beat it. This is a test",
        #summary="The best. Nuff said.",
        version="V1",
        terms_of_service="https://www.youtube.com/watch?v=dQw4w9WgXcQ?autoplay=1",
        contact={
            "name": "My Website",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ?autoplay=1"
        },
        license_info={
            "name": "To be selected",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ?autoplay=1",
        },
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

