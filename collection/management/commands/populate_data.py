from django.core.management.base import BaseCommand
from collection.models import Case, Series, CollectorProfile

class Command(BaseCommand):
    help = 'Populate database with Hot Wheels cases and series'

    def handle(self, *args, **kwargs):
        # Create Cases
        cases_data = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q']
        for case_name in cases_
            Case.objects.get_or_create(
                name=case_name,
                defaults={'year': 2025, 'description': f'2025 Hot Wheels Mainline Case {case_name} assortment'}
            )
        
        # Create Series
        series_data = [
            ('HW J-Imports', 'Japanese imports including Skylines, Civics, Supras', '#ff3d3d'),
            ('HW First Response', 'Emergency vehicles, police cars, fire trucks', '#3d3dff'),
            ('Factory Fresh', 'Brand new castings and modern vehicle designs', '#ffef00'),
            ('Rod Squad', 'Classic hot rods, street rods, custom muscle cars', '#ff6b6b'),
            ('HW Hot Trucks', 'Pickup trucks, monster trucks, utility vehicles', '#4ecdc4'),
            ('HW Screen Time', 'Movie and TV show vehicles, Batman, Fast & Furious', '#9b59b6'),
            ('HW Art Cars', 'Artistic liveries and special paint designs', '#f39c12'),
            ('HW Dream Garage', 'Exotic supercars, luxury vehicles, dream machines', '#e74c3c'),
            ('X-Raycers', 'Transparent body panels showing internal mechanics', '#1abc9c'),
            ('HW Ride-Ons', 'Motorcycles, scooters, two-wheeled vehicles', '#34495e'),
            ('HW Metro', 'City vehicles, delivery vans, urban transport', '#95a5a6'),
            ('HW Dirt', 'Off-road vehicles, rally cars, dirt bikes, 4x4s', '#d35400'),
            ('HW 70s vs 90s', 'Classic vehicles from the 1970s and 1990s', '#8e44ad'),
            ('HW EV', 'Electric vehicles and future mobility', '#27ae60'),
        ]
        
        for name, desc, color in series_
            Series.objects.get_or_create(
                name=name,
                defaults={'description': desc, 'color_theme': color}
            )
        
        # Create Collector Profile
        CollectorProfile.objects.get_or_create(
            email='collector@hotwheels.com',
            defaults={
                'name': 'Jake Mitchell',
                'bio': 'Passionate Hot Wheels collector for 30 years',
                'years_collecting': 30
            }
        )
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database!'))
