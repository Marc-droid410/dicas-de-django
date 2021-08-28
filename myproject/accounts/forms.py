from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import AuditEntry


class MyAuthenticationForm(AuthenticationForm):

    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
        'invalid_password': _("Senha inválida."),
        'max_attempt': _(
            "Você atingiu o número máximo de tentativas."
            "Estamos te enviando um e-mail."
        ),
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password
            )
            if self.user_cache is None:
                self.check_authentication_error(username)
            else:
                self.confirm_login_allowed(self.user_cache)
            return self.cleaned_data
        else:
            self.validation_field()

    def validation_field(self):
        raise ValidationError(
            'Os campos usuário ou senha devem ser preenchidos.',
            code='invalid_fields',
            params={'username': self.username_field.verbose_name},
        )

    def check_authentication_error(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise self.get_invalid_login_error()
        else:
            self.check_max_attempts(user)
            raise self.get_invalid_password_error()

    def check_max_attempts(self, user):
        max_attempts = AuditEntry.objects.filter(
            username=user.username,
            action='user_login_password_failed'
        ).count()
        if max_attempts >= 2:
            # Enviar email...
            raise self.get_max_attempts_error()

    def get_invalid_password_error(self):
        return ValidationError(
            self.error_messages['invalid_password'],
            code='invalid_password',
            params={'username': self.username_field.verbose_name},
        )

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': self.username_field.verbose_name},
        )

    def get_max_attempts_error(self):
        return ValidationError(
            self.error_messages['max_attempt'],
            code='max_attempt',
            params={'username': self.username_field.verbose_name},
        )
