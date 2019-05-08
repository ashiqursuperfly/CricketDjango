from django.db import models

# Create your models here.
class Players(models.Model):
    player_id = models.IntegerField(primary_key=True)
    full_name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    batting_style = models.CharField(max_length=100, blank=True, null=True)
    bowling_style = models.CharField(max_length=100, blank=True, null=True)
    speciality = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.full_name + ' ' + str(self.speciality)
    class Meta:
        managed = False
        db_table = 'players'

