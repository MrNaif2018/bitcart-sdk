from decimal import Decimal

import pytest

pytestmark = pytest.mark.asyncio


async def test_balance(btc_wallet):
    attrs = ["confirmed", "unconfirmed", "unmatured", "lightning"]
    balance = await btc_wallet.balance()
    for attr in attrs:
        assert balance[attr] >= 0  # NOTE: unconfirmed can be negative
        assert isinstance(balance[attr], Decimal)


async def test_history(btc_wallet):
    history = await btc_wallet.history()
    assert isinstance(history["summary"], dict)
    assert isinstance(history["transactions"], list)


async def test_payment_request(btc_wallet):
    # request1
    request1_amount = "0.5"
    request1 = await btc_wallet.addrequest(request1_amount)
    assert request1[btc_wallet.amount_field] == request1["amount_BTC"] == Decimal(request1_amount)
    # request2
    request2_amount, request2_desc = "0.6", "test description"
    request2 = await btc_wallet.addrequest(request2_amount, request2_desc)
    assert request2["amount_BTC"] == Decimal(request2_amount)
    assert request2["memo"] == request2_desc
    # get request2
    response2 = await btc_wallet.getrequest(request2["address"])
    assert response2["amount_BTC"] == Decimal(request2_amount)
    assert response2["memo"] == request2_desc


async def test_insufficient_funds_pay(btc_wallet):
    with pytest.raises(ValueError):
        await btc_wallet.pay_to("2MzEqRRjMwECrZRH9fg5BDsa11SWsKSCE95", 0.1)