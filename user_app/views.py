import random
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView
from .models import CustomUser
from .forms import RegistrationForm, VerificationForm
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'user_app/home.html'

class RegisterView(View):
    def get(self, request):
        return render(request, 'user_app/register.html', {'form': RegistrationForm()})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            user.verification_code = code
            user.is_active = False
            user.save()

            send_mail(
                'Код подтверждения от Shop',
                f'Ваш код подтверждения: {code}',
                'gleb29032006@gmail.com',
                [user.email],
                fail_silently=False,
            )

            request.session['user_id'] = user.id
            return redirect('verify')
        return render(request, 'user_app/register.html', {'form': form})

class VerifyEmailView(View):
    def get(self, request):
        return render(request, 'user_app/verify.html', {'form': VerificationForm()})

    def post(self, request):
        form = VerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            user = CustomUser.objects.get(id=request.session['user_id'])
            if user.verification_code == code:
                user.email_verified = True
                user.is_active = True
                user.save()
                login(request, user)
                return redirect('home')
            form.add_error('code', 'Неверный код подтверждения')
        return render(request, 'user_app/verify.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'user_app/login.html'

    def form_valid(self, form):
        user = form.get_user()
        if not user.email_verified:
            return redirect('verify')
        login(self.request, user)
        return redirect('home')