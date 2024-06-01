from enum import Enum


class IngredientType(Enum):
    LIQUOR = 1
    MIXER = 2


class Drink:
    def __init__(self, name: str, ingredients: list[(str, float, IngredientType)]):
        self.name = name
        self.ingredients = ingredients

    def to_string(self):
        content = self.name
        for ingredient in self.ingredients:
            if ingredient[2] == IngredientType.LIQUOR:
                quant = ' shots'
            else:
                quant = ' oz'
            content += '\n' + ingredient[0] + ', ' + str(ingredient[1]) + quant
        return content

    def get_name(self):
        return self.name

    def get_ingredients(self):
        return self.ingredients
