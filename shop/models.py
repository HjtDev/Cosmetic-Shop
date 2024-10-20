from django.db import models
from django.shortcuts import reverse


class Faq(models.Model):
    question = models.CharField(verbose_name='سوال', max_length=200)
    answer = models.TextField(verbose_name='جواب')
    is_visible = models.BooleanField(verbose_name='نمایش در سایت')

    def __str__(self):
        return self.question

    def get_absolute_url(self):
        return reverse('shop:faq')

    class Meta:
        verbose_name = 'سوال متداول'
        verbose_name_plural = 'سوالات متداول'
