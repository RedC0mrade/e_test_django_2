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
