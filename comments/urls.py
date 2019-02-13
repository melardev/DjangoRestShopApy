from django.conf.urls import url

from comments.views import CommentListView, CommentDetailsView

app_name = 'comments'
urlpatterns = [
    url(r'^products/(?P<slug>([a-z0-9-])+)/comments$', CommentListView.as_view(), name='commnet_list'),
    url(r'^comments/(?P<pk>([a-z0-9-])+)$', CommentDetailsView.as_view(), name='comment_details_short'),
    url(r'^products/(?P<slug>([a-z0-9-])+)/comments/(?P<pk>([a-z0-9-])+)$', CommentDetailsView.as_view(),
        name='comment_details'),

]
