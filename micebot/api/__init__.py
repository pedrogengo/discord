from typing import Optional, Text, NoReturn

from httpx import post, get, put, delete

from micebot.model.model import (
    Product,
    ProductCreation,
    ProductEdit,
    ProductDelete,
    OrderQuery,
    OrderWithTotal,
    ProductQuery,
    ProductResponse,
    ProductDeleteResponse,
)
from micebot.api.errors import (
    CodeAlreadyRegistered,
    UnknownNetworkError,
    ProductNotFound,
    ProductAlreadyTaken,
    OrderNotFound,
)


class Api:
    def __init__(self, endpoint: str, username: str, password: str):
        """
        Init the API.

        Args:
            - endpoint: the API endpoint.
            - username: the client username for authorization.
            - password: the client password for authorization.
        """
        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.access_token = None
        self.DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def _check_authentication(self) -> NoReturn:
        """
        Authenticate the user if its not authenticated yet.
        """
        if not self.heartbeat():
            self.authenticate()

    def get_access_token(self) -> Optional[Text]:
        """
        Get the access token.

        Returns:
            - the access token if present. Otherwise, `None`is returned.
        """
        return self.access_token

    def authenticate(self) -> bool:
        """
        Authenticate the client.

        Returns:
            - the specific product response associate to request.
        """
        response = post(
            f"{self.endpoint}/auth/",
            data={"username": self.username, "password": self.password},
        )

        if response.status_code == 401:
            return False

        access_token = response.json().get("access_token")
        if not access_token:
            raise ValueError(
                "The access_token key is not present " "on Authorization response."
            )

        self.access_token = access_token
        return True

    def heartbeat(self) -> bool:
        """
        Check if the application "session" is valid.

        Returns:
            - the specific heartbeat response associate to request.
        """
        access_token = self.get_access_token()

        if not access_token:
            return False

        response = get(
            f"{self.endpoint}/hb/",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        if response.status_code == 401:
            return False

        is_valid = response.json().get("valid")

        if not is_valid:
            return False

        return True

    def add_product(self, product: ProductCreation) -> Optional[Product]:
        """
        Add a new product.

        Args:
            - product: the required values for product creation.

        Raises:
            CodeAlreadyRegistered: when the code used to register the
                product is already in use by another persisted product.
            UnknownNetworkError: when any unknown network error happens.

        Returns:
            - the API response for a creation operation.
        """
        self._check_authentication()

        response = post(
            f"{self.endpoint}/products/",
            json={"code": product.code, "summary": product.summary},
            headers={"Authorization": f"Bearer {self.get_access_token()}"},
        )

        if response.status_code == 409:
            raise CodeAlreadyRegistered(
                f"{product.code} is already in use by another product."
            )

        if response.status_code != 201:
            raise UnknownNetworkError(
                f"Failed to add a product, network error: "
                f"(status: {response.status_code} - data: {response.content})."
            )
        return Product(**response.json())

    def edit_product(self, product: ProductEdit) -> Optional[Product]:
        """
        Edit an existent product.

        Args:
            - product: the parameters for edit a product.

        Raises:
            ProductNotFound: when no product was found for the uuid provided.
            CodeAlreadyRegistered: when the code used to register the
                product is already in use by another persisted product.
            UnknownNetworkError: when any unknown network error happens.

        Returns:
            - the API response for an edit operation.
        """
        self._check_authentication()

        response = put(
            f"{self.endpoint}/products/{product.uuid}",
            json={"code": product.code, "summary": product.summary},
            headers={"Authorization": f"Bearer {self.get_access_token()}"},
        )

        if response.status_code == 404:
            raise ProductNotFound(f"Product with uuid {product.uuid} not found.")

        if response.status_code == 409:
            raise CodeAlreadyRegistered(
                f"{product.code} is already in use by another product."
            )

        if response.status_code != 200:
            raise UnknownNetworkError(
                f"Failed to edit a product, network error: "
                f"(status: {response.status_code} - data: {response.content})."
            )
        return Product(**response.json())

    def delete_product(self, product: ProductDelete) -> ProductDeleteResponse:
        """
        Delete an existent product.

        Args:
            - product: the parameters for remove a product.

        Raises:
            ProductNotFound: when no product was found for the uuid provided.
            ProductAlreadyTaken: when the product is already taken.
            UnknownNetworkError: when any unknown network error happens.

        Returns:
            - the API response from a delete operation.
        """
        self._check_authentication()

        response = delete(
            f"{self.endpoint}/products/{product.uuid}",
            headers={"Authorization": f"Bearer {self.get_access_token()}"},
        )

        if response.status_code == 404:
            raise ProductNotFound(f"Product with uuid {product.uuid} not found.")

        if response.status_code == 401:
            raise ProductAlreadyTaken(
                f"Cannot delete the product {product.uuid}, "
                f"because it is already taken."
            )

        if response.status_code != 200:
            raise UnknownNetworkError(
                f"Failed to remove a product, network error: "
                f"(status: {response.status_code} - data: {response.content})."
            )

        return ProductDeleteResponse(**response.json())

    def list_products(self, query: ProductQuery) -> ProductResponse:
        """
        List the registered products.

        Args:
            - query: the query parameters for list products.

        Raises:
            ProductNotFound: when there is no product registed yet.
            UnknownNetworkError: when any unknown network error happens.

        Returns:
            - the API response from a delete operation.
        """
        self._check_authentication()

        response = get(
            f"{self.endpoint}/products/",
            params={
                "taken": query.taken,
                "desc": query.desc,
                "limit": query.limit,
            },
            headers={"Authorization": f"Bearer {self.get_access_token()}"},
        )

        if response.status_code == 404:
            raise ProductNotFound("No product registered yet!")

        if response.status_code != 200:
            raise UnknownNetworkError(
                f"Failed to list the products, network error: "
                f"(status: {response.status_code} - data: {response.content})."
            )
        return ProductResponse(**response.json())

    def list_orders(self, query: OrderQuery = OrderQuery()) -> OrderWithTotal:
        """
        List the registered orders.

        Args:
            - query: the query parameters for list orders.

        Raises:
            OrderNotFound: when there is no orders registed yet.
            UnknownNetworkError: when any unknown network error happens.

        Returns:
            - the available orders for the query parameters provided.
        """
        self._check_authentication()

        response = get(
            f"{self.endpoint}/orders/",
            params={
                "moderator": query.moderator,
                "owner": query.owner,
                "skip": query.skip,
                "limit": query.limit,
                "desc": query.desc,
            },
            headers={"Authorization": f"Bearer {self.get_access_token()}"},
        )

        if response.status_code == 404:
            raise OrderNotFound("No orders registered yet!")

        if response.status_code != 200:
            raise UnknownNetworkError(
                f"Failed to list the orders, network error: "
                f"(status: {response.status_code} - data: {response.content})."
            )

        return OrderWithTotal(**response.json())
