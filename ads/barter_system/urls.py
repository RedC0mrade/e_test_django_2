# from django.urls import path
# from django.contrib.auth import views as auth_views
# from . import views

# urlpatterns = [
#     path(
#         "login/",
#         auth_views.LoginView.as_view(template_name="registration/login.html"),
#         name="login",
#     ),
#     path(
#         "logout/",
#         auth_views.LogoutView.as_view(next_page="login"),
#         name="logout",
#     ),
#     path(
#         "signup/",
#         views.signup_view,
#         name="signup",
#     ),
#     path(
#         "ads/",
#         views.AdListView.as_view(),
#         name="ad_list",
#     ),
#     path(
#         "ads/create/",
#         views.AdCreateView.as_view(),
#         name="ad_create",
#     ),
#     path(
#         "ads/<int:pk>/edit/",
#         views.AdUpdateView.as_view(),
#         name="ad_edit",
#     ),
#     path(
#         "ads/<int:pk>/delete/",
#         views.AdDeleteView.as_view(),
#         name="ad_delete",
#     ),
#     path(
#         "exchange_proposals/filtered/",
#         views.ExchangeProposalFilteredListView.as_view(),
#         name="exchangeproposal_filtered_list",
#     ),
#     path(
#         "exchange_proposals/",
#         views.ExchangeProposalListView.as_view(),
#         name="exchangeproposal_list",
#     ),
#     path(
#         "exchange_proposals/<int:pk>/",
#         views.ExchangeProposalDetailView.as_view(),
#         name="exchangeproposal_detail",
#     ),
#     path(
#         "exchange_proposals/create/",
#         views.ExchangeProposalCreateView.as_view(),
#         name="exchangeproposal_create",
#     ),
#     path(
#         "exchange_proposals/<int:pk>/update/",
#         views.ExchangeProposalUpdateView.as_view(),
#         name="exchangeproposal_update",
#     ),
#     path(
#         "exchange_proposals/<int:pk>/delete/",
#         views.ExchangeProposalDeleteView.as_view(),
#         name="exchangeproposal_delete",
#     ),
# ]
