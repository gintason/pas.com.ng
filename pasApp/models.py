from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'categories'
  
    def __str__(self): 
        return self.name
     
class Product(models.Model):
    name = models.CharField(max_length=225)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='static/images')

    def __str__(self):
        return self.name
    

class Interview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
   
    def __str__(self):
        return self.question

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"