from fastapi import APIRouter, Depends, Body

from common.paginate import PaginationRequestBodySchema
from schemas.wallet_schemas import WalletPaginationResponse, ResponseCreate, WalletCreate
from services.wallet_service import WalletService

router = APIRouter()

@router.get(
    "/wallets/get",
    tags=["Wallet"],
    summary="Получить записи о запрашиваемых кошельках",
    description="Метод для получения данных о запрашиваемых кошельках с данными."
                "\n\n Параметры пагинации: \n\n page - Текущая страница "
                "\n\n page_size - Количество отображаемых элементов",
    response_model=WalletPaginationResponse,
)
async def get_wallet_records(
    dto: PaginationRequestBodySchema = Depends(),
    service: WalletService = Depends()
):
    return await service.get_all_wallet(dto)

@router.post(
    "/wallets/create-or-update",
    tags=["Wallet"],
    summary="Создать запись о запрашиваемом кошельке",
    description="Метод для создания записи о запрашиваемом кошельке с данными.",
    response_model=ResponseCreate,
)
async def add_wallet(
    dto: WalletCreate = Body(),
    service: WalletService = Depends()
):
    return await service.add_wallet(dto.wallet_address)
