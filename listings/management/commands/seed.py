import random
from django.core.management.base import BaseCommand
from listings.models import Listing
from listings.models import User
import uuid

class Command(BaseCommand):
    help = 'Seed the database with sample listings'

    def handle(self, *args, **kwargs):
        # Create a host user if not exist
        host, created = User.objects.get_or_create(
            username='hostuser',
            defaults={
                'email': 'host@example.com',
                'role': 'host',
                'first_name': 'Host',
                'last_name': 'User',
                'password': 'pbkdf2_sha256$dummyhashedpassword',  # For real usage, use set_password
            }
        )
        if created:
            host.set_password('password123')
            host.save()

        Listing.objects.all().delete()  # Clear previous listings

        sample_listings = [
            {
                "name": "Cozy Apartment Downtown",
                "description": "A nice and cozy apartment in the city center.",
                "location": "New York",
                "pricepernight": 120.00,
            },
            {
                "name": "Beachside Bungalow",
                "description": "Enjoy the ocean breeze in this beachside bungalow.",
                "location": "Miami",
                "pricepernight": 200.00,
            },
            {
                "name": "Mountain Cabin Retreat",
                "description": "Secluded cabin with beautiful mountain views.",
                "location": "Denver",
                "pricepernight": 150.00,
            },
        ]

        for listing in sample_listings:
            Listing.objects.create(
                property_id=uuid.uuid4(),
                host=host,
                name=listing['name'],
                description=listing['description'],
                location=listing['location'],
                pricepernight=listing['pricepernight']
            )

        self.stdout.write(self.style.SUCCESS('Sample listings seeded successfully.'))
