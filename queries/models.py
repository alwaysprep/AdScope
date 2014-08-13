from django.db import models

# Create your models here.
class TrainQueries(models.Model):
    query = models.CharField(max_length=220)
    relevant = models.BooleanField()
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.query



class TestQueries(models.Model):
    query = models.CharField(max_length=220)
    rsv = models.FloatField()
    processed = models.BooleanField()
    date = models.DateTimeField(auto_now=True)


    def __unicode__(self):
        return self.query


class Words(models.Model):
    word = models.CharField(max_length=75)
    pt = models.FloatField()
    ut = models.FloatField()
    c = models.FloatField()

class Sessions(models.Model):
    confirm_added = models.IntegerField()
    confirm_excluded = models.IntegerField()
    refuse_added = models.IntegerField()
    refuse_excluded = models.IntegerField()

    def __unicode__(self):
        return "(%s, %f)" % (self.word, self.c)



