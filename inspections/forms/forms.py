from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, \
    ReadOnlyPasswordHashField

from ..models import BaseUser, Seller, Customer, Mechanic

# import logging
# log = logging.getLogger(__name__)
# from django.utils.encoding import force_text

#     def is_valid(self):
#         print("hi")
#         log.error(force_text(self.errors))
#         return super(SellerCreationForm, self).is_valid()


class BaseUserCreationForm(UserCreationForm):
    """ Form to be used in creation of a new Person or User instance. """

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
        """ Check for email being unique to JitSpot.
        """
        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data['email']
        try:
            BaseUser._default_manager.get(email=email)
        except Seller.DoesNotExist:
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


class SellerCreationForm(forms.ModelForm):
    """ Form to be used in creation of a new Person or User instance. """

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
        """ Check for email being unique to JitSpot.
        """
        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data['email']
        try:
            Seller._default_manager.get(email=email)
        except Seller.DoesNotExist:
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
        user = super(SellerCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        return user

    class Meta:
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name']
        model = Seller


class CustomerCreationForm(UserCreationForm):
    """ Form to be used in creation of a new Person or User instance. """

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
        """ Check for email being unique to JitSpot.
        """
        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data['email']
        try:
            Customer._default_manager.get(email=email)
        except Customer.DoesNotExist:
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
        user = super(CustomerCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        return user

    class Meta:
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name']
        model = Customer


class MechanicCreationForm(UserCreationForm):
    """ Form to be used in creation of a new Person or User instance. """

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
        """ Check for email being unique to JitSpot.
        """
        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data['email']
        try:
            Mechanic._default_manager.get(email=email)
        except Mechanic.DoesNotExist:
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
        user = super(MechanicCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        return user

    class Meta:
        fields = ['email', 'password1', 'password2', 'first_name',
                  'last_name', 'phone_number', 'address']
        model = Mechanic


class SellerChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=_("Password"), help_text=_(
        "Raw passwords are not stored, so there is no way to see "
        "this user's password, but you can change the password "
        "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = Seller
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SellerChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class CustomerChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=_("Password"), help_text=_(
        "Raw passwords are not stored, so there is no way to see "
        "this user's password, but you can change the password "
        "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = Customer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CustomerChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class MechanicChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=_("Password"), help_text=_(
        "Raw passwords are not stored, so there is no way to see "
        "this user's password, but you can change the password "
        "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = Mechanic
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MechanicChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
