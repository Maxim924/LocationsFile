import csv
import asyncio
from geopy.distance import geodesic

ad_platforms = []

async def load_advertising_platforms(file_content: str):
    """
    Функция загрузки рекламных площадок из файла
    """
    global ad_platforms
    decoded_contents = file_content.splitlines()
    reader = csv.DictReader(decoded_contents)
    new_ad_platforms = []

    for row in reader:
        try:
            new_ad_platforms.append({
                "id": row["id"],
                "name": row["name"],
                "latitude": float(row["latitude"]),
                "longitude": float(row["longitude"]),
                "locations": row["locations"].split(",")
            })
        except (ValueError, KeyError):
            continue

    ad_platforms = new_ad_platforms

async def search_advertising_platforms(latitude, longitude, radius, location):
    """
    Функция поиска списка рекламных площадок для заданной локации
    """
    result = []
    tasks = []

    relevant_platforms = [platform for platform in ad_platforms if any(location.startswith(loc) for loc in platform["locations"])]

    for platform in relevant_platforms:
        tasks.append(asyncio.to_thread(geodesic, (latitude, longitude), (platform["latitude"], platform["longitude"])))

    distances = await asyncio.gather(*tasks)

    for platform, distance in zip(relevant_platforms, distances):
        if distance.km <= radius:
            result.append(platform)

    return {"count": len(result), "platforms": result}
