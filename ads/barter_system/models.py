from django.db import models
from django.contrib.auth.models import User

from django.forms import ValidationError


class Ad(models.Model):
    """
    Модель объявления
    """

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at"]

    class Category(models.TextChoices):
        ELECTRONICS = "electronics", "Электроника"
        CLOTHING = "clothing", "Одежда"
        BOOKS = "books", "Книги"
        OTHER = "other", "Другое"

    class Condition(models.TextChoices):
        NEW = "new", "Новое"
        USED = "used", "Б/у"
        DEFECTIVE = "defective", "С дефектом"

    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER,
        verbose_name="Категория товара",
    )

    condition = models.CharField(
        max_length=20,
        choices=Condition.choices,
        default=Condition.USED,
        verbose_name="Состояние товара",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )

    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок",
    )

    description = models.TextField(
        max_length=1000,
        verbose_name="Описание",
    )

    image_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Ссылка на изображение",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    def __str__(self) -> str:
        return f"{self.title} (Пользователь: {self.user.username})"

    @property
    def short_description(self) -> str:
        """Сокращенное описание (первые 50 символов)"""
        return self.description[:50] + (
            "..." if len(self.description) > 50 else ""
        )


class ExchangeProposal(models.Model):

    class Meta:
        verbose_name = "Предложение обмена"
        verbose_name_plural = "Предложения обмена"
        ordering = ["-created_at"]

    class ProposalStatus(models.TextChoices):
        PENDING = "pending", "В ожидании"
        ACCEPTED = "accepted", "Принято"
        REJECTED = "rejected", "Отклонено"

    ad_sender = models.ForeignKey(
        "Ad",
        related_name="sent_proposals",
        on_delete=models.CASCADE,
        verbose_name="Объявление отправителя",
    )

    ad_receiver = models.ForeignKey(
        "Ad",
        related_name="received_proposals",
        on_delete=models.CASCADE,
        verbose_name="Объявление получателя",
    )

    comment = models.TextField(
        blank=True,
        verbose_name="Комментарий",
    )

    status = models.CharField(
        max_length=20,
        choices=ProposalStatus.choices,
        default=ProposalStatus.PENDING,
        verbose_name="Статус предложения",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    def clean(self):
        if self.ad_sender == self.ad_receiver:
            raise ValidationError("Нельзя создать предложение обмена на одно и то же объявление.")
    
    def __str__(self):
        return f"{self.ad_sender.user.username} предлагает {self.ad_receiver.user.username} обмен ({self.status})"
