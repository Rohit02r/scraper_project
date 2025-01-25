from django.urls import path
from scraper import views  # Correct the import to the 'scraper' app


urlpatterns = [
    path('', views.home, name='home'),
    path('scrape/', views.scrape_data, name='scrape_data'),  # Ensure this is defined correctly
  
]
