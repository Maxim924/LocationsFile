from math import ceil
from typing import Type

from fastapi import HTTPException
from pydantic import BaseModel, Field
from starlette import status


class PaginationRequestBodySchema(BaseModel):
    page: int | None = Field(description="Текущая страница", default=None)
    page_size: int | None = Field(
        description="Количество элементов для отображения на странице", default=None
    )

    class Config:
        from_attributes = True


class PaginationAbstractResponseSchema(BaseModel):
    total_pages: int | None = Field(
        description="Максимальное количество страниц с текущими параметрами page_size"
    )
    current_page: int | None = Field(description="Текущая страница")


def paginate(
    dto: PaginationRequestBodySchema,
    data: list[dict] = None,
    data_schema: Type[BaseModel] = None,
):
    """Производит пагинацию для страницы.

    :param dto: тело запроса с пагинацией
    :param data: список элементов
    :param data_schema: схема для преобразования данных
    """
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Данные отсутствуют"
        )

    if dto.page is None or dto.page_size is None:
        response = {
            "current_page": None,
            "total_pages": None,
            "data": data,
        }
        return response

    if dto.page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Значение 'page' должно быть больше или равно 1.",
        )
    if dto.page_size < 1 or dto.page_size > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Значение 'page_size' должно быть между 1 и 50.",
        )

    total = len(data)
    total_page = ceil(total / dto.page_size)

    if dto.page > total_page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Страница {dto.page} выходит за пределы доступных страниц ({total_page})",
        )

    start_item = (dto.page - 1) * dto.page_size
    final_item = min(dto.page * dto.page_size, total)
    data = data[start_item:final_item]

    if data_schema:
        data = [data_schema.from_orm(single_data) for single_data in data]

    response = {
        "current_page": dto.page,
        "total_pages": total_page,
        "data": data,
    }
    return response
