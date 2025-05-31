from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.core.validators import EmailValidator


# Optional: Extend user model if you want custom fields like role
class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Override groups and user_permissions with unique related_name to avoid clashes
    groups = models.ManyToManyField(
        Group,
        related_name='listings_user_set',  # changed from default 'user_set'
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='listings_user_set',  # changed from default 'user_set'
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
        related_query_name='user',
    )

    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
        validators=[EmailValidator()],
        error_messages={
            'unique': "A user with that email already exists.",
        },
    )
    password_hash = models.CharField(max_length=128, null=False, blank=False)
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    
    def __str__(self):
        return f"{self.username} ({self.role})"

class Listing(models.Model):
    property_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties', limit_choices_to={'role': 'host'})
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    pricepernight = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
    ]
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.booking_id} by {self.user}"

class Review(models.Model):
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('property', 'user')

    def __str__(self):
        return f"Review by {self.user} for {self.property}"
