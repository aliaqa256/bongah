from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from .validators import PhoneValidator




class UserManager(BaseUserManager):
    def create_user(self, username, phone_number, password=None, **kwargs):
        if not username:
            raise ValueError("Users must have username")
        if not password:
            raise ValueError("Users must have password")
        if not phone_number:
            raise ValueError("Users must have phone_number")
        user = self.model(username=username,
                          phone_number=phone_number, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_staffuser(self, username, phone_number, password, **kwargs):
        user = self.model(username=username,
                          phone_number=phone_number, staff=True, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, phone_number, password, **kwargs):
        user = self.model(username=username, phone_number=phone_number,
                          staff=True, superuser=True, active=True, **kwargs)
        user.set_password(password)
        user.save()
        return user


# Model User --------------------------------------------------------------------
class User(AbstractBaseUser):
    full_name = models.CharField(
        verbose_name='full name', max_length=250, blank=False, null=False)
    username = models.CharField(verbose_name='username', max_length=200,
                                db_index=True, null=False, blank=False, unique=True)
    email = models.EmailField(verbose_name='email',
                              blank=True, null=True, unique=True,default=None)
    superuser = models.BooleanField(verbose_name='is superuser', default=False)
    staff = models.BooleanField(verbose_name='is staff', default=False)
    active = models.BooleanField(verbose_name='active', default=True)
    created_date = models.DateTimeField(
        verbose_name='created date', auto_now_add=True)
    update_date = models.DateTimeField(
        verbose_name='update date', auto_now=True)

    # phone number with validation
    phone_number = models.CharField(
        verbose_name='phone number', max_length=15, validators=[PhoneValidator], blank=True, null=True)





    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']

    objects = UserManager()

    @property
    def is_active(self):
        return self.active

    @property
    def is_superuser(self):
        return self.superuser

    @property
    def is_staff(self):
        return self.staff

    def __str__(self):
        return "{}".format(self.username)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        ordering = ('id', 'created_date',)
        verbose_name = 'User'
        verbose_name_plural = 'Users'







class Home(models.Model):
    title = models.CharField(verbose_name='title', max_length=250, blank=False, null=False)
    price = models.CharField(verbose_name='price',
                             max_length=250, blank=True, null=True)
    address = models.CharField(verbose_name='address', max_length=250, blank=True, null=True)
    link = models.CharField(verbose_name='link', max_length=250, blank=True, null=True)
    description = models.TextField(verbose_name='description', blank=True, null=True)
    year = models.CharField(verbose_name='year', max_length=250, blank=True, null=True)
    rooms = models.CharField(verbose_name='rooms', max_length=250, blank=True, null=True)
    area = models.CharField(verbose_name='area', max_length=250, blank=True, null=True)
    floor = models.CharField(verbose_name='floor', max_length=250, blank=True, null=True)
    anbari = models.CharField(verbose_name='anbari', max_length=250, blank=True, null=True)
    parking = models.CharField(verbose_name='parking', max_length=250, blank=True, null=True)
    elevator = models.CharField(verbose_name='elevator', max_length=250, blank=True, null=True)
    price_per_meter = models.CharField(verbose_name='price_per_meter', max_length=250, blank=True, null=True)
    total_price = models.CharField(verbose_name='total_price', max_length=250, blank=True, null=True)
    type_of_sell = models.CharField(verbose_name='type_of_sell', max_length=250, blank=True, null=True)
    main_type = models.CharField(verbose_name='main_type', max_length=250, blank=True, null=True)
    sub_type = models.CharField(verbose_name='sub_type', max_length=250, blank=True, null=True)
    contact = models.CharField(verbose_name='contact', max_length=250, blank=True, null=True)
    created_date = models.DateTimeField(
        verbose_name='created date', auto_now_add=True)
    update_date = models.DateTimeField(
        verbose_name='update date', auto_now=True)

    def __str__(self):
        return "{}".format(self.title)
    
    class Meta:
        ordering = ('id', 'created_date',)
        verbose_name = 'Home'
        verbose_name_plural = 'Homes'


class AppTokens(models.Model):
    title=models.CharField(verbose_name='title', max_length=250, blank=False, null=False)
    token=models.CharField(verbose_name='token', max_length=1000, blank=False, null=False)
    created_date = models.DateTimeField(
        verbose_name='created date', auto_now_add=True)
    update_date = models.DateTimeField(
        verbose_name='update date', auto_now=True)
    

    def __str__(self):
        return "{}".format(self.title)
    
    class Meta:
        ordering = ('id', 'created_date',)
        verbose_name = 'AppToken'
        verbose_name_plural = 'AppTokens'
    

class SearchWords(models.Model):
    word = models.CharField(max_length=100)
    user = models.ForeignKey('User', on_delete=models.CASCADE,
                             null=True, blank=True, related_name='search_words')

    def __str__(self):
        return self.word
