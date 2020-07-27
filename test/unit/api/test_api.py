from unittest.mock import patch, MagicMock

from micebot.api import (
    Api,
    CodeAlreadyRegistered,
    UnknownNetworkError,
    ProductNotFound,
    ProductAlreadyTaken,
)
from test.unit.factories import (
    ProductCreationFactory,
    ProductFactory,
    ProductEditFactory,
    ProductDeleteFactory,
    ProductDeleteResponseFactory,
)
from test.unit.test_case import Test


class TestAPI(Test):
    def setUp(self):
        self.endpoint = "http://" + self.faker.domain_name()
        self.username = self.faker.user_name()
        self.password = self.faker.password()

        self.api = Api(
            endpoint=self.endpoint,
            username=self.username,
            password=self.password,
        )


class TestAuthenticate(TestAPI):
    @patch("micebot.api.post")
    def test_should_return_false_when_http_status_is_401_for_auth(self, post):
        response = MagicMock()
        response.status_code = 401

        post.return_value = response

        self.assertFalse(self.api.authenticate())
        post.assert_called_with(
            self.endpoint + "/auth/",
            data={"username": self.username, "password": self.password},
        )

    @patch("micebot.api.post")
    def test_should_raise_value_error_when_access_token_is_not_present_on_response(  # noqa
        self, post
    ):
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {}

        post.return_value = response

        with self.assertRaises(ValueError) as context:
            self.api.authenticate()

        self.assertEqual(
            "The access_token key is not present on Authorization response.",
            str(context.exception),
        )

        post.assert_called_with(
            self.endpoint + "/auth/",
            data={"username": self.username, "password": self.password},
        )

    @patch("micebot.api.post")
    def test_set_access_token_and_return_true_when_it_is_present(self, post):

        access_token = self.faker.sha256()

        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {"access_token": access_token}

        post.return_value = response

        self.assertIsNone(self.api.get_access_token())
        self.assertTrue(self.api.authenticate())
        self.assertEqual(access_token, self.api.get_access_token())

        post.assert_called_with(
            self.endpoint + "/auth/",
            data={"username": self.username, "password": self.password},
        )


