from django.shortcuts import render,redirect
from .models import Course, Prof, Prof_Review, Course_Review, P_Rev_Like, C_Rev_Like, P_Rev_Report, C_Rev_Report
from django.contrib import messages
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from users.models import Profile

def home(request):
	return render(request, 'review/home.html')

def findprof(request):
	pro = Prof.objects.order_by('name')
	if request.method == 'POST':
		pname = request.POST['pname']
		matches = Prof.objects.filter(name__icontains=pname).order_by('name')
		ct = 0
		for match in matches:
			ct+=1
		if(ct > 0):
			return render(request, 'review/findprof.html', {'profs': pro, 'matches': matches, 'ct': ct})
		else:
			messages.info(request, f'No results found for \"{pname}\"!')
	return render(request, 'review/findprof.html', {'profs': pro})

def findcourse(request):
	crs = Course.objects.order_by('name')
	if request.method == 'POST':
		cname = request.POST['cname']
		matches = Course.objects.filter(name__icontains=cname).order_by('name')
		ct = 0
		for match in matches:
			ct+=1
		if(ct > 0):
			return render(request, 'review/findcourse.html', {'courses': crs, 'matches': matches, 'ct': ct})
		else:
			messages.info(request, f'No reviews found for \"{cname}\"!')
	return render(request, 'review/findcourse.html', {'courses': crs})

def findcoursename(request, cname):
	crs = Course.objects.get(name=cname)
	matches = Course_Review.objects.filter(course=crs).order_by('-date_posted')
	ct = 0
	for match in matches:
		ct += 1
	return render(request, 'review/course_template.html', {'course': crs, 'matches': matches, 'ct': ct})

def findprofname(request, pk):
	prf = Prof.objects.get(id = pk)
	matches = Prof_Review.objects.filter(prof=prf).order_by('-date_posted')
	ct = 0
	for match in matches:
		ct += 1
	return render(request, 'review/prof_template.html', {'prof': prf, 'matches': matches, 'ct': ct})

class ProfCreateView(LoginRequiredMixin, CreateView):
	model = Prof
	fields = ['name', 'dept', 'info']

class CourseCreateView(LoginRequiredMixin, CreateView):
	model = Course
	fields = ['name', 'title', 'dept', 'info']

class CourseReviewDetailView(DetailView):
	model = Course_Review

class CourseReviewCreateView(LoginRequiredMixin, CreateView):
	model = Course_Review
	fields = ['title', 'review', 'course_difficulty', 'anonymous']

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.course = Course.objects.get(name = self.kwargs.get('cname'))
		#checker = Course_Review.objects.filter(course = form.instance.course).filter(name = )
		return super().form_valid(form)

class CourseReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Course_Review
	fields = ['title', 'review', 'course_difficulty', 'anonymous']

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.course = Course.objects.get(name = self.kwargs.get('cname'))
		return super().form_valid(form)

	def test_func(self):
		c_rev = self.get_object()
		return self.request.user == c_rev.author

class CourseReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Course_Review
	
	def test_func(self):
		c_rev = self.get_object()
		return self.request.user == c_rev.author

	def get_success_url(self):
		messages.info(self.request, 'Review Deleted!')
		return reverse_lazy('review-find-course-name', kwargs = {'cname': self.get_object().course.name})


class ProfReviewDetailView(DetailView):
	model = Prof_Review

class ProfReviewCreateView(LoginRequiredMixin, CreateView):
	model = Prof_Review
	fields = ['title', 'review', 'content_quality', 'anonymous']

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.prof = Prof.objects.get(id = self.kwargs.get('ppk'))
		#checker = Course_Review.objects.filter(course = form.instance.course).filter(name = )
		return super().form_valid(form)

class ProfReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Prof_Review
	fields = ['title', 'review', 'content_quality', 'anonymous']

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.prof = Prof.objects.get(id = self.kwargs.get('ppk'))
		return super().form_valid(form)

	def test_func(self):
		p_rev = self.get_object()
		return self.request.user == p_rev.author

class ProfReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Prof_Review
	
	def test_func(self):
		p_rev = self.get_object()
		return self.request.user == p_rev.author

	def get_success_url(self):
		messages.info(self.request, 'Review Deleted!')
		return reverse_lazy('review-find-prof-name', kwargs = {'pk': self.get_object().prof.id})

