from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/historique/', views.historique_view, name='historique'),
    path('dashboard/repartition/', views.repartition_view, name='repartition'),
    path('dashboard/<str:module_name>/', views.liste_view, name='liste_module'),

    path('dashboard/<str:module_name>/ajouter/', views.ajouter_donnees, name='ajouter_donnees'),
    path('dashboard/<str:module_name>/<int:pk>/modifier/', views.modifier_donnees, name='modifier_donnees'),
    path('dashboard/<str:module_name>/<int:pk>/supprimer/', views.supprimer_donnees, name='supprimer_donnees'),
]
