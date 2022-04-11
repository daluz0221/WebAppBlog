import datetime
from django.utils import timezone

from django.db import models

class PublishedPostManager(models.Manager):
   

    def get_queryset(self):
        """
        Obtiene una lista de todos los posts publicados.
        """
        return super(PublishedPostManager, self).get_queryset().filter( active=True)

    def listar_post_por_fecha(self, kword):
        """
        Obtiene una lista de todos los posts publicados dentro de un rango de fecha específico.
        """
        resultado = self.filter(
            title__icontains=kword,
            
        )

        return resultado

    def listar_post_por_fecha2(self, kword, fecha1, fecha2):
        """
        Obtiene una lista de todos los posts publicados dentro de un rango de fecha específico.
        """

        date1 = datetime.datetime.strptime(fecha1, '%Y-%m-%d').date()
        date2 = datetime.datetime.strptime(fecha2, '%Y-%m-%d').date()
        if date1 > date2:
            date1, date2 = date2, date1

        resultado = self.filter(
            created_date__range=(date1, date2)
        )

        return resultado




class ActiveManager(models.Manager):
    
    def activar_post_por_fecha(self):
        """
        manager para activar un post  dependiendo de la fecha que se le pase.
        """      


        fecha_actual = str(datetime.datetime.now())
        print(fecha_actual)

        resultado = self.filter(
            fecha_activacion__lt=fecha_actual
            
        )

            
        return resultado

    def desactivar_post_por_fecha(self):
        """
        manager un post para desactivar un post dependiendo de la fecha que se le pase.
        """     
        

        fecha_actual = str(datetime.datetime.now())
        

        resultado = self.filter(
            fecha_desactivacion__lt=fecha_actual
            
        )    
        return resultado