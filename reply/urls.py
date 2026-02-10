from django.urls import path

from . import views

urlpatterns=[
    path('ReadM/<int:pk>/', views.ReadView.as_view(), name='readm'),
    path('message/', views.MessageView.as_view(), name='message_list'),
    path('comment/reply/<int:comment_id>/', views.ReplyComment.as_view(), name='reply_comment_page'),
    path('comment/update/<int:comment_id>/',views.CommentUpdate.as_view(),name='comment_update'),
    path('comment/delete/<int:comment_id>/',views.CommentDelete.as_view(),name='comment_delete'),
    path('message/edit/<int:message_id>/', views.MessageEditView.as_view(), name='message_edit'),
    path('message/delete/<int:message_id>/',views.MessageDeleteView.as_view(),name='message_delete'),
    path('message/reply/<int:message_id>/', views.ReplyMessageView.as_view(), name='reply_message'),
]
