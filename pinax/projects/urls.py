from django.conf.urls.defaults import *

from projects.models import Project
from wiki import models as wiki_models


wiki_args = {
    'group_slug_field': 'slug',
    'group_qs': Project.objects.all()
}


urlpatterns = patterns('',
    url(r'^$', 'projects.views.projects', name="projects_list"),
    # @@@ what to do about clash with project with slug 'your_projects'?
    url(r'^your_projects/$', 'projects.views.your_projects', name="your_projects"),
    url(r'^(\w+)/$', 'projects.views.project', name="project_detail"),

    # topics
    url(r'^(\w+)/topics/$', 'projects.views.topics', name="project_topics"),
    url(r'^topic/(\d+)/$', 'projects.views.topic', name="project_topic"),

    # tasks
    url(r'^(\w+)/tasks/$', 'projects.views.tasks', name="project_tasks"),
    url(r'^task/(\d+)/$', 'projects.views.task', name="project_task"),
    url(r'^tasks/(\w+)/$', 'projects.views.user_tasks', name="project_user_tasks"),

    # wiki
    url(r'^(?P<group_slug>\w+)/wiki/', include('wiki.urls'), kwargs=wiki_args),
)
