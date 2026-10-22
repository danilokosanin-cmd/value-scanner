# VALUE SCANNER v0.2 — prototype de simulation

## iPhone
Décompresser l'archive dans l'app Fichiers, puis ouvrir `index.html` dans Safari (si l'ouverture locale ne fonctionne pas selon la version iOS, héberger ce fichier sur un service de pages statiques). Cliquer sur « Charger la démonstration ». Les événements sont fictifs.

Importer ensuite un CSV avec les colonnes `sport,event,market,selection,odds,model_probability,uncertainty` (probabilités et incertitudes en décimales). Ne pas utiliser les probabilités fictives pour miser.

## Python (facultatif)
`python3 scanner.py example.csv`

## Limites majeures
- Aucune connexion Winamax, aucun calendrier ni cote en direct.
- Aucun modèle prédictif entraîné, aucune estimation de probabilité produite automatiquement.
- Le score prudent n'est **pas** un intervalle de confiance validé.
- Pas de pari automatisé, aucune garantie de gain.
- Étape suivante : obtenir une source de données sous licence, des historiques horodatés, entraîner un premier modèle, valider hors échantillon, puis connecter les cotes du bookmaker si l'accès est autorisé.
