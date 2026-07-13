from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from decimal import Decimal

# ==========================================
# MODULE 1 : AUTHENTIFICATION & PROFILS
# ==========================================

class Utilisateur(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrateur'),
        ('DIRECTEUR', 'Directeur des Études'),
        ('PROFESSEUR', 'Professeur'),
        ('PARENT', 'Parent/Tuteur'),
    ]
    
    telephone = models.CharField(max_length=20, unique=True, verbose_name="Numéro de Téléphone")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='PARENT')
    
    REQUIRED_FIELDS = ['telephone', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.last_name.upper()} {self.first_name} ({self.get_role_display()})"


class Professeur(models.Model):
    user = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='profil_professeur')
    matricule_prof = models.CharField(max_length=50, unique=True)
    grade = models.CharField(max_length=100, help_text="Ex: Licencié, Gradué, Docteur")

    def __str__(self):
        return f"Prof. {self.user.last_name}"


class Tuteur(models.Model):
    user = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='profil_tuteur')
    profession = models.CharField(max_length=100, blank=True, null=True)
    adresse_domicile = models.TextField()
    enfants = models.ManyToManyField('Eleve', through='ParentEleve', related_name='tuteurs')

    def __str__(self):
        return f"Tuteur: {self.user.last_name} {self.user.first_name}"


class ParentEleve(models.Model):
    LIEN_CHOICES = [
        ('PERE', 'Père'),
        ('MERE', 'Mère'),
        ('TUTEUR_LEGAL', 'Tuteur Légal'),
        ('ONCLE_TANTE', 'Oncle / Tante'),
    ]
    tuteur = models.ForeignKey(Tuteur, on_delete=models.CASCADE)
    eleve = models.ForeignKey('Eleve', on_delete=models.CASCADE)
    lien_parente = models.CharField(max_length=20, choices=LIEN_CHOICES, default='TUTEUR_LEGAL')

    class Meta:
        unique_together = ('tuteur', 'eleve')


# ==========================================
# MODULE 2 : STRUCTURE SCOLAIRE & INSCRIPTIONS
# ==========================================

class AnneeScolaire(models.Model):
    libelle = models.CharField(max_length=20, unique=True, help_text="Ex: 2025-2026")
    est_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.est_active:
            AnneeScolaire.objects.filter(est_active=True).update(est_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Année Scolaire {self.libelle}"


class Ecole(models.Model):
    nom_ecole = models.CharField(max_length=255)
    code_national = models.CharField(max_length=100, unique=True)
    adresse = models.TextField()

    def __str__(self):
        return self.nom_ecole


class OptionScolaire(models.Model):
    nom_option = models.CharField(max_length=100, help_text="Ex: Commerciale & Gestion")
    ecole = models.ForeignKey(Ecole, on_delete=models.CASCADE, related_name='options')

    def __str__(self):
        return f"{self.nom_option} - {self.ecole.nom_ecole}"


class Classe(models.Model):
    nom_classe = models.CharField(max_length=50, help_text="Ex: 5ème Humanités")
    option_scolaire = models.ForeignKey(OptionScolaire, on_delete=models.CASCADE, related_name='classes')

    def __str__(self):
        return f"{self.nom_classe} ({self.option_scolaire.nom_option})"


class Eleve(models.Model):
    GENRE_CHOICES = [('M', 'Masculin'), ('F', 'Féminin')]
    
    matricule = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100)
    postnom = models.CharField(max_length=100, blank=True, null=True)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES)

    def __str__(self):
        return f"{self.nom.upper()} {self.postnom or ''} {self.prenom}"


class Inscription(models.Model):
    STATUT_CHOICES = [('ACTIF', 'Actif'), ('ABANDON', 'Abandon'), ('TRANSFERE', 'Transféré')]
    
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE, related_name='inscriptions')
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='inscriptions')
    annee_scolaire = models.ForeignKey(AnneeScolaire, on_delete=models.CASCADE)
    date_inscription = models.DateField(auto_now_add=True)
    statut_inscription = models.CharField(max_length=20, choices=STATUT_CHOICES, default='ACTIF')
    frais_inscription_paye = models.BooleanField(default=False)

    class Meta:
        unique_together = ('eleve', 'annee_scolaire')

    def __str__(self):
        return f"{self.eleve} en {self.classe} ({self.annee_scolaire.libelle})"

    def obtenir_bulletin_par_periode(self, periode):
        """Calcule le bulletin de l'élève pour le tuteur."""
        notes_periode = self.notes.filter(periode=periode)
        total_obtenu = sum(note.note_obtenue for note in notes_periode)
        total_maximum = sum(note.points_max for note in notes_periode)
        pourcentage = (total_obtenu / total_maximum) * 100 if total_maximum > 0 else 0
        
        return {
            'notes': notes_periode,
            'total_obtenu': total_obtenu,
            'total_maximum': total_maximum,
            'pourcentage': round(pourcentage, 2)
        }


# ==========================================
# MODULE 3 : PÉDAGOGIE & EMPLOI DU TEMPS
# ==========================================

class Matiere(models.Model):
    libelle = models.CharField(max_length=150)
    code_matiere = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.libelle


