from app.models.lightning import Invoice, LnInfo, Payment, PaymentRequest


def get_implementation_name() -> str:
    return "c-lightning"


async def get_wallet_balance_impl():
    raise NotImplementedError("c-lightning not yet implemented")


async def add_invoice_impl(
    value_msat: int, memo: str = "", expiry: int = 3600, is_keysend: bool = False
) -> Invoice:
    raise NotImplementedError("c-lightning not yet implemented")


async def decode_pay_request_impl(pay_req: str) -> PaymentRequest:
    raise NotImplementedError("c-lightning not yet implemented")


async def send_payment_impl(
    pay_req: str, timeout_seconds: int, fee_limit_msat: int
) -> Payment:
    raise NotImplementedError("c-lightning not yet implemented")


async def get_ln_info_impl() -> LnInfo:
    raise NotImplementedError("c-lightning not yet implemented")


async def listen_invoices() -> Invoice:
    raise NotImplementedError("c-lightning not yet implemented")
