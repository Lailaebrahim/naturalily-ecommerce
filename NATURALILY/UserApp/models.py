from django.db import models


class ShopUser(models.Model):
    """
    ShopUser model is a custom user model that extends the default Django User model.
    """
    img = models.ImageField(upload_to='images/users/', default='images/users/default.png')
    phone = models.CharField(max_length=20, null=True)
    joined_at = models.DateField(auto_now_add=True)
    """The related_name attribute in your OneToOneField allows you to access the ShopUser instance
    from the auth.User instance using the attribute name ShopUser."""
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='shopUser')
    
    def __str__(self):
        return self.user.username