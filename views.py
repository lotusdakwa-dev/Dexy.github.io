from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum
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
from .forms import (
    EcoleForm,
    ClasseForm,
    EleveForm,
    NoteForm,
    HoraireForm,
    FraisScolaireForm,
    ProfesseurForm,
    TuteurForm,
    ParentEleveForm,
    AnneeScolaireForm,
    OptionScolaireForm,
    MatiereForm,
    InscriptionForm,
    PresenceForm,
    DisciplineForm,
    PaiementForm,
    NotificationForm,
    EvenementForm,
)

MODULES_CONFIG = {
    'utilisateurs': {
        'model': Utilisateur,
        'form': None,
        'redirect': 'liste_module',
        'titre': 'un utilisateur',
        'label': 'Utilisateurs',
        'columns': [
            {'label': 'Utilisateur', 'attr': 'username'},
            {'label': 'Nom', 'attr': 'last_name'},
            {'label': 'Prénom', 'attr': 'first_name'},
            {'label': 'Rôle', 'attr': 'role'},
        ],
    },
    'professeurs': {
        'model': Professeur,
        'form': ProfesseurForm,
        'redirect': 'liste_module',
        'titre': 'un professeur',
        'label': 'Professeurs',
        'columns': [
            {'label': 'Professeur', 'attr': 'user'},
            {'label': 'Matricule', 'attr': 'matricule_prof'},
            {'label': 'Grade', 'attr': 'grade'},
        ],
    },
    'tuteurs': {
        'model': Tuteur,
        'form': TuteurForm,
        'redirect': 'liste_module',
        'titre': 'un tuteur',
        'label': 'Tuteurs',
        'columns': [
            {'label': 'Tuteur', 'attr': 'user'},
            {'label': 'Profession', 'attr': 'profession'},
            {'label': 'Adresse', 'attr': 'adresse_domicile'},
        ],
    },
    'parenteleves': {
        'model': ParentEleve,
        'form': ParentEleveForm,
        'redirect': 'liste_module',
        'titre': 'un lien parent-élève',
        'label': 'Parents/Élèves',
        'columns': [
            {'label': 'Tuteur', 'attr': 'tuteur'},
            {'label': 'Élève', 'attr': 'eleve'},
            {'label': 'Lien', 'attr': 'lien_parente'},
        ],
    },
    'annees': {
        'model': AnneeScolaire,
        'form': AnneeScolaireForm,
        'redirect': 'liste_module',
        'titre': 'une année scolaire',
        'label': 'Années scolaires',
        'columns': [
            {'label': 'Année', 'attr': 'libelle'},
            {'label': 'Active', 'attr': 'est_active'},
        ],
    },
    'options': {
        'model': OptionScolaire,
        'form': OptionScolaireForm,
        'redirect': 'liste_module',
        'titre': 'une option scolaire',
        'label': 'Options scolaires',
        'columns': [
            {'label': 'Option', 'attr': 'nom_option'},
            {'label': 'École', 'attr': 'ecole'},
        ],
    },
    'matieres': {
        'model': Matiere,
        'form': MatiereForm,
        'redirect': 'liste_module',
        'titre': 'une matière',
        'label': 'Matières',
        'columns': [
            {'label': 'Matière', 'attr': 'libelle'},
            {'label': 'Code', 'attr': 'code_matiere'},
        ],
    },
    'inscriptions': {
        'model': Inscription,
        'form': InscriptionForm,
        'redirect': 'liste_module',
        'titre': 'une inscription',
        'label': 'Inscriptions',
        'columns': [
            {'label': 'Élève', 'attr': 'eleve'},
            {'label': 'Classe', 'attr': 'classe'},
            {'label': 'Année', 'attr': 'annee_scolaire'},
            {'label': 'Statut', 'attr': 'statut_inscription'},
        ],
    },
    'presences': {
        'model': Presence,
        'form': PresenceForm,
        'redirect': 'liste_module',
        'titre': 'une présence',
        'label': 'Présences',
        'columns': [
            {'label': 'Élève', 'attr': 'inscription.eleve'},
            {'label': 'Horaire', 'attr': 'horaire'},
            {'label': 'Date', 'attr': 'date_jour'},
            {'label': 'Statut', 'attr': 'statut_presence'},
        ],
    },
    'disciplines': {
        'model': Discipline,
        'form': DisciplineForm,
        'redirect': 'liste_module',
        'titre': 'une discipline',
        'label': 'Disciplines',
        'columns': [
            {'label': 'Élève', 'attr': 'inscription.eleve'},
            {'label': 'Faute', 'attr': 'faute'},
            {'label': 'Sanction', 'attr': 'sanction'},
            {'label': 'Date', 'attr': 'date_incident'},
        ],
    },
    'paiements': {
        'model': Paiement,
        'form': PaiementForm,
        'redirect': 'liste_module',
        'titre': 'un paiement',
        'label': 'Paiements',
        'columns': [
            {'label': 'Référence', 'attr': 'reference_transaction'},
            {'label': 'Montant', 'attr': 'montant_paye'},
            {'label': 'Statut', 'attr': 'statut'},
            {'label': 'Mode', 'attr': 'mode_paiement'},
        ],
    },
    'notifications': {
        'model': Notification,
        'form': NotificationForm,
        'redirect': 'liste_module',
        'titre': 'une notification',
        'label': 'Notifications',
        'columns': [
            {'label': 'Destinataire', 'attr': 'user_destinataire'},
            {'label': 'Titre', 'attr': 'titre'},
            {'label': 'Canal', 'attr': 'type_canal'},
            {'label': 'Statut', 'attr': 'statut_envoi'},
        ],
    },
    'evenements': {
        'model': Evenement,
        'form': EvenementForm,
        'redirect': 'liste_module',
        'titre': 'un événement',
        'label': 'Événements',
        'columns': [
            {'label': 'Titre', 'attr': 'titre_evenement'},
            {'label': 'Type', 'attr': 'type_evenement'},
            {'label': 'Début', 'attr': 'date_debut'},
            {'label': 'Fin', 'attr': 'date_fin'},
        ],
    },
    'ecoles': {
        'model': Ecole,
        'form': EcoleForm,
        'redirect': 'liste_module',
        'titre': 'une école',
        'label': 'Écoles',
        'columns': [
            {'label': 'Nom', 'attr': 'nom_ecole'},
            {'label': 'Code national', 'attr': 'code_national'},
            {'label': 'Adresse', 'attr': 'adresse'},
        ],
    },
    'classes': {
        'model': Classe,
        'form': ClasseForm,
        'redirect': 'liste_module',
        'titre': 'une classe',
        'label': 'Classes',
        'columns': [
            {'label': 'Classe', 'attr': 'nom_classe'},
            {'label': 'Option', 'attr': 'option_scolaire'},
        ],
    },
    'eleves': {
        'model': Eleve,
        'form': EleveForm,
        'redirect': 'liste_module',
        'titre': 'un élève',
        'label': 'Élèves',
        'columns': [
            {'label': 'Matricule', 'attr': 'matricule'},
            {'label': 'Nom complet', 'attr': 'nom'},
            {'label': 'Genre', 'attr': 'genre'},
        ],
    },
    'notes': {
        'model': Note,
        'form': NoteForm,
        'redirect': 'liste_module',
        'titre': 'une note',
        'label': 'Notes',
        'columns': [
            {'label': 'Élève', 'attr': 'inscription.eleve'},
            {'label': 'Matière', 'attr': 'matiere'},
            {'label': 'Note', 'attr': 'note_obtenue'},
            {'label': 'Période', 'attr': 'periode'},
        ],
    },
    'horaires': {
        'model': Horaire,
        'form': HoraireForm,
        'redirect': 'liste_module',
        'titre': 'un horaire',
        'label': 'Horaires',
        'columns': [
            {'label': 'Jour', 'attr': 'jour_semaine'},
            {'label': 'Classe', 'attr': 'classe'},
            {'label': 'Matière', 'attr': 'matiere'},
            {'label': 'Heure', 'attr': 'heure_debut'},
        ],
    },
    'frais': {
        'model': FraisScolaire,
        'form': FraisScolaireForm,
        'redirect': 'liste_module',
        'titre': 'un frais scolaire',
        'label': 'Frais',
        'columns': [
            {'label': 'Libellé', 'attr': 'libelle_frais'},
            {'label': 'Classe', 'attr': 'classe'},
            {'label': 'Montant', 'attr': 'montant_total'},
            {'label': 'Devise', 'attr': 'devise'},
        ],
    },
}

