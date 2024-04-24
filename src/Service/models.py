from django.db import models
from django.core.validators import RegexValidator

class Client(models.Model):
    national_id = models.CharField(primary_key=True,max_length=12,validators=[RegexValidator(r'^\d{11}$')])
    account_id = models.CharField(max_length=11,validators=[RegexValidator(r'^\d{4,10}$')],blank=True,null=True)
    client_name = models.CharField(max_length=50,blank=True,null=True)    
    phone = models.CharField(max_length=11,validators=[RegexValidator(r'^\d{10}$')],blank=True,null=True)
    mother_firstname = models.CharField(max_length=50,blank=True,null=True)
    mother_lastname = models.CharField(max_length=50,blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    working = models.BooleanField(blank=True,null=True)
    client_status = models.CharField(max_length=50,blank=True,null=True)
    working_field = models.TextField(blank=True,null=True)
    company_name = models.CharField(max_length=50,blank=True,null=True)
    salary = models.PositiveBigIntegerField(blank=True,null=True)
    housing = models.BooleanField(blank=True,null=True)
    married = models.BooleanField(blank=True,null=True)
    spouse_firstname = models.CharField(max_length=50,blank=True,null=True)
    spouse_lastname = models.CharField(max_length=50,blank=True,null=True)
    num_children = models.PositiveBigIntegerField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return f'{self.client_name}_{str(self.created)}'
    
class Service(models.Model):
    client = models.ForeignKey(Client, related_name="services" , on_delete = models.DO_NOTHING)
    service_name = models.CharField(max_length=50)
    amount = models.IntegerField()
    source = models.TextField(blank=True,null=True)
    cause = models.TextField()
    phone = models.CharField(max_length=11,validators=[RegexValidator(r'^\d{10}$')],blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return f'{self.client.client_name}_{self.service_name}_{str(self.created)}'