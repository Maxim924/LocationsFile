from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from common.paginate import PaginationRequestBodySchema, paginate
from database import async_get_session
from models.wallet_models import WalletRecord
from tronpy import Tron
from fastapi import Depends, HTTPException
from starlette import status
from typing import List, Dict
from schemas.wallet_schemas import WalletBase
import re

tron = Tron()

class WalletService:
    def __init__(self, session: AsyncSession = Depends(async_get_session)):
        self.session = session

    @staticmethod
    def is_valid_wallet_address(wallet_address: str) -> bool:
        """
        Проверка, что адрес кошелька является допустимым (формат адреса Tron).
        """
        return bool(re.match(r'^T[a-zA-Z0-9]{33}$', wallet_address))

    async def add_wallet(self, wallet_address: str) -> Dict[str, str]:
        """
        Получает данные кошелька с tron и выполняет запрос на создание.

        :param wallet_address: адрес кошелька
        """
        if not self.is_valid_wallet_address(wallet_address):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid wallet address"
            )
        try:
            account_info = tron.get_account(wallet_address)
            balance = account_info.get("balance", 0) / 1e6
            bandwidth = account_info.get("bandwidth", 0)
            energy = account_info.get("energy", 0)

            request_for_wallet = await self.create_wallet(wallet_address, balance, bandwidth, energy)
            return request_for_wallet

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred: {str(e)}"
            )

    async def get_all_wallet(self, dto: PaginationRequestBodySchema) -> List[WalletBase]:
        """
        Получает данные о запросах кошельков с пагинацией.

        :param dto: схема пагинации
        """
        wallet = list(
            (
                await self.session.execute(
                select(WalletRecord).order_by(desc(WalletRecord.date_created)))
            ).scalars().all()
        )

        if not wallet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not Found"
            )
        return paginate(dto, wallet, WalletBase)

    async def create_wallet(self, wallet_address: str, balance: float, bandwidth: int, energy: int) -> Dict[str, str]:
        """
        Создает запись о запрашиваемом кошельке.

        :param wallet_address: адрес кошелька
        :param balance: баланс кошелька
        :param bandwidth: количество транзакций или операций, которые можно выполнить без платы
        :param energy: ресурсы, которые требуются для выполнения смарт-контрактов и операций в сети Tron
        """
        try:
            new_record = WalletRecord(
                address=wallet_address,
                balance=balance,
                bandwidth=bandwidth,
                energy=energy
            )
            self.session.add(new_record)
            await self.session.commit()

            return {"message": f"Информация о кошельке {wallet_address} сохранена"}

        except Exception as e:
            return {"error": str(e)}
