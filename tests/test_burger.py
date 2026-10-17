from unittest.mock import Mock

import pytest

from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import (
    INGREDIENT_TYPE_FILLING,
    INGREDIENT_TYPE_SAUCE,
)


class TestBurger:

    def test_set_buns_affects_burger_price(self, burger, bun):
        bun.get_price.return_value = 100

        burger.set_buns(bun)

        assert burger.get_price() == 200

    def test_add_ingredient_affects_burger_price(self, burger, bun, ingredient):
        bun.get_price.return_value = 100
        ingredient.get_price.return_value = 50
        burger.set_buns(bun)

        burger.add_ingredient(ingredient)

        assert burger.get_price() == 250

    def test_remove_ingredient_removes_it_from_receipt(self, burger, bun):
        bun.get_name.return_value = 'Bun'
        bun.get_price.return_value = 100
        sauce = Mock(spec=Ingredient)
        sauce.get_type.return_value = INGREDIENT_TYPE_SAUCE
        sauce.get_name.return_value = 'Sauce'
        sauce.get_price.return_value = 10
        filling = Mock(spec=Ingredient)
        filling.get_type.return_value = INGREDIENT_TYPE_FILLING
        filling.get_name.return_value = 'Filling'
        filling.get_price.return_value = 30
        burger.set_buns(bun)
        burger.add_ingredient(sauce)
        burger.add_ingredient(filling)

        burger.remove_ingredient(0)
        receipt = burger.get_receipt()

        assert '= sauce Sauce =' not in receipt
        assert '= filling Filling =' in receipt

    def test_move_ingredient_changes_order_in_receipt(self, burger, bun):
        bun.get_name.return_value = 'Bun'
        bun.get_price.return_value = 100
        first_ingredient = Mock(spec=Ingredient)
        first_ingredient.get_type.return_value = INGREDIENT_TYPE_SAUCE
        first_ingredient.get_name.return_value = 'First'
        first_ingredient.get_price.return_value = 10
        second_ingredient = Mock(spec=Ingredient)
        second_ingredient.get_type.return_value = INGREDIENT_TYPE_FILLING
        second_ingredient.get_name.return_value = 'Second'
        second_ingredient.get_price.return_value = 20
        third_ingredient = Mock(spec=Ingredient)
        third_ingredient.get_type.return_value = INGREDIENT_TYPE_FILLING
        third_ingredient.get_name.return_value = 'Third'
        third_ingredient.get_price.return_value = 30
        burger.set_buns(bun)
        burger.add_ingredient(first_ingredient)
        burger.add_ingredient(second_ingredient)
        burger.add_ingredient(third_ingredient)

        burger.move_ingredient(0, 2)
        receipt = burger.get_receipt()

        assert receipt.index('= filling Second =') < receipt.index('= filling Third =')
        assert receipt.index('= filling Third =') < receipt.index('= sauce First =')

    @pytest.mark.parametrize(
        'ingredient_prices, expected_price',
        [
            ([], 200),
            ([50], 250),
            ([50, 25], 275),
        ],
    )
    def test_get_price_returns_buns_and_ingredients_price(
        self,
        burger,
        bun,
        ingredient_prices,
        expected_price,
    ):
        bun.get_price.return_value = 100
        burger.set_buns(bun)

        for price in ingredient_prices:
            ingredient = Mock(spec=Ingredient)
            ingredient.get_price.return_value = price
            burger.add_ingredient(ingredient)

        assert burger.get_price() == expected_price

    def test_get_receipt_returns_correct_receipt(self, burger, bun):
        bun.get_name.return_value = 'Bun'
        bun.get_price.return_value = 100
        sauce = Mock(spec=Ingredient)
        sauce.get_type.return_value = INGREDIENT_TYPE_SAUCE
        sauce.get_name.return_value = 'Sauce'
        sauce.get_price.return_value = 10
        filling = Mock(spec=Ingredient)
        filling.get_type.return_value = INGREDIENT_TYPE_FILLING
        filling.get_name.return_value = 'Filling'
        filling.get_price.return_value = 30
        burger.set_buns(bun)
        burger.add_ingredient(sauce)
        burger.add_ingredient(filling)

        expected_receipt = (
            '(==== Bun ====)\n'
            '= sauce Sauce =\n'
            '= filling Filling =\n'
            '(==== Bun ====)\n'
            '\n'
            'Price: 240'
        )

        assert burger.get_receipt() == expected_receipt
