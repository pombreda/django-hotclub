from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from blog.models import Post
from blog.forms import *

try:
    from notification import models as notification
except ImportError:
    notification = None

def blogs(request):
	blogs = Post.objects.filter(status=2).order_by("-publish")
	return render_to_response("blog/blogs.html", {"blogs": blogs}, context_instance=RequestContext(request))
	
def article(request, username, slug):
	user = User.objects.get(username=username)
	post = get_object_or_404(Post, slug=slug, author=user)
	return render_to_response("blog/article.html", {
						"post": post}, context_instance=RequestContext(request))
	
def yourarticles(request):
	user = request.user
	blogs = Post.objects.filter(author=user)
	return render_to_response("blog/yourarticles.html", {"blogs": blogs}, context_instance=RequestContext(request))
	
@login_required
def new(request):
	if request.user.is_authenticated() and request.method == "POST":
		if request.POST["action"] == "create":
			blog_form = BlogForm(request.POST)
			blog = blog_form.save(commit=False)
			blog.author = request.user
			blog.creator_ip = request.META['REMOTE_ADDR']
			blog.save()
			blog_form = BlogForm()
		else:
			blog_form = BlogForm()
	else:
		blog_form = BlogForm()
	return render_to_response("blog/new.html", {
						"blog_form": blog_form,
						}, context_instance=RequestContext(request))
						
def edit(request, id):
	if request.method == "GET":
		post = get_object_or_404(Post, id=id)
		if post.author == request.user:
			is_author = True
		else:
			is_author = False
		
		if request.user.is_authenticated() and request.method == "POST":
			if request.POST["action"] == "update":
				blog_form = BlogForm(request.POST, instance=post)
				blog = blog_form.save(commit=False)
				blog.save()
			else:
				blog_form = BlogForm(instance=post)
		
		blog_form = BlogForm(instance=post)
	return render_to_response("blog/edit.html", {"is_author": is_author, "blog_form": blog_form}, context_instance=RequestContext(request))