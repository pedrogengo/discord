from factory import Factory, Faker, SubFactory, List

from micebot.model.model import (
    ProductCreation,
    ProductEdit,
    ProductDelete,
    Product,
    ProductQuery,
    Order,
    OrderQuery,
    OrderWithTotal,
    ProductDeleteResponse,
    ProductResponse,
    ProductTotal,
)


class ProductCreationFactory(Factory):
    class Meta:
        model = ProductCreation

    code = Faker("md5")
    summary = Faker("sentence", nb_words=4)


class ProductEditFactory(Factory):
    class Meta:
        model = ProductEdit

    uuid = Faker("uuid4")
    code = Faker("md5")
    summary = Faker("sentence", nb_words=4)


class ProductDeleteFactory(Factory):
    class Meta:
        model = ProductDelete

    uuid = Faker("uuid4")


class ProductDeleteResponseFactory(Factory):
    class Meta:
        model = ProductDeleteResponse

    deleted = Faker("boolean")


class ProductFactory(Factory):
    class Meta:
        model = Product

    uuid = Faker("uuid4")
    code = Faker("md5")
    summary = Faker("sentence", nb_words=4)
    taken = Faker("boolean")
    created_at = Faker("date_time_between", start_date="-30d", end_date="-10d")
    updated_at = Faker("date_time_between", start_date="-5d", end_date="now")


class ProductQueryFactory(Factory):
    class Meta:
        model = ProductQuery

    taken = Faker("boolean")
    desc = Faker("boolean")
    limit = Faker("boolean")


class ProductTotalFactory(Factory):
    class Meta:
        model = ProductTotal

    all = Faker("pyint")
    taken = Faker("pyint")
    available = Faker("pyint")


class ProductResponseFactory(Factory):
    class Meta:
        model = ProductResponse

    total = SubFactory(ProductTotalFactory)
    products = List([SubFactory(ProductFactory) for _ in range(5)])


class OrderFactory(Factory):
    class Meta:
        model = Order

    mod_id = Faker("sha256")
    mod_display_name = Faker("user_name")
    owner_display_name = Faker("user_name")
    uuid = Faker("uuid4")
    requested_at = Faker(
        "date_time_between", start_date="-30d", end_date="-10d"
    )
    product = SubFactory(ProductFactory)


class OrderQueryFactory(Factory):
    class Meta:
        model = OrderQuery

    skip = Faker("pyint", min_value=0, max_value=10)
    limit = Faker("pyint", min_value=10, max_value=50)
    moderator = Faker("user_name")
    owner = Faker("user_name")
    desc = Faker("boolean")


class OrderWithTotalFactory(Factory):
    class Meta:
        model = OrderWithTotal

    total = Faker("pyint", min_value=1, max_value=100)
    orders = List([SubFactory(OrderFactory) for _ in range(5)])
