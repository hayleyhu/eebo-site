from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class category(models.Model):
    name = models.CharField(u'name', max_length=50)

    def __unicode__(self):
        return self.name

class word(models.Model):
    theword = models.CharField(u'word', max_length=200)
    index = models.CharField(u'index', max_length=50)
    category = models.ForeignKey(u'category', blank=True, null=True)

    def __unicode__(self):
        return self.theword


class item(models.Model):
    file_position = models.CharField(u'file_position', max_length=200, blank=True, null=True)
    kwicl = models.CharField(u'kwicl',max_length=200, blank=True, null=True)
    keyword = models.CharField(u'keyword', max_length=200, blank=True, null=True)
    kwicr = models.CharField(u'kwicr', max_length=200, blank=True, null=True)
    choice1 = models.CharField(u'choice1', max_length=200, blank=True, null=True)
    choice2 = models.CharField(u'choice2', max_length=200, blank=True, null=True)
    choice3 = models.CharField(u'choice3', max_length=200, blank=True, null=True)
    correct_choice = models.CharField(u'correct_choice', max_length=200, blank=True, null=True)


    def __unicode__(self):
        return self.keyword

#CORRECTION_CHOICES = ((0, '--'),(1, 'choice 1 is correct'), (2, 'choice 2 is correct'), (3, 'choice 3 is correct'), (4, 'No choice is correct'), (5, 'No choice is given'), (6, 'Wrong number of black dots (and/or no comp choice given)'), (7, 'Foreign'))
APPROVAL_CHOICES = ((1, 'approve'), (-1, 'reject'), (0, 'hold'))
CORRECTION_CHOICES = ((0, '--'),(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'))





class correction(models.Model):

    corrected_word = models.ForeignKey(item)
    correction_author = models.ForeignKey(User)
    correction_made = models.IntegerField(u'correction_made', choices=CORRECTION_CHOICES)
    correction_word = models.CharField(u'correction_word', max_length=200, blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    approved = models.IntegerField(u'approved', choices=APPROVAL_CHOICES, blank=True, null=True)

    def __unicode__(self):
        return str(self.time)