def build_dashboard_context():
    stats = {
        config['label']: config['model'].objects.count()
        for config in MODULES_CONFIG.values()
    }
    total_records = sum(stats.values())
    icons = {
        'Utilisateurs': '👥',
        'Professeurs': '👨‍🏫',
        'Tuteurs': '🧑‍🤝‍🧑',
        'Parents/Élèves': '👪',
        'Années scolaires': '📘',
        'Options scolaires': '🎓',
        'Matières': '📚',
        'Inscriptions': '📝',
        'Présences': '✅',
        'Disciplines': '⚠️',
        'Paiements': '💳',
        'Notifications': '🔔',
        'Événements': '📅',
        'Écoles': '🏫',
        'Classes': '🏷️',
        'Élèves': '👩‍🎓',
        'Notes': '🧾',
        'Horaires': '⏰',
        'Frais': '💰',
    }
    accents = {
        'Utilisateurs': 'accent-purple',
        'Professeurs': 'accent-blue',
        'Tuteurs': 'accent-cyan',
        'Parents/Élèves': 'accent-pink',
        'Années scolaires': 'accent-green',
        'Options scolaires': 'accent-orange',
        'Matières': 'accent-blue',
        'Inscriptions': 'accent-purple',
        'Présences': 'accent-cyan',
        'Disciplines': 'accent-orange',
        'Paiements': 'accent-pink',
        'Notifications': 'accent-green',
        'Événements': 'accent-blue',
        'Écoles': 'accent-green',
        'Classes': 'accent-blue',
        'Élèves': 'accent-purple',
        'Notes': 'accent-orange',
        'Horaires': 'accent-cyan',
        'Frais': 'accent-pink',
    }
    modules = []
    for key, config in MODULES_CONFIG.items():
        count = config['model'].objects.count()
        modules.append({
            'module_name': key,
            'label': config['label'],
            'route': 'liste_module',
            'count': count,
            'icon': icons.get(config['label'], '🔎'),
            'accent': accents.get(config['label'], 'accent-green'),
        })

    max_stat = max(stats.values()) if stats else 1
    max_module = max((module['count'] for module in modules), default=1)
    for module in modules:
        module['percent'] = int(module['count'] * 100 / max_module) if max_module else 0

    trend_data = sorted(
        [
            {
                'label': label,
                'count': count,
                'percent': int(count * 100 / max_stat) if max_stat else 0,
            }
            for label, count in stats.items()
        ],
        key=lambda item: item['count'],
        reverse=True,
    )[:6]

    return {
        'stats': stats,
        'total_records': total_records,
        'modules': modules,
        'trend_data': trend_data,
    }


