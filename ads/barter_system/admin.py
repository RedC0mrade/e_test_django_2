from django.contrib import admin
from django.http import HttpRequest
from django.utils.safestring import SafeString
from django.db.models.query import QuerySet

from .models import Ad, ExchangeProposal


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    """
    Админ модель объявления.
    """

    list_display: tuple[str, ...] = (
        "title",
        "user",
        "category",
        "condition",
        "short_description",
        "created_at",
    )
    list_filter: tuple[str, ...] = (
        "category",
        "condition",
        "created_at",
        "user",
    )
    search_fields: tuple[str, ...] = (
        "title",
        "description",
        "user__username",
    )
    readonly_fields: tuple[str, ...] = ("created_at",)
    ordering: list[str] = ["-created_at"]


@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    """
    Админ модель предложениями обмена.
    """

    list_display: tuple[str, ...] = (
        "id",
        "ad_sender_display",
        "ad_receiver_display",
        "status",
        "created_at",
        "short_comment",
    )

    list_filter: tuple[str, ...] = (
        "status",
        "created_at",
    )

    search_fields: tuple[str, ...] = (
        "ad_sender__title",
        "ad_sender__user__username",
        "ad_receiver__title",
        "ad_receiver__user__username",
        "comment",
    )

    readonly_fields: tuple[str, ...] = ("created_at",)
    ordering: list[str] = ["-created_at"]

    def ad_sender_display(self, obj: ExchangeProposal) -> SafeString:
        """
        Форматированное отображение объявления отправителя.
        
        Args:
            obj: Экземпляр модели ExchangeProposal
            
        Returns:
            HTML-безопасная строка с информацией об объявлении
        """
        return admin.utils.display_for_value(f"{obj.ad_sender.title} (ID: {obj.ad_sender.id})")

    ad_sender_display.short_description = "Объявление отправителя"

    def ad_receiver_display(self, obj: ExchangeProposal) -> SafeString:
        """
        Форматированное отображение объявления получателя.
        
        Args:
            obj: Экземпляр модели ExchangeProposal
            
        Returns:
            HTML-безопасная строка с информацией об объявлении
        """
        return admin.utils.display_for_value(f"{obj.ad_receiver.title} (ID: {obj.ad_receiver.id})")

    ad_receiver_display.short_description = "Объявление получателя"

    def short_comment(self, obj: ExchangeProposal) -> str:
        """
        Сокращенная версия комментария для отображения в списке.
        
        Args:
            obj: Экземпляр модели ExchangeProposal
            
        Returns:
            Сокращенный комментарий (первые 50 символов)
        """
        return obj.comment[:50] + "..." if len(obj.comment) > 50 else obj.comment

    short_comment.short_description = "Комментарий"

    def get_queryset(self, request: HttpRequest) -> QuerySet[ExchangeProposal]:
        """
        Оптимизирует запрос к БД с помощью select_related.
        
        Args:
            request: Объект HTTP-запроса
            
        Returns:
            QuerySet с предложениями обмена, включая связанные объявления
        """
        return super().get_queryset(request).select_related(
            "ad_sender",
            "ad_sender__user",
            "ad_receiver",
            "ad_receiver__user",
        )

    def get_readonly_fields(
        self, 
        request: HttpRequest, 
        obj: ExchangeProposal | None = None
    ) -> tuple[str, ...]:
        """
        Определяет, какие поля должны быть только для чтения.
        Для существующих объектов запрещает изменение объявлений.
        
        Args:
            request: Объект HTTP-запроса
            obj: Экземпляр модели или None для нового объекта
            
        Returns:
            Кортеж имен полей только для чтения
        """
        if obj:  # Если объект уже существует
            return self.readonly_fields + ("ad_sender", "ad_receiver")
        return self.readonly_fields