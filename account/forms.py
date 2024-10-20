from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.contrib.auth.password_validation import validate_password


# create a user registration form
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('phone', 'first_name', 'last_name', 'password1', 'password2')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if self.instance.pk:
            if User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Phone already exists.')
        else:
            if User.objects.filter(phone=phone).exists():
                raise forms.ValidationError('Phone already exists.')

        if not phone.isdigit():
            raise forms.ValidationError('phone must be a number.')

        if not phone.startswith('09'):
            raise forms.ValidationError('phone must start with 09 digits.')

        if len(phone) != 11:
            raise forms.ValidationError('phone must have 11 digits.')

        return phone


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('phone', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if self.instance.pk:
            if User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Phone already exists.')
        else:
            if User.objects.filter(phone=phone).exists():
                raise forms.ValidationError('Phone already exists.')

        if not phone.isdigit():
            raise forms.ValidationError('phone must be a number.')

        if not phone.startswith('09'):
            raise forms.ValidationError('phone must start with 09 digits.')

        if len(phone) != 11:
            raise forms.ValidationError('phone must have 11 digits.')

        return phone


class UserChangeFormNew(UserChangeForm):
    class Meta:
        model = User
        fields = ('phone', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')


class UserUpdateProfileForm(forms.ModelForm):
    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(), required=False)
    password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')  # Exclude password fields from here

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # Validate passwords if provided
        if password1 and password1 != password2:
            raise forms.ValidationError("رمز عبور جدید و تأیید رمز عبور مطابقت ندارد.")

        if password1:
            try:
                validate_password(password=password1)  # Validate the new password
            except forms.ValidationError as e:
                raise forms.ValidationError(e.messages)

        return cleaned_data


    def save(self, commit=True):
        user = super().save(commit=False)

        # Update the user's password if provided
        if self.cleaned_data['password1']:
            user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user
