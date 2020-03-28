from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

def validate_rating():
	pass
	
class Department(models.Model):
	code = models.CharField(max_length = 2, primary_key = True)
	dept = models.CharField(max_length = 50)

	def __str__(self):
		return self.code

class Prof(models.Model):
	name = models.CharField(max_length = 100)
	dept = models.ForeignKey(Department, on_delete=models.CASCADE)
	info = models.TextField()

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('review-find-prof-name', kwargs = {'pk' : self.pk})

class Course(models.Model):
	name = models.CharField(max_length = 100, unique = True)
	title = models.CharField(max_length = 100)
	dept = models.ForeignKey(Department, on_delete=models.CASCADE)
	info = models.TextField()

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('review-find-course-name', kwargs = {'cname': self.name})

class Prof_Review(models.Model):
	title = models.CharField(max_length=100)
	prof = models.ForeignKey(Prof, on_delete=models.CASCADE)
	review = models.TextField()
	content_quality = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	anonymous = models.BooleanField()
	date_posted = models.DateTimeField(auto_now_add = True)
	date_modif = models.DateTimeField(auto_now = True)
	likes = models.IntegerField(default=0)
	dislikes = models.IntegerField(default=0)
	reports = models.IntegerField(default=0)
	
	class Meta:
		constraints	= [
			models.UniqueConstraint(fields = ['prof', 'author'], name = 'unique_prof_review'),
		]

	def __str__(self):
		return f'{self.title}'
	
	def get_absolute_url(self):
		return reverse('prof-review-detail', kwargs = {'ppk': self.prof.id, 'pk': self.id})

class Course_Review(models.Model):
	title = models.CharField(max_length=100)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	review = models.TextField()
	course_difficulty = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	anonymous = models.BooleanField()
	date_posted = models.DateTimeField(auto_now_add = True)
	date_modif = models.DateTimeField(auto_now = True)
	likes = models.IntegerField(default=0)
	dislikes = models.IntegerField(default=0)
	reports = models.IntegerField(default=0)

	class Meta:
		constraints	= [
			models.UniqueConstraint(fields = ['course', 'author'], name = 'unique_course_review'),
		]

	def __str__(self):
		return f'{self.title}'

	def get_absolute_url(self):
		return reverse('course-review-detail', kwargs = {'cname': self.course.name, 'pk': self.id})

class P_Rev_Like(models.Model):
	post = models.ForeignKey(Prof_Review, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	value = models.IntegerField()
	date = models.DateTimeField(auto_now=True)
	
	class Meta:
		unique_together = ("post", "value", "user")

	def __str__(self):
		return f'{self.post.title}, {self.user.username}, {self.value}' 

class C_Rev_Like(models.Model):
	post = models.ForeignKey(Course_Review, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	value = models.IntegerField()
	date = models.DateTimeField(auto_now=True)
	
	class Meta:
		unique_together = ("post", "value", "user")

	def __str__(self):
		return f'{self.post.title}, {self.user.username}, {self.value}'

class P_Rev_Report(models.Model):
	post = models.ForeignKey(Prof_Review, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now=True)
	
	class Meta:
		unique_together = ("post", "user")

	def __str__(self):
		return f'{self.post.title}, {self.user.username}' 

class C_Rev_Report(models.Model):
	post = models.ForeignKey(Course_Review, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now=True)
	
	class Meta:
		unique_together = ("post", "user")

	def __str__(self):
		return f'{self.post.title}, {self.user.username}'