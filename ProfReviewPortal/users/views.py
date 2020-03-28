from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from review.models import Prof_Review, Course_Review

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'account created for {username}!')
			return redirect('login')
	else:
		form=UserRegisterForm()
	return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
	p_revs = Prof_Review.objects.filter(author = request.user).order_by('-date_posted')[:5]
	c_revs = Course_Review.objects.filter(author = request.user).order_by('-date_posted')[:5]
	pr = request.user.profile
	if pr.warn_offensive:
		messages.warning(request, f'Warning: Do not write offensive posts or your account will be banned!')
		pr.warn_offensive = False
		pr.save()
	return render(request, 'users/profile.html', {'crevs': c_revs, 'prevs': p_revs})
