from django import forms
from .models import (
    Utilisateur,
    Professeur,
    Tuteur,
    ParentEleve,
    AnneeScolaire,
    Ecole,
    OptionScolaire,
    Classe,
    Eleve,
    Inscription,
    Matiere,
    Horaire,
    Note,
    Presence,
    Discipline,
    FraisScolaire,
    Paiement,
    Notification,
    Evenement,
)

class EcoleForm(forms.ModelForm):
    class Meta:
        model = Ecole
        fields = '__all__'

class ClasseForm(forms.ModelForm):
    class Meta:
        model = Classe
        fields = '__all__'

class EleveForm(forms.ModelForm):
    class Meta:
        model = Eleve
        fields = '__all__'
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = '__all__'

class HoraireForm(forms.ModelForm):
    class Meta:
        model = Horaire
        fields = '__all__'
        widgets = {
            'heure_debut': forms.TimeInput(attrs={'type': 'time'}),
            'heure_fin': forms.TimeInput(attrs={'type': 'time'}),
        }

class FraisScolaireForm(forms.ModelForm):
    class Meta:
        model = FraisScolaire
        fields = '__all__'

class ProfesseurForm(forms.ModelForm):
    class Meta:
        model = Professeur
        fields = '__all__'

class TuteurForm(forms.ModelForm):
    class Meta:
        model = Tuteur
        fields = '__all__'

class ParentEleveForm(forms.ModelForm):
    class Meta:
        model = ParentEleve
        fields = '__all__'

class AnneeScolaireForm(forms.ModelForm):
    class Meta:
        model = AnneeScolaire
        fields = '__all__'

class OptionScolaireForm(forms.ModelForm):
    class Meta:
        model = OptionScolaire
        fields = '__all__'

class MatiereForm(forms.ModelForm):
    class Meta:
        model = Matiere
        fields = '__all__'

class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = '__all__'

class PresenceForm(forms.ModelForm):
    class Meta:
        model = Presence
        fields = '__all__'

class DisciplineForm(forms.ModelForm):
    class Meta:
        model = Discipline
        fields = '__all__'

class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = '__all__'

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = '__all__'

class EvenementForm(forms.ModelForm):
    class Meta:
        model = Evenement
        fields = '__all__'