from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def get_success_url(self):
        next = self.request.GET.get("next")
        if not next:
            return redirect("/login/")

        return redirect(next)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
