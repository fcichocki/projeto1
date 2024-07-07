from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import CustomUserChangeForm
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return '/index'

# A view que você irá usar na URL


def custom_login_view(request):
    if request.user.is_authenticated:
        return redirect('/index')
    else:
        return CustomLoginView.as_view()(request)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redireciona para a página de login após o cadastro bem-sucedido
            return redirect(reverse('login'))
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def usuarios_cadastrados(request):
    users = User.objects.all()
    for user in users:
        user.edit_form = CustomUserChangeForm(instance=user)
        user.password_form = PasswordChangeForm(user=user)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, pk=user_id)

        if 'delete_user' in request.POST:
            user.delete()
            messages.success(request, 'Usuário excluído com sucesso!')
            return redirect('usuarios_cadastrados')

        if 'change_password' in request.POST:
            password_form = user.password_form = PasswordChangeForm(
                user, request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Senha alterada com sucesso!')
                return redirect('usuarios_cadastrados')
            else:
                messages.error(request, 'Erro ao alterar a senha.')

        else:
            edit_form = user.edit_form = CustomUserChangeForm(
                request.POST, instance=user)
            if edit_form.is_valid():
                edit_form.save()
                messages.success(
                    request, 'Dados do usuário atualizados com sucesso!')
                return redirect('usuarios_cadastrados')
            else:
                messages.error(
                    request, 'Erro ao atualizar os dados do usuário.')

    return render(request, 'usuarioscadastrados.html', {'users': users})


def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        messages.success(request, 'Usuário atualizado com sucesso!')
        return redirect('usuarios_cadastrados')
    return redirect('usuarios_cadastrados')


def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=user_id)
        user.delete()
        messages.success(request, 'Usuário excluído com sucesso!')
        return redirect('usuarios_cadastrados')
    else:
        messages.error(request, 'Método não permitido.')
        return redirect('usuarios_cadastrados')
