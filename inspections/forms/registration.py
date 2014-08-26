# http://michalcodes4life.wordpress.com/2014/02/08
# /multiple-user-types-in-django-1-6/

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from ..models import BaseUser, Seller, Mechanic
# Add logging to any form or thing that validates
# import logging
# log = logging.getLogger(__name__)
# from django.utils.encoding import force_text
#     def is_valid(self):
#         print("hi")
#         log.error(force_text(self.errors))
#         return super(<Form>, self).is_valid()


class BaseUserCreationForm(forms.ModelForm):

    """ Form to be used in creation of a new BaseUser or User instance. """

    errorMessages = {
        'duplicateEmail': _("A user with that email already exists."),
        'passwordMismatch': _("The two password fields didn't match."),
    }

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    def clean_email(self):
        """ Check for email being unique to NoLemon.
        """
        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data['email']
        try:
            self._meta.model._default_manager.get(email=email)
        except self._meta.model.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.errorMessages['duplicateEmail'],
            code='duplicateEmail',
        )

    def clean_password1(self):  # cleanPassword2 is in UserCreationForm
        """ Validate that the password has a sufficient level of complexity.
        """
        password = self.cleaned_data["password1"]
        if len(password) <= 3:
            raise forms.ValidationError('Password too short.')
        return password

    def clean_password2(self):
        """ Check if the provided password and its confirmation entry
            are the same.
        """
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch')
        return password2

    def save(self, commit=True):
        """ Save the provided password in a hashed format.
        """
        # Save the provided password in hashed format
        user = super(BaseUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        return user

    class Meta:
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name']
        model = BaseUser


class SellerCreationForm(BaseUserCreationForm):

    """ Form to be used in creation of a new Seller. """

    class Meta:
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name',
                  'city']
        model = Seller


class MechanicCreationForm(BaseUserCreationForm):

    """ Form to be used in creation of a new Mechanic or User instance. """

    class Meta:
        fields = ['email', 'password1', 'password2', 'first_name',
                  'last_name', 'phone_number', 'address', 'city', 'province']
        model = Mechanic


class BaseUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=_("Password"), help_text=_(
        "Raw passwords are not stored, so there is no way to see "
        "this user's password, but you can change the password "
        "using <a href=\"password/\">this form</a>."))

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

    class Meta:
        model = BaseUser
        fields = '__all__'


class SellerChangeForm(BaseUserChangeForm):

    class Meta:
        model = Seller
        fields = '__all__'


class MechanicChangeForm(BaseUserChangeForm):

    class Meta:
        model = Mechanic
        fields = '__all__'
