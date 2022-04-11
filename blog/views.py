from datetime import datetime, timedelta

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse_lazy, reverse




from users.models import User

from .models import Post, Comment, Category, UserActions
from .forms import ActivePostForm, DeactivePostForm,  Commentform,  PostCreateForm, UpdatePostForm

# Create your views here.







def like_post(request, slug):
    post = get_object_or_404(Post, id=request.POST.get('like_id'))
    
    liked = False

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('blog:post_detail', args=[str(slug)]))


def change_user_role(request, pk):
    """Método para habilitar o deshabilitar el rol de un usuario a administrador"""
    user = get_object_or_404(User, id=request.POST.get('role_id'))
  

    if user.role == 'admin':
        user.role = 'estandar'
        user.save()
    else:
        user.role = 'admin'
        user.save()
    return HttpResponseRedirect(reverse('blog:perfil'))


class CreateCategory(LoginRequiredMixin, CreateView):
    """
    Clase para crear una categoria
    """
    model = Category
    fields = ['name']
    template_name = 'blog/create_category.html'
    success_url = reverse_lazy('blog:perfil')

    def form_valid(self, form):
        
        category = form.instance.name
        UserActions.objects.create(user=self.request.user, category=category, description='Creó una categoria')
        return super().form_valid(form)

    


class PostKeyWordsListView(ListView):
    """Lista de Post por palabra clave"""
    context_object_name = 'obj'
    paginate_by = 2
    template_name = 'blog/list2.html'

    
    def get_queryset(self):
        palabra_clave = self.request.GET.get("search", '')
        print('**********************************************************')
        print(palabra_clave)
        lista = Post.objects.filter(
            title__icontains=palabra_clave
        ).filter(active=True).order_by('publish')
        print(lista)
        return lista
    
    def get_context_data(self, **kwargs):
        context = super(PostKeyWordsListView, self).get_context_data(**kwargs)
       
       
        context['palabra_clave'] = self.request.GET.get("search", '')
        
        return context
    


class PostListView(ListView):
    """
    Clase para listar todos los post
    """

    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'obj'
    paginate_by = 4

    def get_queryset(self):
        """
        Obtiene una lista de todos los posts publicados.

        """
        resultado = Post.act_manager.activar_post_por_fecha()
        if resultado:
            for post in resultado:
                
                post.fecha_activacion = datetime.now() + timedelta(days=7)
                post.active = True
                
                post.save()

        deactivacion = Post.act_manager.desactivar_post_por_fecha()

        if deactivacion:
            for post in deactivacion:
                post.fecha_desactivacion = datetime.now() + timedelta(days=7)
                post.active = False
                post.save()

        return super(PostListView, self).get_queryset().filter( active=True)

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
       
        context['categories'] = Category.objects.all()
        return context

class PostListByCategoryView(ListView):
    """
    Clase para listar todos los post por categoria
    """

    model = Post
    template_name = 'blog/list_by_category.html'
    context_object_name = 'obj'
    paginate_by = 2

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super(PostListByCategoryView, self).get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        
        context['category'] = category
        return context


class CreatePostView(LoginRequiredMixin,CreateView):
    """
    Clase para crear un post
    """

    model = Post
    template_name = 'blog/add_blog.html'
    form_class = PostCreateForm
    success_url = reverse_lazy('blog:post_list')
    Login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.instance.title
        UserActions.objects.create(user=self.request.user, post=post, description='Creó un post')
        return super().form_valid(form)

class PostDetailView(DetailView):
    """
    Clase para mostrar el detalle de un post
    """

    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['comentarios'] = Comment.objects.filter(post=self.get_object(), active=True).order_by('-created')
        context['form'] = Commentform()
        context['liked'] = liked
        return context


class PostByDateView(ListView):
    """
    Clase para listar todos los post por fecha específica
    """

    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'obj'
    paginate_by = 2

    def get_queryset(self):
        palabra_clave = self.request.GET.get("kword", '')
        #Fecha 1
        fecha1 = self.request.GET.get("fecha1", '')
        # Fecha 2
        fecha2 = self.request.GET.get("fecha2", '')
        print(type(fecha1))

        if fecha1 != '' and fecha2 != '':
            # return Post.published.listar_post_por_fecha2(palabra_clave, fecha1, fecha2)
            return Post.objects.filter(created_date__range=(fecha1, fecha2))
            print('entre aqui')
        else:
            print('no entre aqui')
            return Post.objects.filter(active=True)


