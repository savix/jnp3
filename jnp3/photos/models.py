# -*- coding: utf-8 -*-

from django.db import models

# Ten model ma zostać zastąpiony własnym, korzystającym z HandlerSocketa
# stworzone tylko do testów zadania asynchronicznego

class Photo(models.Model):
    STATUS_CHOICES = (
        (u'n', u'new'),
        (u'r', u'ready'),
        (u'd', u'deleted'),
    )
    desc = models.TextField()
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    
    def update_status(self, status):
        self.status = status
        self.save()
    
    @staticmethod
    def get(id):
        return Photo.objects.get(id=id)
    
    @staticmethod
    def create(desc):
        return Photo.objects.create(desc=desc, status=u'n')
