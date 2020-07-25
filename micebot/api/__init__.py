from typing import Optional, List, Text, Dict

from httpx import post, get, put, delete

from micebot.model.model import (
    Product,
    ProductCreation,
    ProductEdit,
    ProductDelete,
    OrderQuery,
    OrderWithTotal,
    ProductQuery,
)


class Api:
    def __init__(self, endpoint: str, username: str, password: str):
        """
        Init the API instance.

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

    def _check_authentication(self):
        if not self.heartbeat():
            self.authenticate()

    def get_access_token(self) -> Optional[Text]:
        """
        Get the access token.

        Returns:
            - the access token value, if present. Otherwise, `None` is returned.
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
                "The access_token key is not present"
                "on Authorization response."
            )

        self.access_token = access_token
        return True

    def heartbeat(self) -> bool:
        """
        Check if the application "session" is valid.

        Returns:
            - the specific heartbeat response associate to request.
        """
        response = get(f"{self.endpoint}/hb")

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

        Returns:
            - `None` if there is any fail on product creation, otherwise, if
            the server respond with http status 201, the product objet is
            returned.
        """
        self._check_authentication()

        response = post(
            f"{self.endpoint}/products/",
            json={"code": product.code, "summary": product.summary},
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        if response.status_code == 409:
            ...

        if response.status_code == 201:
            return Product(**response.json())

    def edit_product(self, product: ProductEdit) -> Optional[Product]:
        self._check_authentication()

        response = put(
            f"{self.endpoint}/products/{product.uuid}",
            json={"code": product.code, "summary": product.summary},
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        if response.status_code == 404:
            ...  # product not found

        if response.status_code == 409:
            ...  # code already in use.

        return Product(**response.json())

    def delete_product(
        self, product: ProductDelete
    ) -> Optional[Dict[Text, bool]]:
        self._check_authentication()

        response = delete(
            f"{self.endpoint}/products/{product.uuid}",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        if response.status_code == 404:
            ...  # product not found

        if response.status_code == 401:
            ...  # code already taken

        return dict(**response.json())

    def list_products(self, query: ProductQuery) -> List[Product]:
        self._check_authentication()

        response = get(
            f"{self.endpoint}/products/",
            params={"taken": query.taken, "desc": query.desc},
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        if response.status_code == 404:
            ...  # No product registed yet.

        if response.status_code == 200:
            return [Product(**content) for content in response.json()]

        return []

    def list_orders(
        self, query: OrderQuery = OrderQuery()
    ) -> Optional[OrderWithTotal]:
        """
        List the registered orders.

        Args:
            - query: the query parameters.

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
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        if response.status_code == 404:
            ...  # No product registed yet.

        if response.status_code == 200:
            return OrderWithTotal(**response.json())
