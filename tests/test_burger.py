from unittest.mock import Mock

import pytest

from praktikum.bun import Bun
from praktikum.burger import Burger
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import (
    INGREDIENT_TYPE_FILLING,
    INGREDIENT_TYPE_SAUCE,
)


@pytest.fixture
def burger():
    return Burger()


@pytest.fixture
def bun():
    return Mock(spec=Bun)


@pytest.fixture
def ingredient():
    return Mock(spec=Ingredient)


class TestBurger:

    def test_new_burger_has_no_bun_and_ingredients(self, burger):
        assert burger.bun is None
        assert burger.ingredients == []

    def test_set_buns_saves_bun(self, burger, bun):
        burger.set_buns(bun)

        assert burger.bun == bun

    def test_add_ingredient_adds_ingredient_to_list(
        self,
        burger,
        ingredient
    ):
        burger.add_ingredient(ingredient)

        assert burger.ingredients == [ingredient]

    def test_remove_ingredient_removes_ingredient_by_index(self, burger):
        first_ingredient = Mock(spec=Ingredient)
        second_ingredient = Mock(spec=Ingredient)
        burger.ingredients = [first_ingredient, second_ingredient]

        burger.remove_ingredient(0)

        assert burger.ingredients == [second_ingredient]

    def test_move_ingredient_moves_ingredient_to_new_position(self, burger):
        first_ingredient = Mock(spec=Ingredient)
        second_ingredient = Mock(spec=Ingredient)
        third_ingredient = Mock(spec=Ingredient)
        burger.ingredients = [
            first_ingredient,
            second_ingredient,
            third_ingredient
        ]

        burger.move_ingredient(0, 2)

        assert burger.ingredients == [
            second_ingredient,
            third_ingredient,
            first_ingredient
        ]

    @pytest.mark.parametrize(
        'ingredient_prices, expected_price',
        [
            ([], 200),
            ([50], 250),
            ([50, 25], 275),
        ]
    )
    def test_get_price_returns_buns_and_ingredients_price(
        self,
        burger,
        bun,
        ingredient_prices,
        expected_price
    ):
        bun.get_price.return_value = 100
        burger.set_buns(bun)

        for price in ingredient_prices:
            ingredient = Mock(spec=Ingredient)
            ingredient.get_price.return_value = price
            burger.add_ingredient(ingredient)

        assert burger.get_price() == expected_price

    def test_get_receipt_returns_correct_receipt(self, burger, bun):
        bun.get_name.return_value = 'Краторная булка'
        bun.get_price.return_value = 100

        sauce = Mock(spec=Ingredient)
        sauce.get_type.return_value = INGREDIENT_TYPE_SAUCE
        sauce.get_name.return_value = 'Соус'
        sauce.get_price.return_value = 10

        filling = Mock(spec=Ingredient)
        filling.get_type.return_value = INGREDIENT_TYPE_FILLING
        filling.get_name.return_value = 'Котлета'
        filling.get_price.return_value = 30

        burger.set_buns(bun)
        burger.add_ingredient(sauce)
        burger.add_ingredient(filling)

        expected_receipt = (
            '(==== Краторная булка ====)\n'
            '= sauce Соус =\n'
            '= filling Котлета =\n'
            '(==== Краторная булка ====)\n'
            '\n'
            'Price: 240'
        )

        assert burger.get_receipt() == expected_receipt