class UnknownNetworkError(Exception):
    """Generic network error."""


class CodeAlreadyRegistered(Exception):
    """When the code is already in use by another product."""


class ProductNotFound(Exception):
    """When the query for a product returns 404."""


class ProductAlreadyTaken(Exception):
    """When the product is already taken."""


class OrderNotFound(Exception):
    """When the query for a order returns 404."""