def post_inactivar(request, slug):
    post = Post.objects.filter(slug=slug).first()
    obj = None
    if not post:
        return redirect("blog:perfil")

    if request.method == 'GET':
        obj = post

    if request.method == 'POST':
        post.active = False
        post.save()
        return redirect("blog:perfil")

    return render(request, "blog/post/inactivar.html", {'obj': obj})


class ActivePostView(LoginRequiredMixin, UpdateView):
    """
    Clase para cambiar el estado de un post a activo
    """
    model = Post
    template_name = 'blog/post/active.html'
    form_class = ActivePostForm
    success_url = reverse_lazy('blog:post_list')
    Login_url = reverse_lazy('users:login')



class DeactivePostView(LoginRequiredMixin, UpdateView):
    """
    Clase para cambiar el estado de un post a inactivo
    """
    model = Post
    template_name = 'blog/post/active.html'
    form_class = DeactivePostForm
    success_url = reverse_lazy('blog:post_list')
    Login_url = reverse_lazy('users:login')
    


class CreateCommentView(LoginRequiredMixin,CreateView):
    """
    Clase para crear un comentario
    """

    model = Comment
    template_name = 'blog/add_comment.html'
    fields = ['body']
    success_url = reverse_lazy('blog:post_list')
    Login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        
        print('hola1')
        comentario = form.instance.body
        print('hola2')
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, slug=self.kwargs['slug'])
        
        UserActions.objects.create(user=self.request.user, comment=comentario, description='Creó un comentario')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.kwargs['slug']])

class UpdatePostView(LoginRequiredMixin, UpdateView):
    """
    Clase para actualizar un post
    """

    model = Post
    template_name = 'blog/update_blog.html'
    form_class = UpdatePostForm
    success_url = reverse_lazy('blog:perfil')
    Login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = self.request.user
        actual_user_id = self.request.user.id
        post_user_id = self.get_object().author.id
        post= self.get_object()
        
        
        if user.role == 'admin' or actual_user_id == post_user_id:

            UserActions.objects.create(user=user, post=post, description='Actualizó un post')

            return super().form_valid(form)

        
    
        else:
            return HttpResponseRedirect(reverse('blog:perfil'))

class UserProfileView(LoginRequiredMixin,ListView):
    """
    Clase para listar los post de un usuario
    """

    model = Post
    template_name = 'blog/perfil.html'
    context_object_name = 'obj'
    paginate_by = 2
    login_url = 'users:login'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user.username)
        return Post.objects.filter(author=user).order_by('-created_date')

    def get_context_data(self, **kwargs):

        context =  super().get_context_data(**kwargs)
        all_post = Post.objects.all()
        all_comments = Comment.objects.all()
        user_post = Post.objects.filter(author=self.request.user)
        print(self.request.user.role)
       

        users = User.objects.all()
        context['users'] = list(users)
        context['all_post'] = all_post
        user = self.request.user
        user_comments = Comment.objects.filter(author=user)
        context['user_comments'] = user_comments 
        context['all_comments'] = all_comments
        context['user_post'] = user_post
        return context


class DeletePostView(LoginRequiredMixin, DeleteView):
    """
    Clase para eliminar un post
    """

    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('blog:perfil')
    login_url = 'users:login'

   

class UserHistoryView(LoginRequiredMixin, ListView):
    """
    Clase para listar acciones de un usuario
    """

    model = UserActions
    template_name = 'blog/history.html'
    context_object_name = 'obj'
    paginate_by = 10
    login_url = 'users:login'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user.username)
        return UserActions.objects.filter(user=user).order_by('-created')


class AllActionsView(LoginRequiredMixin, ListView):
    """
    Clase para listar todas las acciones
    """

    model = UserActions
    template_name = 'blog/all_actions.html'
    context_object_name = 'obj'
    paginate_by = 10
    login_url = 'users:login'

    def get_queryset(self):
        return UserActions.objects.all().order_by('-created')

class UpdateCommentView(LoginRequiredMixin, UpdateView):
    """
    Clase para actualizar un post
    """

    model = Comment
    template_name = 'blog/update_comment.html'
    fields = [ 'body', 'active']
    success_url = reverse_lazy('blog:perfil')
    Login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = self.request.user
        actual_user_id = self.request.user.id
        post_user_id = self.get_object().author.id
        comment = self.get_object()
        
        
        if user.role == 'admin' or actual_user_id == post_user_id:

            UserActions.objects.create(user=user, comment=comment, description='Actualizó un comentario')

            return super().form_valid(form)

        
    
        else:
            return HttpResponseRedirect(reverse('blog:perfil'))


