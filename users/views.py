from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register(request):

	if request.method == "POST":
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, 'Your account has been created! You are able to log in now!')
			return redirect('login')

	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form' : form})

@login_required
def profile(request):

	if request.method == "POST":
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST,
		 							request.FILES,
		  							instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, 'Your account has been updated!')
			return redirect('profile')
	else:
		form_user_update = UserUpdateForm(instance=request.user)
		form_profile_update = ProfileUpdateForm(instance=request.user.profile)

	context = {
		'form_user_update': form_user_update,
		'form_profile_update': form_profile_update

	}

	return render(request, 'users/profile.html', context)