@login_required
def dashboard_view(request):
    context = build_dashboard_context()
    eleves_par_genre = {
        'Masculin': Eleve.objects.filter(genre='M').count(),
        'Féminin': Eleve.objects.filter(genre='F').count(),
    }
    inscriptions_by_classe = Inscription.objects.values('classe__nom_classe').annotate(total=Count('id')).order_by('-total')[:5]
    frais_by_annee = FraisScolaire.objects.values('annee_scolaire__libelle').annotate(total=Sum('montant_total')).order_by('annee_scolaire__libelle')
    context.update({
        'eleves_par_genre': eleves_par_genre,
        'inscriptions_by_classe': inscriptions_by_classe,
        'frais_by_annee': frais_by_annee,
    })
    return render(request, 'dashboard.html', context)


@login_required
def historique_view(request):
    context = build_dashboard_context()
    return render(request, 'historique.html', context)


@login_required
def repartition_view(request):
    context = build_dashboard_context()
    return render(request, 'repartition.html', context)


def resolve_attr(instance, path):
    value = instance
    for part in path.split('.'):
        value = getattr(value, part, '')
        if callable(value):
            value = value()
        if value is None:
            return ''
    return value


@login_required
def liste_view(request, module_name):
    config = MODULES_CONFIG.get(module_name)
    if not config:
        return redirect('dashboard')

    queryset = config['model'].objects.all()
    headers = [column['label'] for column in config['columns']]
    rows = []
    for item in queryset:
        rows.append({
            'pk': item.pk,
            'values': [resolve_attr(item, column['attr']) for column in config['columns']],
        })

    return render(request, 'liste_generique.html', {
        'module': config,
        'module_name': module_name,
        'headers': headers,
        'rows': rows,
    })

@login_required
def ajouter_donnees(request, module_name):
    config = MODULES_CONFIG.get(module_name)
    if not config:
        return redirect('dashboard')

    form_class = config.get('form')
    if not form_class:
        messages.error(request, 'Ce module ne prend pas en charge la création de données via l’interface.')
        return redirect('dashboard')

    form = form_class(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'{config["label"]} enregistré avec succès.')
        return redirect(config['redirect'], module_name=module_name)

    return render(request, 'ajouter_form.html', {
        'form': form,
        'titre': f'Ajouter {config["titre"]}',
        'redirect_url': config['redirect'],
        'module_name': module_name,
    })

@login_required
def modifier_donnees(request, module_name, pk):
    config = MODULES_CONFIG.get(module_name)
    if not config:
        return redirect('dashboard')

    instance = get_object_or_404(config['model'], pk=pk)
    form_class = config.get('form')
    if not form_class:
        messages.error(request, 'Ce module ne prend pas en charge la modification via l’interface.')
        return redirect('dashboard')

    form = form_class(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'{config["label"]} mis à jour avec succès.')
        return redirect(config['redirect'], module_name=module_name)

    return render(request, 'ajouter_form.html', {
        'form': form,
        'titre': f'Modifier {config["titre"]}',
        'redirect_url': config['redirect'],
        'module_name': module_name,
    })

@login_required
def supprimer_donnees(request, module_name, pk):
    config = MODULES_CONFIG.get(module_name)
    if not config:
        return redirect('dashboard')

    instance = get_object_or_404(config['model'], pk=pk)
    if request.method == 'POST':
        instance.delete()
        messages.success(request, f'{config["label"]} supprimé avec succès.')
        return redirect(config['redirect'], module_name=module_name)

    return render(request, 'confirm_delete.html', {
        'object': instance,
        'redirect_url': config['redirect'],
        'module_name': module_name,
    })
