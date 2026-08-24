# KidsLearn — MVP enrichi

Application bilingue français/anglais de lecture et d’alphabétisation pour enfants.

## Fonctionnalités ajoutées
- Lecture des histoires en **français ou anglais**.
- **Lecture à voix haute** avec SpeechSynthesis du navigateur.
- Histoires par niveaux et catégories.
- Évaluations de compréhension automatiques.
- **Compétences** affichées sur le tableau de bord.
- **Badges** : première histoire, 5 activités, score parfait.
- **Mini-jeu de lettres** et espace jeux.
- Tableau de bord parent avec enfants, scores, progression et accès à la bibliothèque.
- Tableau de bord enfant avec progression, compétences, badges et graphique.
- **Espace administrateur** avec statistiques globales et dernières évaluations.
- API JSON `/api/progress/<child_id>` pour connecter plus tard une application mobile.
- Base SQLite.

## Lancer

```bash
python -m venv .venv
# Windows : .venv\Scripts\activate
# macOS/Linux : source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Ouvrir `http://127.0.0.1:5000`.

### Compte administrateur de démonstration
- Email : `admin@kidslearn.local`
- Mot de passe : `Admin123!`

**Important :** ces identifiants sont uniquement pour le prototype. Change-les avant toute mise en production.

## Étape production recommandée
- PostgreSQL
- vraie gestion des sessions/CSRF
- confirmation e-mail et récupération de mot de passe
- stockage cloud des illustrations/audio
- comptes enfant sécurisés liés au parent
- vrai moteur de recommandations pédagogiques
- analytics détaillés par compétence
- application mobile ou PWA
- synthèse vocale native/voix enfant selon disponibilité

## Accès administrateur (prototype local)

Le compte administrateur est créé automatiquement au démarrage si absent.

- E-mail : `admin@kidslearn.local`
- Mot de passe : `Admin123!`
- Dashboard : `/admin`

Pour une utilisation en production, changez immédiatement ce mot de passe et ne conservez pas ces identifiants par défaut.
