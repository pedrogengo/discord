from unittest.case import TestCase

from faker import Faker


class Test(TestCase):
    def setUp(self):
        self.faker = Faker("pt_BR")
