from django import forms
from .models import Comment
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

class CommentForm(forms.ModelForm):
	captcha = ReCaptchaField(widget=ReCaptchaWidget())
	class Meta:
		model = Comment
		fields = ['content']