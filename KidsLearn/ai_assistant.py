"""Mini-assistant KidsLearn, 100% hors connexion.
Elle guide l'enfant pour choisir son niveau et donner son avis sur KidsLearn.
"""

def assistant_message(level, liked, lang="fr"):
    if lang == "en":
        if not level:
            return "Hi! Which age level are you in?"
        if liked is None:
            return "Do you like KidsLearn?"
        return {"yes":"Awesome! Keep learning and playing! 🌟", "some":"Thanks! We can make KidsLearn even better! 💡", "no":"Thanks for telling us. We'll keep improving! 🚀"}.get(liked, "Thanks for your feedback!")
    if not level:
        return "Coucou ! Quel est ton niveau d'âge ?"
    if liked is None:
        return "Est-ce que tu apprécies KidsLearn ?"
    return {"yes":"Super ! Continue à apprendre et à jouer ! 🌟", "some":"Merci ! Nous pouvons rendre KidsLearn encore meilleur ! 💡", "no":"Merci pour ton avis. Nous allons continuer à améliorer KidsLearn ! 🚀"}.get(liked, "Merci pour ton avis !")
