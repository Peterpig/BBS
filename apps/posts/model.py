# -*- coding: utf-8 -*-
from django.db import models
from DjangoUeditor.models import UEditorField

class NewArticle(models.Model):
    """发表文章model"""
    Name=models.CharField('name',max_length=100,blank=True)
    Content=UEditorField(
                    u'内容   ',
                    width=600, 
                    height=300, 
                    toolbars="full", 
                    imagePath="", 
                    filePath="", 
                    upload_settings={"imageMaxSize":1204000},
                    settings={},
                    command=None,
                    blank=True
                )