class Horaire(models.Model):
    JOUR_CHOICES = [
        ('LUNDI', 'Lundi'), ('MARDI', 'Mardi'), ('MERCREDI', 'Mercredi'),
        ('JEUDI', 'Jeudi'), ('VENDREDI', 'Vendredi'), ('SAMEDI', 'Samedi')
    ]
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='horaires')
    professeur = models.ForeignKey(Professeur, on_delete=models.CASCADE, related_name='horaires')
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    jour_semaine = models.CharField(max_length=15, choices=JOUR_CHOICES)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    annee_scolaire = models.ForeignKey(AnneeScolaire, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.jour_semaine} | {self.classe} - {self.matiere.libelle}"


# ==========================================
# MODULE 4 : ÉVALUATIONS, PRÉSENCES & DISCIPLINE
# ==========================================

class Note(models.Model):
    PERIODE_CHOICES = [
        ('P1', '1ère Période'), ('P2', '2ème Période'), ('EXAM_S1', 'Examen Semestre 1'),
        ('P3', '3ème Période'), ('P4', '4ème Période'), ('EXAM_S2', 'Examen Semestre 2'),
    ]
    inscription = models.ForeignKey(Inscription, on_delete=models.CASCADE, related_name='notes')
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    periode = models.CharField(max_length=10, choices=PERIODE_CHOICES)
    note_obtenue = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    points_max = models.IntegerField(default=20)

    def __str__(self):
        return f"{self.inscription.eleve} - {self.matiere} ({self.periode})"


class Presence(models.Model):
    STATUT_PRESENCE = [('PRESENT', 'Présent'), ('ABSENT', 'Absent'), ('RETARD', 'En Retard'), ('JUSTIFIE', 'Justifié')]
    
    inscription = models.ForeignKey(Inscription, on_delete=models.CASCADE, related_name='presences')
    horaire = models.ForeignKey(Horaire, on_delete=models.CASCADE)
    date_jour = models.DateField()
    statut_presence = models.CharField(max_length=15, choices=STATUT_PRESENCE, default='PRESENT')
    commentaire = models.TextField(blank=True, null=True)


class Discipline(models.Model):
    inscription = models.ForeignKey(Inscription, on_delete=models.CASCADE, related_name='incidents_disciplinaires')
    faute = models.CharField(max_length=255)
    sanction = models.CharField(max_length=255, blank=True, null=True)
    date_incident = models.DateField()


# ==========================================
# MODULE 5 : FINANCES & PAIEMENTS
# ==========================================

class FraisScolaire(models.Model):
    DEVISE_CHOICES = [('USD', 'USD'), ('CDF', 'CDF')]
    
    libelle_frais = models.CharField(max_length=150)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    devise = models.CharField(max_length=3, choices=DEVISE_CHOICES, default='USD')
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='frais')
    annee_scolaire = models.ForeignKey(AnneeScolaire, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.libelle_frais} ({self.montant_total} {self.devise})"


class Paiement(models.Model):
    MODE_PAIEMENT = [('MPESA', 'M-Pesa'), ('ORANGE', 'Orange Money'), ('AIRTEL', 'Airtel Money'), ('CASH', 'Cash'), ('BANQUE', 'Banque')]
    STATUT_PAIEMENT = [('PENDING', 'En Attente'), ('SUCCESS', 'Succès'), ('FAILED', 'Échoué')]
    
    reference_transaction = models.CharField(max_length=100, unique=True)
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateTimeField(auto_now_add=True)
    mode_paiement = models.CharField(max_length=15, choices=MODE_PAIEMENT)
    statut = models.CharField(max_length=15, choices=STATUT_PAIEMENT, default='PENDING')
    inscription = models.ForeignKey(Inscription, on_delete=models.CASCADE, related_name='paiements')
    frais_scolaire = models.ForeignKey(FraisScolaire, on_delete=models.CASCADE)


# ==========================================
# MODULE 6 : COMMUNICATION & ÉVÉNEMENTS
# ==========================================

class Notification(models.Model):
    CANAL_CHOICES = [('SMS', 'SMS'), ('IN_APP', 'In-App'), ('EMAIL', 'Email')]
    STATUT_ENVOI = [('EN_ATTENTE', 'En Attente'), ('ENVOYE', 'Envoyé'), ('ECHEC', 'Échoué')]
    
    user_destinataire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='notifications')
    titre = models.CharField(max_length=150)
    message = models.TextField()
    type_canal = models.CharField(max_length=10, choices=CANAL_CHOICES, default='IN_APP')
    statut_envoi = models.CharField(max_length=15, choices=STATUT_ENVOI, default='EN_ATTENTE')
    date_creation = models.DateTimeField(auto_now_add=True)


class Evenement(models.Model):
    TYPE_CHOICES = [('SCOLAIRE', 'Scolaire'), ('HORS_SCOLAIRE', 'Hors-Scolaire')]
    
    ecole = models.ForeignKey(Ecole, on_delete=models.CASCADE, related_name='evenements')
    titre_evenement = models.CharField(max_length=200)
    description = models.TextField()
    type_evenement = models.CharField(max_length=20, choices=TYPE_CHOICES, default='SCOLAIRE')
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    lieu = models.CharField(max_length=200, default="À l'école")