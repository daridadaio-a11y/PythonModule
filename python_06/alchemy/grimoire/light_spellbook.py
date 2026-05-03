def light_spell_allowed_ingredients() -> list:
    return(["earth", "air", "fire", "water"])

def light_spell_record(spell_name: str, ingredients: str) -> str:
    from .light_validator import validate_ingredients
    return(f"Spell recorded: {spell_name} ({validate_ingredients(ingredients)})")