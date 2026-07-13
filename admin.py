from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Utilisateur, Professeur, Tuteur, ParentEleve, AnneeScolaire,
    Ecole, OptionScolaire, Classe, Eleve, Inscription,
    Matiere, Horaire, Note, Presence, Discipline, FraisScolaire, Paiement,
    Notification, Evenement
)

# Configuration de l'utilisateur personnalisé dans l'admin
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Informations Spécifiques', {'fields': ('telephone', 'role')}),
    )
    list_display = ['username', 'email', 'telephone', 'role', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_active']

admin.site.register(Utilisateur, CustomUserAdmin)

# Profils connexes
@admin.register(Professeur)
class ProfesseurAdmin(admin.ModelAdmin):
    list_display = ['user', 'matricule_prof', 'grade']
    search_fields = ['user__last_name', 'matricule_prof']

class ParentEleveInline(admin.TabularInline):
    model = ParentEleve
    extra = 1

@admin.register(Tuteur)
class TuteurAdmin(admin.ModelAdmin):
    list_display = ['user', 'profession']
    inlines = [ParentEleveInline]
    search_fields = ['user__last_name']

# Scolarité
@admin.register(AnneeScolaire)
class AnneeScolaireAdmin(admin.ModelAdmin):
    list_display = ['libelle', 'est_active']

@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ['eleve', 'classe', 'annee_scolaire', 'statut_inscription']
    list_filter = ['classe', 'annee_scolaire', 'statut_inscription']
    search_fields = ['eleve__nom', 'eleve__matricule']

@admin.register(Eleve)
class EleveAdmin(admin.ModelAdmin):
    list_display = ['matricule', 'nom', 'postnom', 'prenom', 'genre']
    search_fields = ['nom', 'matricule']

# Administration simplifiée pour le reste des tables
admin.site.register(Ecole)
admin.site.register(OptionScolaire)
admin.site.register(Classe)
admin.site.register(Matiere)
admin.site.register(Horaire)
admin.site.register(Note)
admin.site.register(Presence)
admin.site.register(Discipline)
admin.site.register(FraisScolaire)
admin.site.register(Paiement)
admin.site.register(Notification)
admin.site.register(Evenement)