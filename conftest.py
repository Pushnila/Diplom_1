from unittest.mock import Mock

import pytest

from praktikum.bun import Bun
from praktikum.burger import Burger
from praktikum.ingredient import Ingredient


@pytest.fixture
def burger():
    return Burger()


@pytest.fixture
def bun():
    return Mock(spec=Bun)


@pytest.fixture
def ingredient():
    return Mock(spec=Ingredient)
