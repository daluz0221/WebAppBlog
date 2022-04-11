from datetime import timedelta, datetime



from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField




from users.models import User

from .managers import PublishedPostManager, ActiveManager

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
            
        
        
        self.slug = self.name 
        super(Category, self).save(*args, **kwargs)


class Post(models.Model):
    """
    Definición del modelo Post.
    """

    

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')

    body = RichTextField(blank=True, null=True)
    # body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_data = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    fecha_activacion = models.DateTimeField(default=datetime.now)
    fecha_desactivacion = models.DateTimeField(default=datetime.now)
   

    
   

    
    active = models.BooleanField(default=True)

    objects = models.Manager() # The default manager.
    published = PublishedPostManager() #Custom manager
    act_manager = ActiveManager() #second custom manager

    class Meta:
        ordering = ('-publish',)
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def save(self, *args, **kwargs):
        # Calculamos el total de segundos de la hora actual
        now = datetime.now()
        total_time = timedelta(
            hours=now.hour,
            minutes=now.minute,
            seconds=now.second
        )

        seconds = int(total_time.total_seconds())

        slug_unique = '{} {}'.format(self.title, str(seconds))
        self.slug = slugify(slug_unique)
        super(Post, self).save(*args, **kwargs)

   



class Comment(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    slug = models.SlugField(max_length=200)
    body = RichTextField(blank=True, null=True)
    # body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)   
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)


    def __str__(self):
        return 'Comentario de {} en {}'.format(self.author, self.post)

    def save(self, *args, **kwargs):
        
        
        
        self.slug = self.post.slug 
        super(Comment, self).save(*args, **kwargs)


class UserActions(models.Model):
    """
    Definición del modelo UserActions.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_actions')
    post = models.CharField(max_length=200, default='', blank=True, null=True)
    comment = models.CharField(max_length=200, default='', blank=True, null=True)
    category = models.CharField(max_length=200, default='', blank=True, null=True)
    description = models.CharField(max_length=50, default='')
    created = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return '{} {}'.format(self.user, self.description)