# 🏫 Solution Globale de Gestion Scolaire (School ERP) - Django

Un système d'information et de gestion scolaire (ERP) robuste et modulaire, conçu spécifiquement pour s'adapter au cadre institutionnel, administratif et monétaire de la République Démocratique du Congo (RDC). 

Développé avec Django, ce projet offre une architecture backend structurée pour centraliser l'ensemble du flux opérationnel d'un établissement d'enseignement (du primaire au secondaire).

---

## 🚀 Architecture Modulaire & Fonctionnalités

Le système s'articule autour de **6 modules applicatifs** interconnectés :

### 1. 👥 Authentification & Profils
*   **Utilisateur Personnalisé (`AbstractUser`)** : Contrôle d'accès basé sur les rôles (Administrateurs, Directeurs des Études, Professeurs, Parents/Tuteurs).
*   **Profils Dédiés** :
    *   **Enseignants** : Suivi des qualifications académiques conformes aux grades de l'ESU en RDC (*Gradué, Licencié, Docteur*).
    *   **Parents/Tuteurs** : Gestion des liens de parenté multiples (*Père, Mère, Tuteur légal, Oncle/Tante*) pour un suivi familial unifié.

### 2. 🏫 Structure Scolaire & Inscriptions
*   **Modélisation Éducative** : Gestion des options de l'enseignement secondaire congolais (*ex: Commerciale & Gestion, Chimie-Biologie*) et des classes associées (*ex: 5ème Humanités*).
*   **Inscriptions & Cycles** : Suivi des inscriptions uniques par année scolaire active.
*   **Moteur de Calcul Pédagogique** : Algorithme interne de calcul automatique des bulletins scolaires (totaux de points, maxima et pourcentages de réussite) par élève et par période.

### 3. 📅 Pédagogie & Emploi du Temps
*   **Référentiel des Matières** : Gestion centralisée des cours et des codes d'identification uniques.
*   **Planification Horaire** : Génération d'emplois du temps hebdomadaires croisant les enseignants, les classes, les matières et les plages horaires disponibles.

### 4. 📝 Évaluations, Présences & Discipline
*   **Évaluation Continue** : Saisie des notes structurée par période (P1, P2, P3, P4) et examens semestriels (S1, S2).
*   **Gestion des Présences** : Registre d'appel journalier par cours avec statuts configurables (*Présent, Absent, Retard, Justifié*).
*   **Régulation Disciplinaire** : Suivi des incidents scolaires, des infractions aux règlements intérieurs et des sanctions prononcées.

### 5. 💳 Finances & Paiements
*   **Frais Scolaires Multi-Devises** : Paramétrage des frais scolaires par classe et par année académique en **USD** (Dollar Américain) et **CDF** (Franc Congolais).
*   **Passerelles de Paiement Mobile Money** : Structure modélisée pour l'intégration d'API financières locales (**M-Pesa**, **Orange Money**, **Airtel Money**), ainsi que les virements bancaires et règlements en espèces (Cash).

### 6. ✉️ Communication & Événements
*   **Système de Notification Multi-Canal** : Dispatching d'alertes administratives, financières ou académiques par **SMS**, **Email** et notifications **In-App**.
*   **Calendrier Institutionnel** : Planification et diffusion des événements académiques et extrascolaires.

---

## 🛠️ Stack Technique

*   **Framework Principal** : Django 5.x (Python)
*   **Base de Données** : PostgreSQL (Production) / SQLite (Développement)
*   **Validation de Données** : `django.core.validators` (gestion stricte des notes et flux financiers)

---

## ⚙️ Procédure d'Installation & Déploiement

1. **Cloner le projet** :
   ```bash
   git clone [https://github.com/lotusdakwa-dev/Dexy.github.io.git](https://github.com/lotusdakwa-dev/Dexy.github.io.git)
   cd Dexy.github.io
