from models.wallet_models import WalletRecord
from tests.factories import BaseFactory
from uuid import uuid4
from datetime import datetime


class WalletTableFactory(BaseFactory):
    class Meta:
        model = WalletRecord

    uuid = uuid4()
    address = "TMzoZ7iRvSJhi47Fygp47MQbVPbsezdqZV"
    balance = 84.388632
    bandwidth = 0
    energy = 0
    date_created = datetime.now()
