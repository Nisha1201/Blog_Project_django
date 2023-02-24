from django.db import models
# from django.conf import settings
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50,default=None,null=True,blank=True)
    last_name = models.CharField(max_length=50,default=None,null=True,blank=True)
    place = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    dob = models.DateField()
    picture = models.ImageField(upload_to='profile_images')

    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_pics')
    likes= models.ManyToManyField(User,related_name="likes",blank=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         if self.likes == 1:
#             return f"{self.author} : {self.title} - {self.likes} Like"
#         elif self.likes == 0:
#             return f"{self.author} : {self.title} - No Likes"
#         else:
#             return f"{self.author} : {self.title} - {self.likes} Likes"


# class Like(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)                                    
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
     
#     def __str__(self):
#         return f"{self.user} liked {self.post}"
#     class Meta:
#         unique_together = ('user', 'post')

# class Dislike(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return f"{self.user} liked {self.post}"
#     class Meta:
#         unique_together = ('user', 'post')


