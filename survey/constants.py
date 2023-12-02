from django.db.models import IntegerChoices, TextChoices


class AnswerValue(IntegerChoices):
    NoAnswer = 0, "Sin Responder"
    VeryLow = 1, "Muy Bajo"
    Low = 2, "Bajo"
    Regular = 3, "Regular"
    High = 4, "Alto"
    VeryHigh = 5, "Muy Alto"


class LikeValue(TextChoices):
    Liked = "like", "Me gusta"
    Disliked = "dislike", "Me gusta"
