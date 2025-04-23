from django.db import models

# Create your models here.
# campaigns/models.py

class Campaign(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    target_money_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_money_amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'CAMPAIGNS'
        managed = False


class Donation(models.Model):
    id = models.IntegerField(primary_key=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.DO_NOTHING, db_column='campaign_id')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    donated_at = models.DateTimeField()

    class Meta:
        db_table = 'DONATIONS'
        managed = False
