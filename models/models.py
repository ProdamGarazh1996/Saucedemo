from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from enum import Enum


def parse_price(text: str) -> Decimal:
    return Decimal(text.rsplit("$", 1)[-1].strip())


@dataclass(frozen=True)
class User:
    username: str
    password: str


@dataclass(frozen=True)
class Product:
    name: str
    description: str
    price: Decimal


@dataclass(frozen=True)
class CheckoutInfo:
    first_name: str
    last_name: str
    postal_code: str


@dataclass(frozen=True)
class OrderSummary:
    item_total: Decimal
    tax: Decimal
    total: Decimal

    @classmethod
    def calculate(cls, products: list[Product],
                  tax_rate: Decimal) -> "OrderSummary":
        item_total = sum((product.price for product in products),
                         Decimal("0"))
        tax = (item_total * tax_rate).quantize(Decimal("0.01"),
                                               rounding=ROUND_HALF_UP)
        return cls(item_total=item_total, tax=tax, total=item_total + tax)


class SortOption(Enum):
    NAME_ASC = ("az", "Name (A to Z)")
    NAME_DESC = ("za", "Name (Z to A)")
    PRICE_ASC = ("lohi", "Price (low to high)")
    PRICE_DESC = ("hilo", "Price (high to low)")

    def __init__(self, option_value: str, label: str):
        self.option_value = option_value
        self.label = label