@login_required
def ProfReviewPref(request, ppk, pk, pref):
	if request.method == 'POST':
		revpost = get_object_or_404(Prof_Review, id = pk)
		if revpost.author == request.user:
			return redirect('review-find-prof-name',  pk = ppk)
		profil = revpost.author.profile
		pref = int(pref)
		try:
			obj = P_Rev_Like.objects.get(user = request.user, post = revpost)
			val = obj.value
			if val != pref:
				obj.delete()
				upref = P_Rev_Like()
				upref.user = request.user
				upref.post = revpost
				upref.value = pref

				if pref == 1:
					revpost.likes += 1
					profil.rp += 10
					revpost.dislikes -= 1
				elif pref == 2:
					revpost.likes -= 1
					profil.rp -= 10
					revpost.dislikes += 1
				profil.save()
				upref.save()
				revpost.save()
			elif val == pref:
				obj.delete()
				if pref == 1:
					revpost.likes -= 1
					profil.rp -= 10
				elif pref == 2:
					revpost.dislikes -= 1
				revpost.save()
				profil.save()
			return redirect('review-find-prof-name',  pk = ppk)
		except P_Rev_Like.DoesNotExist:
			upref = P_Rev_Like()
			upref.user = request.user
			upref.post = revpost
			upref.value = pref
			if pref == 1:
				revpost.likes += 1
				profil.rp += 10
			elif pref == 2:
				revpost.dislikes += 1
			upref.save()
			profil.save()
			revpost.save()
			return redirect('review-find-prof-name',  pk = ppk)
	else:
		return redirect('review-find-prof-name',  pk = ppk)


@login_required
def CourseReviewPref(request, cname, pk, pref):
	if request.method == 'POST':
		revpost = get_object_or_404(Course_Review, id = pk)
		if revpost.author == request.user:
			return redirect('review-find-course-name',  cname = cname)
		profil = revpost.author.profile
		pref = int(pref)
		try:
			obj = C_Rev_Like.objects.get(user = request.user, post = revpost)
			val = obj.value
			if val != pref:
				obj.delete()
				upref = C_Rev_Like()
				upref.user = request.user
				upref.post = revpost
				upref.value = pref

				if pref == 1:
					revpost.likes += 1
					profil.rp += 10
					revpost.dislikes -= 1
				elif pref == 2:
					revpost.likes -= 1
					profil.rp -= 10
					revpost.dislikes += 1
				upref.save()
				revpost.save()
				profil.save()
			elif val == pref:
				obj.delete()
				if pref == 1:
					revpost.likes -= 1
					profil.rp -= 10
				elif pref == 2:
					revpost.dislikes -= 1
				revpost.save()
				profil.save()
			return redirect('review-find-course-name',  cname = cname)
		except C_Rev_Like.DoesNotExist:
			upref = C_Rev_Like()
			upref.user = request.user
			upref.post = revpost
			upref.value = pref
			if pref == 1:
				revpost.likes += 1
				profil.rp += 10
			elif pref == 2:
				revpost.dislikes += 1
			upref.save()
			revpost.save()
			profil.save()
			return redirect('review-find-course-name',  cname = cname)
	else:
		return redirect('review-find-course-name',  cname = cname)

@login_required
def ProfReviewReport(request, ppk, pk):
	if request.method == 'POST':
		revpost = get_object_or_404(Prof_Review, id = pk)
		try:
			obj = P_Rev_Report.objects.get(user = request.user, post = revpost)
			obj.delete()
			revpost.reports -= 1
			revpost.save()
			return redirect('review-find-prof-name',  pk = ppk)
		except P_Rev_Report.DoesNotExist:
			upref = P_Rev_Report()
			upref.user = request.user
			upref.post = revpost
			revpost.reports += 1
			upref.save()
			revpost.save()
			return redirect('review-find-prof-name',  pk = ppk)
	else:
		return redirect('review-find-prof-name',  pk = ppk)

@login_required
def CourseReviewReport(request, cname, pk):
	if request.method == 'POST':
		revpost = get_object_or_404(Course_Review, id = pk)
		try:
			obj = C_Rev_Report.objects.get(user = request.user, post = revpost)
			obj.delete()
			revpost.reports -= 1
			revpost.save()
#			return findcoursename(request, cname)
			return redirect('review-find-course-name',  cname = cname)
		except C_Rev_Report.DoesNotExist:
			upref = C_Rev_Report()
			upref.user = request.user
			upref.post = revpost
			revpost.reports += 1
			upref.save()
			revpost.save()
			return redirect('review-find-course-name',  cname = cname)
	else:
		return redirect('review-find-course-name',  cname = cname)
