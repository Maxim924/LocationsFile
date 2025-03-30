from uuid import UUID

from pydantic import BaseModel
from datetime import datetime

__all__ = [
    "WalletBase",
    "ResponseCreate",
    "WalletPaginationResponse",
    "WalletCreate",
]

from common.paginate import PaginationAbstractResponseSchema


class WalletBase(BaseModel):
    uuid: UUID | str
    address: str
    balance: float | None
    bandwidth: int | None
    energy: int | None
    date_created: datetime | None

    class Config:
        from_attributes = True


class WalletPaginationResponse(PaginationAbstractResponseSchema):
    data: list[WalletBase]


class WalletCreate(BaseModel):
    wallet_address: str


class ResponseCreate(BaseModel):
    message: str
