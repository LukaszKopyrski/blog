from django.urls import path
from api.views.auth import LoginView,LogoutView,RefreshTokenView,ResetPasswordView
from api.views.post import PostListCreateView,PostDetailsView
from api.views.post_score import AddPostScoreView,DeletePostScoreView
from api.views.comment import CommentListCreateView, CommentDetailView
from api.views.comment_score import AddCommentScoreView,DeleteCommentScoreView
from api.views.reply import ReplyListCreateView,ReplyDetailView
from api.views.reply_score import AddReplyScoreView,DeleteReplyScoreView
from api.views.register import RegisterView
from api.views.my_account import MyAccountView
from api.views.topics import AllTopicsView,TopicsFilterView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('refreshtoken/',RefreshTokenView.as_view()),
    path('resetpassword/',ResetPasswordView.as_view()),
    path('myaccount/',MyAccountView.as_view()),
    
    path("posts/",PostListCreateView.as_view()),
    path("post/<int:pk>/",PostDetailsView.as_view()),

    path('addpostscore/<int:post_id>/',AddPostScoreView.as_view()),
    path('deletepostscore/<int:post_id>/<str:username>/',DeletePostScoreView.as_view()),
    
    path("comments/<int:post_id>/",CommentListCreateView.as_view()),
    path("comment/<int:pk>/",CommentDetailView.as_view()),
    
    path('addcommentscore/<int:comment_id>/',AddCommentScoreView.as_view()),
    path('deletecommentscore/<int:comment_id>/<str:username>/',DeleteCommentScoreView.as_view()),
    
    path("replies/<int:comment_id>/",ReplyListCreateView.as_view()),
    path("reply/<int:pk>/",ReplyDetailView.as_view()),
    
    path('addreplyscore/<int:reply_id>/',AddReplyScoreView.as_view()),
    path('deletereplyscore/<int:reply_id>/<str:username>/',DeleteReplyScoreView.as_view()),

    
    path('alltopics/',AllTopicsView.as_view()),
    path('findposts/<str:topic>/',TopicsFilterView.as_view()),
    
]
