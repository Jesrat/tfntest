from django.contrib.auth import views as auth_views

class GenLoginView(auth_views.LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True


class GenLogoutView(auth_views.LogoutView):
    next_page = 'login'
