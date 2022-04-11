from django.urls import path

from .views import  PostListView, PostDetailView, like_post, UserProfileView, change_user_role, PostListByCategoryView, CreatePostView,  UpdatePostView, PostByDateView, CreateCommentView, UserHistoryView,post_inactivar, UpdateCommentView, AllActionsView, ActivePostView, DeactivePostView, PostKeyWordsListView,CreateCategory

app_name = 'blog'

urlpatterns = [

    #mostrar posts
    path('', PostListView.as_view(), name='post_list'),
    path('lista/', PostByDateView.as_view(), name='post_by_date'),
    path('category/<slug>/', PostListByCategoryView.as_view(), name='post_list_by_category'),
    path('buscar-post/', PostKeyWordsListView.as_view(), name='post_list_palabra_clave'),
    path('post/<slug>/', PostDetailView.as_view(), name='post_detail'),

    #CRUD posts
    path('new-post/', CreatePostView.as_view(), name='add_blog'),
    path('update-post/<pk>/', UpdatePostView.as_view(), name='post_updated'),
    path('inactivar-post/<slug>/', post_inactivar, name='post_deleted'),
    
    #Crear categorias
    path('new-category/', CreateCategory.as_view(), name='add_category'),
   
    #CRUD comments
    path('add-comment/<slug>/', CreateCommentView.as_view(), name='add_comment'), 
    path('update-comment/<pk>/', UpdateCommentView.as_view(), name='comment_updated'),

    #Páginas de zona usuario y administrador
    path('perfil', UserProfileView.as_view(), name='perfil'),
    path('history/', UserHistoryView.as_view(), name='user_history'),
    path('all-history', AllActionsView.as_view(), name='all_actions'),
    path('activar-programado/<slug>/', ActivePostView.as_view(), name='program_active_post'),
    path('desactivar-programado/<slug>/', DeactivePostView.as_view(), name='program_deactive_post'),
    path('change_role/<pk>', change_user_role, name='change_role'),
    
    #Likes
    path('like/<slug>/', like_post, name='likes'),
]