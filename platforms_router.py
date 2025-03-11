
from fastapi import APIRouter, HTTPException, Query, UploadFile
from platforms_service import load_advertising_platforms, search_advertising_platforms

router = APIRouter()

@router.post("/upload/advertising-platforms", tags=["Рекламные площадки"])
async def upload_advertising_platforms(file: UploadFile):
    """
    Метод загрузки рекламных площадок из файла
    Параметры:
        file - CSV-файл с данными рекламных площадок,
    """
    try:
        contents = await file.read()
        await load_advertising_platforms(contents.decode("utf-8"))
        return {"message": "Данные успешно загружены"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка обработки файла: {str(e)}")

@router.get("/search/advertising-platforms", tags=["Рекламные площадки"])
async def search_advertising_platforms_endpoint(
    latitude: float = Query(..., description="Широта центра поиска"),
    longitude: float = Query(..., description="Долгота центра поиска"),
    radius: float = Query(10.0, description="Радиус поиска в километрах"),
    location: str = Query(..., description="Локация для поиска рекламных площадок")
):
    """
    Метод поиска списка рекламных площадок для заданной локации
    Параметры:
        latitude - Широта центра поиска,
        longitude - Долгота центра поиска,
        radius - Радиус поиска в километрах.
        location - Локация поиска.
    """
    return await search_advertising_platforms(latitude, longitude, radius, location)
