from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Sum
from .models import Case, Series, Car, CollectorProfile

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'year', 'total_cars_display', 'release_date', 'updated_at')
    list_filter = ('year', 'name')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'total_cars_display')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'year', 'description')
        }),
        ('Details', {
            'fields': ('release_date', 'total_cars_display')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def display_name(self, obj):
        return f"Case {obj.name}"
    display_name.short_description = 'Case'
    
    def total_cars_display(self, obj):
        count = obj.get_car_count()
        return format_html(
            '<span style="background: #ff3d3d; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            count
        )
    total_cars_display.short_description = 'Cars in Collection'

@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_badge', 'car_count_display', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    readonly_fields = ('slug', 'created_at', 'updated_at', 'car_count_display')
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Styling', {
            'fields': ('color_theme', 'is_active')
        }),
        ('Statistics', {
            'fields': ('car_count_display',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def color_badge(self, obj):
        return format_html(
            '<div style="width: 30px; height: 30px; background: {}; border: 2px solid #000; border-radius: 50%;"></div>',
            obj.color_theme
        )
    color_badge.short_description = 'Color'
    
    def car_count_display(self, obj):
        count = obj.get_car_count()
        return format_html(
            '<span style="background: #3d3dff; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{} MODELS</span>',
            count
        )
    car_count_display.short_description = 'Total Models'

class CarImageFilter(admin.SimpleListFilter):
    title = 'has image'
    parameter_name = 'has_image'
    
    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(image='')
        if self.value() == 'no':
            return queryset.filter(image='')

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'casting_name', 'color', 'case', 'series', 'treasure_badge', 'quantity', 'is_favorite', 'condition', 'year')
    list_filter = ('year', 'case', 'series', 'treasure_hunt', 'condition', CarImageFilter, 'is_favorite', 'is_for_trade')
    search_fields = ('casting_name', 'color', 'notes', 'number')
    readonly_fields = ('slug', 'created_at', 'updated_at', 'thumbnail_large')
    list_editable = ('quantity', 'is_favorite')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('casting_name', 'number', 'year', 'color')
        }),
        ('Classification', {
            'fields': ('case', 'series', 'treasure_hunt')
        }),
        ('Details', {
            'fields': ('manufacturer', 'scale', 'condition', 'quantity')
        }),
        ('Financial', {
            'fields': ('purchase_date', 'purchase_price', 'estimated_value'),
            'classes': ('collapse',)
        }),
        ('Media', {
            'fields': ('image', 'thumbnail_large')
        }),
        ('Collection Management', {
            'fields': ('is_favorite', 'is_for_trade', 'notes')
        }),
        ('Metadata', {
            'fields': ('slug', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border: 2px solid #000;" />', obj.image.url)
        return format_html('<div style="width: 50px; height: 50px; background: #ccc; border: 2px solid #000;"></div>')
    thumbnail.short_description = 'Image'
    
    def thumbnail_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 300px; border: 4px solid #000;" />', obj.image.url)
        return 'No image uploaded'
    thumbnail_large.short_description = 'Preview'
    
    def treasure_badge(self, obj):
        if obj.treasure_hunt == 'STH':
            return format_html('<span style="background: #ffef00; color: #000; padding: 2px 8px; border-radius: 3px; font-weight: bold;">STH</span>')
        elif obj.treasure_hunt == 'TH':
            return format_html('<span style="background: #ff3d3d; color: #fff; padding: 2px 8px; border-radius: 3px; font-weight: bold;">TH</span>')
        elif obj.treasure_hunt == 'CHASE':
            return format_html('<span style="background: #3d3dff; color: #fff; padding: 2px 8px; border-radius: 3px; font-weight: bold;">CHASE</span>')
        return '—'
    treasure_badge.short_description = 'TH'

@admin.register(CollectorProfile)
class CollectorProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'years_collecting', 'total_cars_display')
    readonly_fields = ('total_cars_display',)
    
    def total_cars_display(self, obj):
        return obj.get_total_cars()
    total_cars_display.short_description = 'Total Cars'

# Customize admin site
admin.site.site_header = "Hot Wheels Collection Manager"
admin.site.site_title = "Hot Wheels Admin"
admin.site.index_title = "Collection Dashboard"
