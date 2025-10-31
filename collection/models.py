from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

class Case(models.Model):
    """Hot Wheels Case Mix (A-Q, excluding I and O)"""
    CASE_CHOICES = [
        ('A', 'Case A'), ('B', 'Case B'), ('C', 'Case C'), ('D', 'Case D'),
        ('E', 'Case E'), ('F', 'Case F'), ('G', 'Case G'), ('H', 'Case H'),
        ('J', 'Case J'), ('K', 'Case K'), ('L', 'Case L'), ('M', 'Case M'),
        ('N', 'Case N'), ('P', 'Case P'), ('Q', 'Case Q'),
    ]
    
    name = models.CharField(max_length=1, choices=CASE_CHOICES, unique=True)
    year = models.IntegerField(default=2025, validators=[MinValueValidator(2000)])
    description = models.TextField(blank=True)
    release_date = models.DateField(null=True, blank=True)
    total_cars = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['year', 'name']
        verbose_name = "Case Mix"
        verbose_name_plural = "Case Mixes"
    
    def __str__(self):
        return f"{self.year} Case {self.name}"
    
    def get_car_count(self):
        return self.cars.count()

class Series(models.Model):
    """Hot Wheels Series Categories"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    color_theme = models.CharField(max_length=7, default='#ff3d3d', help_text="Hex color code")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Series"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_car_count(self):
        return self.cars.count()

class Car(models.Model):
    """Hot Wheels Die-Cast Model"""
    TREASURE_HUNT_TYPES = [
        ('NONE', 'Regular'),
        ('TH', 'Treasure Hunt'),
        ('STH', 'Super Treasure Hunt'),
        ('CHASE', 'Chase Edition'),
    ]
    
    CONDITION_CHOICES = [
        ('MINT', 'Mint in Package'),
        ('OPENED', 'Opened/Loose'),
        ('DAMAGED', 'Package Damaged'),
    ]
    
    # Basic Information
    casting_name = models.CharField(max_length=200)
    number = models.CharField(max_length=20, help_text="e.g., 1/250, 01/10")
    year = models.IntegerField(default=2025, validators=[MinValueValidator(1968)])
    
    # Relationships
    case = models.ForeignKey(Case, on_delete=models.SET_NULL, null=True, blank=True, related_name='cars')
    series = models.ForeignKey(Series, on_delete=models.SET_NULL, null=True, blank=True, related_name='cars')
    
    # Details
    color = models.CharField(max_length=100)
    treasure_hunt = models.CharField(max_length=10, choices=TREASURE_HUNT_TYPES, default='NONE')
    manufacturer = models.CharField(max_length=100, default='Mattel')
    scale = models.CharField(max_length=20, default='1:64')
    
    # Collection Info
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='MINT')
    purchase_date = models.DateField(null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estimated_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Media
    image = models.ImageField(upload_to='cars/%Y/', blank=True, null=True)
    
    # Additional Info
    notes = models.TextField(blank=True)
    is_favorite = models.BooleanField(default=False)
    is_for_trade = models.BooleanField(default=False)
    
    # Metadata
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Car"
        verbose_name_plural = "Cars"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.year}-{self.casting_name}-{self.color}")
            self.slug = base_slug
            counter = 1
            while Car.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.year} {self.casting_name} - {self.color}"
    
    def is_treasure_hunt(self):
        return self.treasure_hunt != 'NONE'

class CollectorProfile(models.Model):
    """Collector Information"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    bio = models.TextField(blank=True)
    years_collecting = models.IntegerField(default=0)
    favorite_series = models.ForeignKey(Series, on_delete=models.SET_NULL, null=True, blank=True)
    total_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def get_total_cars(self):
        return Car.objects.aggregate(total=models.Sum('quantity'))['total'] or 0
