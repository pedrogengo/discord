from unittest.case import TestCase

from faker import Faker


class Test(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.faker = Faker("pt_BR")
