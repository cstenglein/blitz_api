from typing import List

from app.auth.auth_bearer import JWTBearer
from app.models.lightning import (
    Invoice,
    LightningInfoLite,
    LnInfo,
    OnChainTransaction,
    Payment,
    PaymentRequest,
    SendCoinsInput,
    SendCoinsResponse,
    WalletBalance,
)
from app.repositories.lightning import (
    add_invoice,
    decode_pay_request,
    get_ln_info,
    get_ln_info_lite,
    get_wallet_balance,
    list_on_chain_tx,
    send_coins,
    send_payment,
)
from app.routers.lightning_docs import (
    get_balance_response_desc,
    send_coins_desc,
    send_payment_desc,
)
from fastapi import APIRouter, HTTPException, Query, status
from fastapi.params import Depends

_PREFIX = "lightning"

router = APIRouter(prefix=f"/{_PREFIX}", tags=["Lightning"])


@router.post(
    "/add-invoice",
    name=f"{_PREFIX}.add-invoice",
    summary="Addinvoice adds a new Invoice to the database.",
    description="For additional information see [LND docs](https://api.lightning.community/#addinvoice)",
    dependencies=[Depends(JWTBearer())],
    response_model=Invoice,
)
async def addinvoice(
    value_msat: int, memo: str = "", expiry: int = 3600, is_keysend: bool = False
):
    try:
        return await add_invoice(memo, value_msat, expiry, is_keysend)
    except HTTPException as r:
        raise HTTPException(r.status_code, detail=r.reason)
    except NotImplementedError as r:
        raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, detail=r.args[0])


@router.get(
    "/get-balance",
    name=f"{_PREFIX}.get-balance",
    summary="Get the current on chain and channel balances of the lighting wallet.",
    response_description=get_balance_response_desc,
    dependencies=[Depends(JWTBearer())],
    response_model=WalletBalance,
)
async def getwalletbalance():
    try:
        return await get_wallet_balance()
    except HTTPException as r:
        raise HTTPException(r.status_code, detail=r.reason)
    except NotImplementedError as r:
        raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, detail=r.args[0])


@router.get(
    "/list-onchain-tx",
    name=f"{_PREFIX}.decode-pay-req",
    summary="Lists all onchain transactions from the wallet",
    response_model=List[OnChainTransaction],
    response_description="A list of all on-chain transactions made.",
    dependencies=[Depends(JWTBearer())],
)
async def list_on_chain_tx_path():
    return await list_on_chain_tx()


@router.post(
    "/send-coins",
    name=f"{_PREFIX}.send-coins",
    summary="Attempt to send on-chain funds.",
    description=send_coins_desc,
    response_description="Either an error or a SendCoinsResponse object on success",
    dependencies=[Depends(JWTBearer())],
    response_model=SendCoinsResponse,
)
async def send_coins_path(input: SendCoinsInput):
    try:
        return await send_coins(input=input)
    except HTTPException as r:
        raise HTTPException(r.status_code, detail=r.detail)
    except NotImplementedError as r:
        raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, detail=r.args[0])


@router.post(
    "/send-payment",
    name=f"{_PREFIX}.send-payment",
    summary="Attempt to pay a payment request.",
    description=send_payment_desc,
    response_description="Either an error or a Payment object on success",
    dependencies=[Depends(JWTBearer())],
    response_model=Payment,
)
async def sendpayment(
    pay_req: str, timeout_seconds: int = 5, fee_limit_msat: int = 8000
):
    try:
        return await send_payment(pay_req, timeout_seconds, fee_limit_msat)
    except HTTPException as r:
        raise HTTPException(r.status_code, detail=r.detail)
    except NotImplementedError as r:
        raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, detail=r.args[0])


@router.get(
    "/get-info",
    name=f"{_PREFIX}.get-info",
    summary="Request information about the currently running lightning node.",
    response_description="Either an error or a LnInfo object on success",
    dependencies=[Depends(JWTBearer())],
    response_model=LnInfo,
)
async def get_info():
    try:
        return await get_ln_info()
    except HTTPException as r:
        raise HTTPException(r.status_code, detail=r.detail)
    except NotImplementedError as r:
        raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, detail=r.args[0])


@router.get(
    "/get-info-lite",
    name=f"{_PREFIX}.get-info-lite",
    summary="Get lightweight current lightning info. Less verbose version of /lightning/get-info",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_200_OK,
    response_model=LightningInfoLite,
)
async def get_ln_info_lite_path():
    try:
        return await get_ln_info_lite()
    except HTTPException as r:
        raise HTTPException(r.status_code, detail=r.reason)
    except NotImplementedError as r:
        raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, detail=r.args[0])


@router.get(
    "/decode-pay-req",
    name=f"{_PREFIX}.decode-pay-req",
    summary="DecodePayReq takes an encoded payment request string and attempts to decode it, returning a full description of the conditions encoded within the payment request.",
    response_model=PaymentRequest,
    response_description="A fully decoded payment request or a HTTP status 400 if the payment request cannot be decoded.",
    dependencies=[Depends(JWTBearer())],
)
async def get_decode_pay_request(
    pay_req: str = Query(..., description="The payment request string to be decoded")
):
    return await decode_pay_request(pay_req)
