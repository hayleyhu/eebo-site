from django.db import models

# Create your models here.
class category(models.Model):
    name = models.CharField(u'name', max_length=50)

    def __unicode__(self):
        return self.name

class word(models.Model):
    theword = models.CharField(u'word', max_length=200)
    index = models.CharField(u'index', max_length=50)
    category = models.ForeignKey('category', blank=True, null=True)


    def __unicode__(self):
        return self.theword


class item(models.Model):
    file_position = models.CharField(u'file_position', max_length=200, blank=True, null=True)
    kwicl = models.TextField(u'kwicl', blank=True, null=True)
    keyword = models.CharField(u'keyword', max_length=200, blank=True, null=True)
    kwicr = models.TextField(u'kwicr', blank=True, null=True)
    choice1 = models.CharField(u'choice1', max_length=200, blank=True, null=True)
    choice2 = models.CharField(u'choice2', max_length=200, blank=True, null=True)
    choice3 = models.CharField(u'choice3', max_length=200, blank=True, null=True)
    correct_choice = models.CharField(u'correct_choice', max_length=200, blank=True, null=True)


    def __unicode__(self):
        return self.keyword


# class correction(models.Model):
#     corrected_word = models.CharField(u'word', max_length=200)
#     author = models.CharField(u'index', max_length=50)
#     correction_made = models.ChoiceField(choices=[(x, x) for x in range(1, 7)])
#     # time =
