from unittest.mock import patch, MagicMock

from micebot.api import Api, CodeAlreadyRegistered, UnknownNetworkError
from micebot.model.model import ProductCreation
from test.unit.factories import ProductCreationFactory, ProductFactory
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
    def test_should_return_false_when_http_status_is_401_for_heartbeat(
        self, get
    ):
        response = MagicMock()
        response.status_code = 401

        get.return_value = response

        self.assertFalse(self.api.heartbeat())
        get.assert_called_with(self.endpoint + "/hb")

    @patch("micebot.api.get")
    def test_should_return_false_when_valid_parameter_does_not_exist(
        self, get
    ):
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {}

        get.return_value = response

        self.assertFalse(self.api.heartbeat())
        get.assert_called_with(self.endpoint + "/hb")

    @patch("micebot.api.get")
    def test_should_return_false_when_valid_parameter_is_false(self, get):
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {"valid": False}

        get.return_value = response

        self.assertFalse(self.api.heartbeat())
        get.assert_called_with(self.endpoint + "/hb")

    @patch("micebot.api.get")
    def test_should_return_true_when_valid_parameter_is_true(self, get):
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {"valid": True}

        get.return_value = response

        self.assertTrue(self.api.heartbeat())
        get.assert_called_with(self.endpoint + "/hb")


class TestAddProduct(TestAPI):
    def setUp(self):
        super().setUp()

    @patch("micebot.api.post")
    @patch("micebot.api.Api._check_authentication")
    def test_should_raise_code_already_registered_when_http_status_is_409(
        self, check_authentication, post
    ):
        response = MagicMock()
        response.status_code = 409
        product_creation = ProductCreationFactory()

        post.return_value = response

        with self.assertRaises(CodeAlreadyRegistered) as context:
            self.api.add_product(product_creation)

        self.assertEqual(
            f"{product_creation.code} is already in use by another product.",  # noqa
            str(context.exception),
        )
        check_authentication.assert_called_once()
        # TODO: validate the parameters and headers from /products/ request.

    @patch("micebot.api.post")
    @patch("micebot.api.Api._check_authentication")
    def test_should_raise_unknown_network_error_when_http_status_is_not_409_or_201(  # noqa
        self, check_authentication, post
    ):
        http_status = self.faker.pyint(min_value=202, max_value=408)
        request_body = self.faker.sentence()
        product_creation = ProductCreationFactory()

        response = MagicMock()
        response.status_code = http_status
        response.content = request_body

        post.return_value = response

        with self.assertRaises(UnknownNetworkError) as context:
            self.api.add_product(product_creation)

        self.assertEqual(
            f"Failed to add a product "
            f"(status: {http_status} - data: {request_body}).",
            str(context.exception),
        )
        check_authentication.assert_called_once()
        # TODO: validate the parameters and headers from /products/ request.

    @patch("micebot.api.post")
    @patch("micebot.api.Api._check_authentication")
    def test_should_return_the_product_data_when_http_status_is_201(
        self, check_authentication, post
    ):
        product = ProductFactory()
        product_creation = ProductCreationFactory(
            code=product.code, summary=product.summary
        )

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

        self.assertEqual(product, self.api.add_product(product_creation))

        check_authentication.assert_called_once()
        # TODO: validate the parameters and headers from /products/ request.
