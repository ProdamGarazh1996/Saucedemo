from decimal import Decimal

from config.settings import settings
from models.models import CheckoutInfo, Product, User

TAX_RATE = Decimal("0.08")


class Users:
    STANDARD = User("standard_user", settings.password)
    LOCKED_OUT = User("locked_out_user", settings.password)
    PROBLEM = User("problem_user", settings.password)
    PERFORMANCE_GLITCH = User("performance_glitch_user", settings.password)
    ERROR = User("error_user", settings.password)
    VISUAL = User("visual_user", settings.password)
    INVALID = User("unknown_user", "wrong_password")


class Products:
    BACKPACK = Product(
        name="Sauce Labs Backpack",
        description="carry.allTheThings() with the sleek, streamlined Sly "
                    "Pack that melds uncompromising style with unequaled "
                    "laptop and tablet protection.",
        price=Decimal("29.99"),
    )
    BIKE_LIGHT = Product(
        name="Sauce Labs Bike Light",
        description="A red light isn't the desired state in testing but it "
                    "sure helps when riding your bike at night. "
                    "Water-resistant with 3 lighting modes, 1 AAA battery "
                    "included.",
        price=Decimal("9.99"),
    )
    BOLT_T_SHIRT = Product(
        name="Sauce Labs Bolt T-Shirt",
        description="Get your testing superhero on with the Sauce Labs bolt "
                    "T-shirt. From American Apparel, 100% ringspun combed "
                    "cotton, heather gray with red bolt.",
        price=Decimal("15.99"),
    )
    FLEECE_JACKET = Product(
        name="Sauce Labs Fleece Jacket",
        description="It's not every day that you come across a midweight "
                    "quarter-zip fleece jacket capable of handling "
                    "everything from a relaxing day outdoors to a busy day "
                    "at the office.",
        price=Decimal("49.99"),
    )
    ONESIE = Product(
        name="Sauce Labs Onesie",
        description="Rib snap infant onesie for the junior automation "
                    "engineer in development. Reinforced 3-snap bottom "
                    "closure, two-needle hemmed sleeved and bottom won't "
                    "unravel.",
        price=Decimal("7.99"),
    )
    RED_T_SHIRT = Product(
        name="Test.allTheThings() T-Shirt (Red)",
        description="This classic Sauce Labs t-shirt is perfect to wear when "
                    "cozying up to your keyboard to automate a few tests. "
                    "Super-soft and comfy ringspun combed cotton.",
        price=Decimal("15.99"),
    )

    ALL = (BACKPACK, BIKE_LIGHT, BOLT_T_SHIRT, FLEECE_JACKET, ONESIE,
           RED_T_SHIRT)


CHECKOUT_INFO = CheckoutInfo(first_name="Ivan", last_name="Ivanov",
                             postal_code="123456")