class TestHeartbeat(TestAPI):
    @patch("micebot.api.get")
    @patch("micebot.api.Api.get_access_token", return_value=None)
    def test_should_return_false_access_token_is_none(
        self, get_access_token, get
    ):
        self.assertFalse(self.api.heartbeat())
        get_access_token.assert_called_once()
        get.assert_not_called()

    @patch("micebot.api.get")
    @patch("micebot.api.Api.get_access_token")
    def test_should_return_false_when_http_status_is_401_for_heartbeat(
        self, get_access_token, get
    ):
        response = MagicMock()
        response.status_code = 401
        access_token = self.faker.sha256()

        get_access_token.return_value = access_token
        get.return_value = response

        self.assertFalse(self.api.heartbeat())
        get.assert_called_with(
            self.endpoint + "/hb/",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        get_access_token.assert_called_once()

    @patch("micebot.api.get")
    @patch("micebot.api.Api.get_access_token")
    def test_should_return_false_when_valid_parameter_does_not_exist(
        self, get_access_token, get
    ):
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {}
        access_token = self.faker.sha256()

        get_access_token.return_value = access_token
        get.return_value = response

        self.assertFalse(self.api.heartbeat())
        get.assert_called_with(
            self.endpoint + "/hb/",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        get_access_token.assert_called_once()

    @patch("micebot.api.get")
    @patch("micebot.api.Api.get_access_token")
    def test_should_return_false_when_valid_parameter_is_false(
        self, get_access_token, get
    ):
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {"valid": False}
        access_token = self.faker.sha256()

        get_access_token.return_value = access_token
        get.return_value = response

        self.assertFalse(self.api.heartbeat())
        get.assert_called_with(
            self.endpoint + "/hb/",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        get_access_token.assert_called_once()

    @patch("micebot.api.get")
    @patch("micebot.api.Api.get_access_token")
    def test_should_return_true_when_valid_parameter_is_true(
        self, get_access_token, get
    ):
        access_token = self.faker.sha256()
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {"valid": True}

        get_access_token.return_value = access_token
        get.return_value = response

        self.assertTrue(self.api.heartbeat())
        get.assert_called_with(
            self.endpoint + "/hb/",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        get_access_token.assert_called_once()


class TestAddProduct(TestAPI):
    @patch("micebot.api.post")
    @patch("micebot.api.Api.get_access_token")
    @patch("micebot.api.Api._check_authentication")
    def test_should_raise_code_already_registered_when_http_status_is_409(
        self, check_authentication, get_access_token, post
    ):
        response = MagicMock()
        response.status_code = 409
        product_creation = ProductCreationFactory()
        access_token = self.faker.sha256()

        get_access_token.return_value = access_token
        post.return_value = response

        with self.assertRaises(CodeAlreadyRegistered) as context:
            self.api.add_product(product_creation)

        self.assertEqual(
            f"{product_creation.code} is already in use by another product.",  # noqa
            str(context.exception),
        )
        check_authentication.assert_called_once()
        post.assert_called_with(
            f"{self.endpoint}/products/",
            json={
                "code": product_creation.code,
                "summary": product_creation.summary,
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

    @patch("micebot.api.post")
    @patch("micebot.api.Api.get_access_token")
    @patch("micebot.api.Api._check_authentication")
    def test_should_raise_unknown_network_error_when_http_status_is_not_409_or_201(  # noqa
        self, check_authentication, get_access_token, post
    ):
        http_status = self.faker.pyint(min_value=202, max_value=408)
        request_body = self.faker.sentence()
        product_creation = ProductCreationFactory()
        access_token = self.faker.sha256()

        response = MagicMock()
        response.status_code = http_status
        response.content = request_body

        post.return_value = response
        get_access_token.return_value = access_token

        with self.assertRaises(UnknownNetworkError) as context:
            self.api.add_product(product_creation)

        self.assertEqual(
            f"Failed to add a product, network error: "
            f"(status: {http_status} - data: {request_body}).",
            str(context.exception),
        )
        check_authentication.assert_called_once()
        post.assert_called_with(
            f"{self.endpoint}/products/",
            json={
                "code": product_creation.code,
                "summary": product_creation.summary,
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

    @patch("micebot.api.post")
    @patch("micebot.api.Api.get_access_token")
    @patch("micebot.api.Api._check_authentication")
    def test_should_return_the_product_data_when_http_status_is_201(
        self, check_authentication, get_access_token, post
    ):
        product = ProductFactory()
        product_creation = ProductCreationFactory(
            code=product.code, summary=product.summary
        )
        access_token = self.faker.sha256()

        response = MagicMock()
        response.status_code = 201
        response.json.return_value = {
            "code": product.code,
            "summary": product.summary,
            "uuid": product.uuid,
            "taken": product.taken,
            "created_at": product.created_at,
            "updated_at": product.updated_at,
        }

        post.return_value = response
        get_access_token.return_value = access_token

        self.assertEqual(product, self.api.add_product(product_creation))

        check_authentication.assert_called_once()
        post.assert_called_with(
            f"{self.endpoint}/products/",
            json={
                "code": product_creation.code,
                "summary": product_creation.summary,
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )


class TestEditProduct(TestAPI):
    @patch("micebot.api.put")
    @patch("micebot.api.Api.get_access_token")
    @patch("micebot.api.Api._check_authentication")
    def test_should_raise_product_not_found_when_http_status_is_404(
        self, check_authentication, get_access_token, put
    ):
        response = MagicMock()
        response.status_code = 404
        product = ProductEditFactory()
        access_token = self.faker.sha256()

        get_access_token.return_value = access_token
        put.return_value = response

        with self.assertRaises(ProductNotFound) as context:
            self.api.edit_product(product=product)

        self.assertEqual(
            f"Product with uuid {product.uuid} not found.",
            str(context.exception),
        )

        put.assert_called_with(
            f"{self.endpoint}/products/{product.uuid}",
            json={"code": product.code, "summary": product.summary},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        check_authentication.assert_called_once()

    @patch("micebot.api.put")
    @patch("micebot.api.Api.get_access_token")
    @patch("micebot.api.Api._check_authentication")
    def test_should_raise_code_already_registered_when_http_status_is_409(
        self, check_authentication, get_access_token, put
    ):
        response = MagicMock()
        response.status_code = 409
        product = ProductEditFactory()
        access_token = self.faker.sha256()

        get_access_token.return_value = access_token
        put.return_value = response

        with self.assertRaises(CodeAlreadyRegistered) as context:
            self.api.edit_product(product=product)

        self.assertEqual(
            f"{product.code} is already in use by another product.",
            str(context.exception),
        )

        put.assert_called_with(
            f"{self.endpoint}/products/{product.uuid}",
            json={"code": product.code, "summary": product.summary},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        check_authentication.assert_called_once()

    @patch("micebot.api.put")
    @patch("micebot.api.Api.get_access_token")
    @patch("micebot.api.Api._check_authentication")
    def test_should_raise_unknown_network_error_when_http_status_is_not_200(
        self, check_authentication, get_access_token, put
    ):
        http_status = self.faker.pyint(min_value=201, max_value=400)
        request_body = self.faker.sentence()

        response = MagicMock()
        response.status_code = http_status
        response.content = request_body

        product = ProductEditFactory()
        access_token = self.faker.sha256()

        get_access_token.return_value = access_token
        put.return_value = response

        with self.assertRaises(UnknownNetworkError) as context:
            self.api.edit_product(product=product)

        self.assertEqual(
            f"Failed to edit a product, network error: "
            f"(status: {http_status} - data: {request_body}).",
            str(context.exception),
        )

        put.assert_called_with(
            f"{self.endpoint}/products/{product.uuid}",
            json={"code": product.code, "summary": product.summary},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        check_authentication.assert_called_once()

    @patch("micebot.api.put")
    @patch("micebot.api.Api.get_access_token")
    @patch("micebot.api.Api._check_authentication")
    def test_should_return_the_edited_product_when_http_code_is_200(
        self, check_authentication, get_access_token, put
    ):
        product_edit = ProductEditFactory()

        product = ProductFactory(
            code=product_edit.code,
            summary=product_edit.summary,
            uuid=product_edit.uuid,
        )

        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {
            "code": product.code,
            "summary": product.summary,
            "uuid": product.uuid,
            "taken": product.taken,
            "created_at": product.created_at,
            "updated_at": product.updated_at,
        }

        access_token = self.faker.sha256()

        get_access_token.return_value = access_token
        put.return_value = response

        self.assertEqual(product, self.api.edit_product(product=product_edit))

        put.assert_called_with(
            f"{self.endpoint}/products/{product.uuid}",
            json={"code": product.code, "summary": product.summary},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        check_authentication.assert_called_once()


class TestDeleteProduct(TestAPI):
    @patch("micebot.api.delete")
    @patch("micebot.api.Api.get_access_token")
    @patch("micebot.api.Api._check_authentication")
    def test_should_raise_product_not_found_when_http_status_is_404(
        self, check_authentication, get_access_token, delete
    ):
        response = MagicMock()
        response.status_code = 404
        product = ProductDeleteFactory()
        access_token = self.faker.sha256()

        get_access_token.return_value = access_token
        delete.return_value = response

        with self.assertRaises(ProductNotFound) as context:
            self.api.delete_product(product=product)

        self.assertEqual(
            f"Product with uuid {product.uuid} not found.",
            str(context.exception),
        )

        delete.assert_called_with(
            f"{self.endpoint}/products/{product.uuid}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        check_authentication.assert_called_once()

    @patch("micebot.api.delete")
    @patch("micebot.api.Api.get_access_token")
    @patch("micebot.api.Api._check_authentication")
    def test_should_raise_code_already_taken_when_http_status_is_401(
        self, check_authentication, get_access_token, delete
    ):
        response = MagicMock()
        response.status_code = 401
        product = ProductDeleteFactory()
        access_token = self.faker.sha256()

        get_access_token.return_value = access_token
        delete.return_value = response

        with self.assertRaises(ProductAlreadyTaken) as context:
            self.api.delete_product(product=product)

        self.assertEqual(
            f"Cannot delete the product {product.uuid}, "
            f"because it is already taken.",
            str(context.exception),
        )

        delete.assert_called_with(
            f"{self.endpoint}/products/{product.uuid}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        check_authentication.assert_called_once()

    @patch("micebot.api.delete")
    @patch("micebot.api.Api.get_access_token")
    @patch("micebot.api.Api._check_authentication")
    def test_should_raise_unknown_network_error_when_http_status_is_not_200(
        self, check_authentication, get_access_token, delete
    ):
        http_status = self.faker.pyint(min_value=201, max_value=400)
        request_body = self.faker.sentence()

        response = MagicMock()
        response.status_code = http_status
        response.content = request_body

        product = ProductDeleteFactory()
        access_token = self.faker.sha256()

        get_access_token.return_value = access_token
        delete.return_value = response

        with self.assertRaises(UnknownNetworkError) as context:
            self.api.delete_product(product=product)

        self.assertEqual(
            f"Failed to remove a product, network error: "
            f"(status: {http_status} - data: {request_body}).",
            str(context.exception),
        )

        delete.assert_called_with(
            f"{self.endpoint}/products/{product.uuid}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        check_authentication.assert_called_once()

    @patch("micebot.api.delete")
    @patch("micebot.api.Api.get_access_token")
    @patch("micebot.api.Api._check_authentication")
    def test_should_return_the_edited_product_when_http_code_is_200(
        self, check_authentication, get_access_token, delete
    ):
        product = ProductDeleteFactory()
        product_delete_response = ProductDeleteResponseFactory(deleted=True)

        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {
            "deleted": product_delete_response.deleted
        }
        access_token = self.faker.sha256()

        get_access_token.return_value = access_token
        delete.return_value = response

        self.assertEqual(
            product_delete_response, self.api.delete_product(product=product)
        )

        delete.assert_called_with(
            f"{self.endpoint}/products/{product.uuid}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        check_authentication.assert_called_once()
