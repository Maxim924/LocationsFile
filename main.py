from fastapi import FastAPI, Request
from platforms_router import router
import uvicorn
from fastapi.templating import Jinja2Templates
app = FastAPI()

app.include_router(router)

templates = Jinja2Templates(directory="templates")
@app.get("/", include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
