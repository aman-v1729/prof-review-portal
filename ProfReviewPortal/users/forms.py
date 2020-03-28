from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ValidationError
from .models import Ban
from datetime import datetime,timedelta
class ExtendedEmailField(forms.EmailField):
	

	def validate(self, value):
		super(forms.EmailField, self).validate(value)
		if not(value.endswith('@iitd.ac.in')):
			raise forms.ValidationError("Use Kerberos Email for registration")
		try:
			User.objects.get(email = value)
			raise forms.ValidationError("Email already registered")
		except User.DoesNotExist:
			now = datetime.now()
			bans = Ban.objects.filter(email = value)
			for ban in bans:
				if ban.permanent:
					raise forms.ValidationError(f'User Banned Permanently')	
			bans = bans.filter(end__gte=now)
			for ban in bans:
				raise forms.ValidationError(f'User Banned till {(ban.end+timedelta(hours = 5, minutes=30)).strftime(" %H:%M:%S, %d/%m/%Y")} IST')
			pass

class UserRegisterForm(UserCreationForm):
	email = ExtendedEmailField()

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


