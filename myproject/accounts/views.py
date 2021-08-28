from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import MyAuthenticationForm
from .models import AuditEntry
from .signals import user_login_password_failed


def logged(request):
    template_name = 'accounts/logged.html'
    return render(request, template_name)


class MyLoginView(LoginView):
    form_class = MyAuthenticationForm

    def form_invalid(self, form):
        username = form.data.get('username')
        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                pass
            else:
                # Dispara o sinal quando o usuário existe, mas a senha está errada.
                user_login_password_failed.send(
                    sender=__name__,
                    request=self.request,
                    user=user
                )

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        user = form.get_user()
        # Zera o AuditEntry
        AuditEntry.objects.filter(
            username=user.username,
            action='user_login_password_failed'
        ).delete()
        return HttpResponseRedirect(self.get_success_url())
