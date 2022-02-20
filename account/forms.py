from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account


class RegistrationForm(UserCreationForm):

    email = forms.EmailField(max_length=255, help_text="Введите действующий адрес")

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2')

    #эти данные из формы с регой, там где я писал name=пасс1, 2 и тд
    # если почта есть, выдаст ошибка, если нет, то всё ок
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.get(email=email) #если данная почта есть, то выдаст ошибку
        except Exception as e:
            return email
        raise forms.ValidationError(f"Почта {email} уже зарегистрирована")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.get(username=username) #если данная почта есть, то выдаст ошибку
        except Exception as e:
            return username
        raise forms.ValidationError(f"Никнейм {username} уже зарегистрирован")


class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=False) #03.11 удалить реквайред

    class Meta:
        model = Account
        fields = ("email", "password")

    #аналогичный логин (внизу описал из файла view)
#    def save(self):
#        email = self.cleaned_data['email']
#        password = self.cleaned_data['password']
#        user = authenticate(email=email, password=password)
#        if user:
#            login(request, user)

    #если без этой функции вводить данные логина, которых нет в БД, то будет одна и та-же ошибка "почта уже существует"
    def clean(self):
       if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Ошибка в пароле или почте")



#из файла view аналогичный логин (вместо def save)
#if user:
#    login(request, user)
#    destination = get_redirect_if_exists(request)
#    if destination:
#       return redirect(destination)
#    return redirect("profile")


class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('username', 'email', 'profile_image', 'hide_email')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email) #если данная почта есть, то выдаст ошибку
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError(f"Почта {email} уже зарегистрирована")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username) #если данная почта есть, то выдаст ошибку
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError(f"Никнейм {username} уже зарегистрирован")
        
    def save(self, commit=True):
        account =  super(AccountUpdateForm, self).save(commit=False)
        account.username = self.cleaned_data['username']
        account.email = self.cleaned_data['email']
        account.profile_image = self.cleaned_data['profile_image']
        account.hide_email = self.cleaned_data['hide_email']
        if commit:
            account.save()
        return account