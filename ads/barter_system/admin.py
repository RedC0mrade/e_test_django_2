from django.contrib import admin
from .models import Ad, ExchangeProposal


class ExchangeProposalInline(admin.TabularInline):
    """
    Inline-представление предложений обмена в админке объявлений.
    """

    model = ExchangeProposal
    fk_name = "ad_sender"
    extra = 0
    fields = ("ad_receiver", "status", "comment", "created_at")
    readonly_fields = ("created_at",)
    show_change_link = True


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    """
    Админ-модель объявления.
    """

    list_display = (
        "title",
        "user",
        "category",
        "condition",
        "short_description",
        "created_at",
    )
    list_filter = (
        "category",
        "condition",
        "created_at",
        "user",
    )
    search_fields = (
        "title",
        "description",
        "user__username",
    )
    readonly_fields = ("created_at",)
    ordering = ["-created_at"]
    inlines = [ExchangeProposalInline]
    autocomplete_fields = ["user"]


@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    """
    Админ-модель для предложений обмена.
    """

    list_display = (
        "id",
        "get_ad_sender",
        "get_ad_receiver",
        "status",
        "comment",
        "created_at",
    )
    list_filter = (
        "status",
        "created_at",
    )
    search_fields = (
        "ad_sender__title",
        "ad_sender__user__username",
        "ad_receiver__title",
        "ad_receiver__user__username",
        "comment",
    )
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
    list_select_related = (
        "ad_sender",
        "ad_sender__user",
        "ad_receiver",
        "ad_receiver__user",
    )
    autocomplete_fields = ["ad_sender", "ad_receiver"]

    def get_ad_sender(self, obj):
        return f"{obj.ad_sender.title} (ID: {obj.ad_sender.id}, Пользователь: {obj.ad_sender.user.username})"

    get_ad_sender.short_description = "Объявление отправителя"
    get_ad_sender.admin_order_field = "ad_sender__title"

    def get_ad_receiver(self, obj):
        return f"{obj.ad_receiver.title} (ID: {obj.ad_receiver.id}, Пользователь: {obj.ad_receiver.user.username})"

    get_ad_receiver.short_description = "Объявление получателя"
    get_ad_receiver.admin_order_field = "ad_receiver__title"
