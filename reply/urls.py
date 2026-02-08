from django.urls import path

from . import views

urlpatterns=[
    path('ReadM/<int:pk>', views.ReadView.as_view(), name='readm'),
    path('message/', views.MessageView.as_view(), name='message_list'),
    path('comment/reply/<int:comment_id>/', views.ReplyComment.as_view(), name='reply_comment_page'),
]