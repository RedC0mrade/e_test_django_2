# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.urls import reverse_lazy
# from django.views import generic
# from .models import Ad, ExchangeProposal
# from .forms import AdForm, ExchangeProposalForm, SignUpForm
# from django.views.generic import CreateView, DeleteView, ListView, UpdateView
# from django.http import HttpResponseForbidden
# from django.db.models import Q
# from django.shortcuts import render, redirect
# from django.contrib.auth import login


# class AdListView(ListView):
#     model = Ad
#     template_name = "ads/ad_list.html"
#     context_object_name = "ads"
#     paginate_by = 10

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         query = self.request.GET.get("q")
#         category = self.request.GET.get("category")
#         condition = self.request.GET.get("condition")

#         if query:
#             queryset = queryset.filter(
#                 Q(title__icontains=query) | Q(description__icontains=query)
#             )
#         if category:
#             queryset = queryset.filter(Category=category)
#         if condition:
#             queryset = queryset.filter(Condition=condition)

#         return queryset


# class AdCreateView(LoginRequiredMixin, CreateView):
#     model = Ad
#     form_class = AdForm
#     template_name = "ads/ad_form.html"
#     success_url = "/ads/"

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)


# class AdUpdateView(LoginRequiredMixin, UpdateView):
#     model = Ad
#     form_class = AdForm
#     template_name = "ads/ad_form.html"
#     success_url = "/ads/"

#     def dispatch(self, request, *args, **kwargs):
#         obj = self.get_object()
#         if obj.user != self.request.user:
#             return HttpResponseForbidden("Вы не автор этого объявления.")
#         return super().dispatch(request, *args, **kwargs)


# class AdDeleteView(LoginRequiredMixin, DeleteView):
#     model = Ad
#     template_name = "ads/confirm_delete.html"
#     success_url = "/ads/"

#     def dispatch(self, request, *args, **kwargs):
#         obj = self.get_object()
#         if obj.user != self.request.user:
#             return HttpResponseForbidden("Вы не можете удалить это объявление")
#         return super().dispatch(request, *args, **kwargs)


# class ExchangeProposalFilteredListView(ListView):
#     model = ExchangeProposal
#     template_name = "exchange_proposals/list.html"
#     context_object_name = "proposals"

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         sender = self.request.GET.get("sender")
#         receiver = self.request.GET.get("receiver")
#         status = self.request.GET.get("status")

#         if sender:
#             queryset = queryset.filter(ad_sender__user__id=sender)
#         if receiver:
#             queryset = queryset.filter(ad_receiver__user__id=receiver)
#         if status:
#             queryset = queryset.filter(status=status)

#         return queryset


# class ExchangeProposalListView(generic.ListView):
#     model = ExchangeProposal
#     template_name = "exchange_proposals/list.html"
#     context_object_name = "proposals"


# class ExchangeProposalDetailView(generic.DetailView):
#     model = ExchangeProposal
#     template_name = "exchange_proposals/detail.html"
#     context_object_name = "proposal"


# class ExchangeProposalCreateView(generic.CreateView):
#     model = ExchangeProposal
#     form_class = ExchangeProposalForm
#     template_name = "exchange_proposals/form.html"
#     success_url = "/exchange_proposals/"


# class ExchangeProposalUpdateView(generic.UpdateView):
#     model = ExchangeProposal
#     form_class = ExchangeProposalForm
#     template_name = "exchange_proposals/form.html"
#     success_url = "/exchange_proposals/"


# class ExchangeProposalDeleteView(generic.DeleteView):
#     model = ExchangeProposal
#     template_name = "exchange_proposals/confirm_delete.html"
#     success_url = "/exchange_proposals/"


# class SignUpView(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy("login")
#     template_name = "signup.html"


# def signup_view(request):
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect("ad_list")  # Заменить на нужную страницу !!!!!!!!!!!!!!!
#     else:
#         form = SignUpForm()
#     return render(request, "registration/signup.html", {"form": form})


from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Ad, ExchangeProposal


# --- Ad Views ---

class AdListView(ListView):
    model = Ad
    template_name = "ads/ad_list.html"
    context_object_name = "ads"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("q")
        category = self.request.GET.get("category")
        condition = self.request.GET.get("condition")

        queryset = Ad.objects.all()

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(user__username__icontains=query)
            )

        if category:
            queryset = queryset.filter(category=category)

        if condition:
            queryset = queryset.filter(condition=condition)

        return queryset.select_related("user")


class AdDetailView(DetailView):
    model = Ad
    template_name = "ads/ad_detail.html"
    context_object_name = "ad"


class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    fields = ["title", "description", "category", "condition", "image_url"]
    template_name = "ads/ad_form.html"
    success_url = reverse_lazy("ad_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AdUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ad
    fields = ["title", "description", "category", "condition", "image_url"]
    template_name = "ads/ad_form.html"
    success_url = reverse_lazy("ad_list")

    def test_func(self):
        return self.get_object().user == self.request.user


class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ad
    template_name = "ads/ad_confirm_delete.html"
    success_url = reverse_lazy("ad_list")

    def test_func(self):
        return self.get_object().user == self.request.user


# --- ExchangeProposal Views ---

class ExchangeProposalCreateView(LoginRequiredMixin, CreateView):
    model = ExchangeProposal
    fields = ["ad_receiver", "comment"]
    template_name = "exchange/proposal_form.html"
    success_url = reverse_lazy("ad_list")

    def form_valid(self, form):
        ad_sender_id = self.kwargs.get("ad_id")
        form.instance.ad_sender = Ad.objects.get(id=ad_sender_id)

        if form.instance.ad_sender.user != self.request.user:
            return self.form_invalid(form)

        return super().form_valid(form)


class ExchangeProposalListView(LoginRequiredMixin, ListView):
    model = ExchangeProposal
    template_name = "exchange/proposal_list.html"
    context_object_name = "proposals"

    def get_queryset(self):
        return ExchangeProposal.objects.filter(
            Q(ad_sender__user=self.request.user) |
            Q(ad_receiver__user=self.request.user)
        ).select_related("ad_sender", "ad_receiver")


class ExchangeProposalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ExchangeProposal
    fields = ["status"]
    template_name = "exchange/proposal_update.html"
    success_url = reverse_lazy("proposal_list")

    def test_func(self):
        proposal = self.get_object()
        return proposal.ad_receiver.user == self.request.user


class ExchangeProposalDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ExchangeProposal
    template_name = "exchange/proposal_confirm_delete.html"
    success_url = reverse_lazy("proposal_list")

    def test_func(self):
        proposal = self.get_object()
        return proposal.ad_sender.user == self.request.user
