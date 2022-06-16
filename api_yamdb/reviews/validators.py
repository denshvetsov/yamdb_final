from django.core.exceptions import ValidationError


def validate_rating(value):
    if 1 < value > 10:
        raise ValidationError(
            f'Рэйтинг должен быть в диапазоне от 1 до 10, а не {value}'
        )
