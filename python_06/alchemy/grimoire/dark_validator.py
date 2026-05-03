
from .dark_spellbook import dark_spell_allowed_ingredients

def validate_ingredients(ingredients: str) -> str:
    allowed_list = dark_spell_allowed_ingredients()
    lower_ingredients = ingredients.lower()
    for i in allowed_list:
        if i in lower_ingredients:
            return(ingredients + " - VALID")
    return(ingredients + "- INVALID")