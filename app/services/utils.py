def calculate_choice_weights(choices_modifiers):
    total = sum(choices_modifiers)
    return [choice / total for choice in choices_modifiers]