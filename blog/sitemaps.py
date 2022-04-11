from django.contrib.sitemaps import Sitemap

from .models import Post

class PostSitemap(Sitemap):

    """
    Clase para mostrar la prioridad de los posts y con qué frecuencia se actualizan
    """
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.publish