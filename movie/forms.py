from django import forms

from .models import *

#登录
class Login(forms.Form):
    username = forms.CharField(
        label="昵称",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control required", 'placeholder': '昵称'}),

    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={"class": "form-control required", 'placeholder': '密码'}),
    )

#编辑
class Edit(forms.ModelForm):
    class Meta:
        model = User
        fields = ["password", "username", "email"]
        labels = {
            "password": "密码",
            "name": "昵称",
            "email": "邮箱",
        }
        widgets = {
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

        def clean_name(self):
            name = self.cleaned_data.get("name")
            result = User.objects.filter(name=name)
            if result:
                raise forms.ValidationError("Name already exists")
            return name

#注册
class RegisterForm(forms.Form):
    username = forms.CharField(
        label="昵称(不可重复)",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': '昵称(不可重复)'}),
    )
    email = forms.EmailField(
        label="邮箱", widget=forms.EmailInput(attrs={"class": "form-control", 'placeholder': '邮箱'})
    )
    password1 = forms.CharField(
        label="密码",
        max_length=128,
        widget=forms.PasswordInput(attrs={"class": "form-control", 'placeholder': '密码'}),
    )
    password2 = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(attrs={"class": "form-control", 'placeholder': '确认密码'}),
    )
   #以下为信息验证
    def clean_username(self):
        username = self.cleaned_data.get("username")

        if len(username) < 6:
            raise forms.ValidationError(
                "Your username must be at least 6 characters long."
            )
        elif len(username) > 50:
            raise forms.ValidationError("Your username is too long.")
        else:
            filter_result = User.objects.filter(username=username)
            if len(filter_result) > 0:
                raise forms.ValidationError("Your username already exists.")
        return username

    def clean_name(self):
        name = self.cleaned_data.get("name")
        filter_result = User.objects.filter(name=name)
        if len(filter_result) > 0:
            raise forms.ValidationError("Your name already exists.")
        return name

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 6:
            raise forms.ValidationError("Your password is too short.")
        elif len(password1) > 20:
            raise forms.ValidationError("Your password is too long.")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password mismatch. Please enter again.")
        return password2
