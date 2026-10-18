// Généré par construire.py à partir des données Atelier Nova (WONDERBREAD, salariés fictifs) : ne pas éditer à la main.
const DATA = {
 "verdicts": {
  "overview": "Observation terminée. <b>Rapport ventes/produits sur une période</b> revient 790 fois par semaine chez les 60 postes : c'est la première tâche à regarder.",
  "problems": "<b>11 problèmes</b> à valider avec vous. Les 3 premiers pèsent 48 % du temps perdu.",
  "interactions": "Les 2 équipes font <b>les mêmes 11 tâches</b>. C'est l'écran <b>Catalogue</b> qui concentre le plus de temps.",
  "tools": "Tout le travail observé se passe dans Magento, avec <b>326 changements d'écran</b> par jour et par poste.",
  "business": "<b>5 skills</b> récupèrent 49 320 € par an. La première se construit en 1 sem.",
  "piloting": "Rien n'est encore en production. Cet écran prendra le relais une fois la première skill déployée."
 },
 "maxKpi": 3,
 "firm": "DeloAI",
 "client": {
  "name": "Atelier Nova",
  "postes": 60,
  "equipes": 2,
  "abonnement": "Pas encore d'abonnement (projection)"
 },
 "consultant": "Équipe hackathon",
 "studyLabel": "Étude d'efficacité opérationnelle",
 "demoTag": "Simulation ×10 · base mesurée : 6 salariés WONDERBREAD",
 "steps": [
  {
   "n": 1,
   "label": "Installation",
   "date": "lun. 12 oct.",
   "status": "done",
   "sub": "Terminé"
  },
  {
   "n": 2,
   "label": "Observation",
   "date": "13 → 19 oct.",
   "status": "done",
   "sub": "5 jours"
  },
  {
   "n": 3,
   "label": "Analyse par l'IA",
   "date": "fin d'observation",
   "status": "done",
   "sub": "Terminé"
  },
  {
   "n": 4,
   "label": "Restitution & rapport",
   "date": "aujourd'hui",
   "status": "active",
   "sub": "En cours"
  },
  {
   "n": 5,
   "label": "Logiciel sur mesure",
   "date": "à planifier",
   "status": "upcoming",
   "sub": "À venir"
  }
 ],
 "advancementPct": 70,
 "overview": {
  "dayLabel": "Observation terminée · restitution en cours",
  "stats": [
   {
    "label": "Gain annuel récupérable",
    "value": "49 320 €",
    "sub": "en automatisant 5 tâches",
    "accent": "good"
   },
   {
    "label": "Postes observés",
    "value": "60 / 60",
    "sub": "2 équipes de 30 · back-office Magento"
   },
   {
    "label": "Heures de travail observées",
    "value": "54,0 h",
    "sub": "temps actif dans l'outil, sur 5 jours"
   },
   {
    "label": "Workflows identifiés",
    "value": "19",
    "sub": "dont 11 communs à 3 personnes ou plus"
   },
   {
    "label": "Problèmes détectés",
    "value": "11",
    "sub": "8 autres non détaillés (moins de 3 pers.)"
   }
  ],
  "dailyHours": [
   {
    "day": "Mar 13",
    "value": 11.43,
    "known": true
   },
   {
    "day": "Mer 14",
    "value": 13.7,
    "known": true
   },
   {
    "day": "Jeu 15",
    "value": 12.1,
    "known": true
   },
   {
    "day": "Ven 16",
    "value": 15.58,
    "known": true
   },
   {
    "day": "Lun 19",
    "value": 0.99,
    "known": true
   }
  ],
  "teamCoverage": [
   {
    "team": "E-commerce",
    "have": 30,
    "total": 30
   },
   {
    "team": "Opérations",
    "have": 30,
    "total": 30
   }
  ],
  "signals": [
   {
    "tag": "Ressaisie",
    "path": "E-commerce, Opérations",
    "text": "Rapport ventes/produits sur une période",
    "meta": "790 fois / sem. · 6 h 00 / sem.",
    "confidence": "Confiance élevée"
   },
   {
    "tag": "Recherche",
    "path": "E-commerce, Opérations",
    "text": "Consultation des commandes annulées",
    "meta": "520 fois / sem. · 5 h 00 / sem.",
    "confidence": "Confiance élevée"
   },
   {
    "tag": "Ressaisie",
    "path": "E-commerce, Opérations",
    "text": "Modifier le prix d'un produit ou d'une variante",
    "meta": "370 fois / sem. · 5 h 00 / sem.",
    "confidence": "Confiance élevée"
   }
  ],
  "signalsUpdated": "à la fin de l'observation",
  "toRelaunch": [],
  "toRelaunchEmpty": "Aucun : les 60 postes ont validé leur résumé (validation de démo, sans relecture humaine).",
  "compliance": [
   "Simulation : volumes multipliés par 10 à partir de 6 postes réellement observés",
   "Données publiques WONDERBREAD (Stanford, CC-BY-4.0)",
   "Salariés fictifs : prénoms inventés, un annotateur réel différent par poste",
   "Aucune capture ni texte d'écran dans ce portail",
   "Analyse par équipe de 3 personnes minimum",
   "Tâche partagée par moins de 3 personnes : non détaillée",
   "Résumés validés pour la démo, sans relecture humaine"
  ],
  "nextSteps": [
   {
    "date": "Aujourd'hui",
    "text": "Restitution : Wrapped, rapport du cabinet et liste des déclencheurs"
   },
   {
    "date": "Ensuite",
    "text": "Relecture des résumés par chaque salarié, pour de vrai"
   },
   {
    "date": "Puis",
    "text": "Skill n° 1 : « Modifier le prix d'un produit ou d'une variante »"
   }
  ]
 },
 "problemsMeta": {
  "total": 11,
  "hoursPerWeek": "33 h 00",
  "annualCost": 57684,
  "validated": 0,
  "categories": [
   "Tous",
   "Recherche",
   "Ressaisie",
   "Répétition"
  ]
 },
 "problems": [
  {
   "id": 1,
   "cat": "Ressaisie",
   "path": "E-commerce, Opérations",
   "title": "Rapport ventes/produits sur une période",
   "metaBits": [
    "790 fois / sem.",
    "6 h 00 / sem.",
    "Automatisable : partiel"
   ],
   "annualCost": 10488,
   "status": "À valider",
   "detail": {
    "description": "Les paramètres sont connus et répétitifs ; un export planifié ou un appel API éviterait la saisie manuelle, mais la finalité de la lecture n'est pas observée.",
    "lostPerWeek": "6 h 00",
    "confidence": "Élevée",
    "observed": [
     "790 occurrences sur la semaine observée",
     "60 personnes concernées (E-commerce, Opérations)",
     "5 exception(s) relevée(s) : Les périodes varient (trimestre, mois, année, plage très large depuis 2010)",
     "5 façons de la nommer chez les salariés"
    ],
    "sequence": [
     "Ouvrir un rapport",
     "Saisir la date de début et l",
     "Choisir le regroupement pour"
    ],
    "solution": "Skill « Rapport ventes/produits sur une période » : les étapes observées deviennent une automatisation, les décisions restent humaines (score 68/100)."
   }
  },
  {
   "id": 2,
   "cat": "Recherche",
   "path": "E-commerce, Opérations",
   "title": "Consultation des commandes annulées",
   "metaBits": [
    "520 fois / sem.",
    "5 h 00 / sem.",
    "Automatisable : oui"
   ],
   "annualCost": 8740,
   "status": "À valider",
   "detail": {
    "description": "Le filtre et le tri sont toujours identiques ; une vue enregistrée ou un rapport automatique des annulations suffirait.",
    "lostPerWeek": "5 h 00",
    "confidence": "Élevée",
    "observed": [
     "520 occurrences sur la semaine observée",
     "60 personnes concernées (E-commerce, Opérations)",
     "5 exception(s) relevée(s) : Seulement deux commandes ouvertes en détail (#107, #142)",
     "5 façons de la nommer chez les salariés"
    ],
    "sequence": [
     "Ouvrir la liste Orders",
     "Ouvrir Filters et choisir le",
     "Appliquer les filtres"
    ],
    "solution": "Skill « Consultation des commandes annulées » : les étapes observées deviennent une automatisation, les décisions restent humaines (score 83/100)."
   }
  },
  {
   "id": 3,
   "cat": "Ressaisie",
   "path": "E-commerce, Opérations",
   "title": "Modifier le prix d'un produit ou d'une variante",
   "metaBits": [
    "370 fois / sem.",
    "5 h 00 / sem.",
    "Automatisable : oui"
   ],
   "annualCost": 8740,
   "status": "À valider",
   "detail": {
    "description": "Séquence très régulière (recherche, ouverture, saisie, enregistrement) répétée sur les variantes ; une mise à jour en masse ou un import CSV éviterait les allers-retours.",
    "lostPerWeek": "5 h 00",
    "confidence": "Élevée",
    "observed": [
     "370 occurrences sur la semaine observée",
     "50 personnes concernées (E-commerce, Opérations)",
     "5 exception(s) relevée(s) : Certains produits n'ont que 1 à 3 variantes, d'autres jusqu'à 6",
     "5 façons de la nommer chez les salariés"
    ],
    "sequence": [
     "Rechercher le produit par mo",
     "Ouvrir la fiche produit ou v",
     "Saisir le nouveau prix dans "
    ],
    "solution": "Skill « Modifier le prix d'un produit ou d'une variante » : les étapes observées deviennent une automatisation, les décisions restent humaines (score 93/100)."
   }
  },
  {
   "id": 4,
   "cat": "Recherche",
   "path": "E-commerce, Opérations",
   "title": "Consulter les avis d'un produit depuis sa fiche",
   "metaBits": [
    "260 fois / sem.",
    "5 h 00 / sem.",
    "Automatisable : partiel"
   ],
   "annualCost": 8740,
   "status": "À valider",
   "detail": {
    "description": "Le parcours est identique à chaque fois et la lecture pourrait être remplacée par une vue ou un export des avis par produit ; l'objectif de la lecture reste inconnu.",
    "lostPerWeek": "5 h 00",
    "confidence": "Moyenne",
    "observed": [
     "260 occurrences sur la semaine observée",
     "30 personnes concernées (E-commerce, Opérations)",
     "3 exception(s) relevée(s) : Recherche parfois corrigée plusieurs fois avant de trouver le bon produit (touches effacer",
     "3 façons de la nommer chez les salariés"
    ],
    "sequence": [
     "Chercher le produit par nom ",
     "Ouvrir la fiche produit",
     "Ouvrir la section « Product "
    ],
    "solution": "Skill « Consulter les avis d'un produit depuis sa fiche » : les étapes observées deviennent une automatisation, les décisions restent humaines (score 45/100)."
   }
  },
  {
   "id": 5,
   "cat": "Recherche",
   "path": "E-commerce, Opérations",
   "title": "Filtrer les commandes annulées",
   "metaBits": [
    "280 fois / sem.",
    "3 h 00 / sem.",
    "Automatisable : partiel"
   ],
   "annualCost": 5244,
   "status": "À valider",
   "detail": {
    "description": "Filtres identiques à chaque fois ; une vue enregistrée suffirait. Valeurs saisies non captées, donc incertain.",
    "lostPerWeek": "3 h 00",
    "confidence": "Moyenne",
    "observed": [
     "280 occurrences sur la semaine observée",
     "60 personnes concernées (E-commerce, Opérations)",
     "3 exception(s) relevée(s) : Un moment n'affiche pas Create Configurations dans le texte capté",
     "5 façons de la nommer chez les salariés"
    ],
    "sequence": [
     "Ouvrir la liste des commande",
     "Ouvrir les filtres",
     "Choisir le statut Annulée"
    ],
    "solution": "Skill « Filtrer les commandes annulées » : les étapes observées deviennent une automatisation, les décisions restent humaines (score 62/100)."
   }
  },
  {
   "id": 6,
   "cat": "Ressaisie",
   "path": "E-commerce, Opérations",
   "title": "Corriger l'adresse d'une commande",
   "metaBits": [
    "240 fois / sem.",
    "2 h 00 / sem.",
    "Automatisable : partiel"
   ],
   "annualCost": 3496,
   "status": "À valider",
   "detail": {
    "description": "Lecture d'information pour décision humaine ; un export des détails pourrait remplacer l'ouverture une à une.",
    "lostPerWeek": "2 h 00",
    "confidence": "Moyenne",
    "observed": [
     "240 occurrences sur la semaine observée",
     "40 personnes concernées (E-commerce, Opérations)",
     "5 exception(s) relevée(s) : Va-et-vient de 1 à 3 commandes selon le moment",
     "3 façons de la nommer chez les salariés"
    ],
    "sequence": [
     "Rechercher la commande par n",
     "Ouvrir l'adresse de livraiso",
     "Saisir la rue, sélectionner "
    ],
    "solution": "Skill « Corriger l'adresse d'une commande » : les étapes observées deviennent une automatisation, les décisions restent humaines (score 64/100)."
   }
  },
  {
   "id": 7,
   "cat": "Ressaisie",
   "path": "E-commerce, Opérations",
   "title": "Rapport du nombre de commandes clients",
   "metaBits": [
    "220 fois / sem.",
    "2 h 00 / sem.",
    "Automatisable : oui"
   ],
   "annualCost": 3496,
   "status": "À valider",
   "detail": {
    "description": "Même rapport avec des paramètres de dates seulement ; réutilisable par un export ou une requête.",
    "lostPerWeek": "2 h 00",
    "confidence": "Élevée",
    "observed": [
     "220 occurrences sur la semaine observée",
     "40 personnes concernées (E-commerce, Opérations)",
     "5 exception(s) relevée(s) : Deux modes de saisie : calendrier (mois, année) ou champs de date",
     "4 façons de la nommer chez les salariés"
    ],
    "sequence": [
     "Ouvrir Rapports > Clients > ",
     "Saisir ou sélectionner la pl",
     "Choisir le regroupement Day"
    ],
    "solution": "Skill « Rapport du nombre de commandes clients » : les étapes observées deviennent une automatisation, les décisions restent humaines (score 75/100)."
   }
  },
  {
   "id": 8,
   "cat": "Recherche",
   "path": "E-commerce, Opérations",
   "title": "Rechercher et filtrer les avis clients",
   "metaBits": [
    "470 fois / sem.",
    "2 h 00 / sem.",
    "Automatisable : partiel"
   ],
   "annualCost": 3496,
   "status": "À valider",
   "detail": {
    "description": "Les recherches par mots-clés d'opinion pourraient être faites par un tri automatique ; la modération elle-même demande un jugement.",
    "lostPerWeek": "2 h 00",
    "confidence": "Moyenne",
    "observed": [
     "470 occurrences sur la semaine observée",
     "50 personnes concernées (E-commerce, Opérations)",
     "5 exception(s) relevée(s) : L'enregistrement d'un avis n'apparaît que deux fois (#131-#132)",
     "5 façons de la nommer chez les salariés"
    ],
    "sequence": [
     "Ouvrir Marketing > User Cont",
     "Choisir le critère de filtre",
     "Saisir le mot-clé ou les dat"
    ],
    "solution": "Skill « Rechercher et filtrer les avis clients » : les étapes observées deviennent une automatisation, les décisions restent humaines (score 55/100)."
   }
  },
  {
   "id": 9,
   "cat": "Répétition",
   "path": "E-commerce, Opérations",
   "title": "Création d'une règle de prix panier",
   "metaBits": [
    "150 fois / sem.",
    "1 h 00 / sem.",
    "Automatisable : partiel"
   ],
   "annualCost": 1748,
   "status": "À valider",
   "detail": {
    "description": "Formulaire identique d'une règle à l'autre ; seuls nom et pourcentage varient.",
    "lostPerWeek": "1 h 00",
    "confidence": "Élevée",
    "observed": [
     "150 occurrences sur la semaine observée",
     "30 personnes concernées (E-commerce, Opérations)",
     "2 exception(s) relevée(s) : Un nom de règle contient des artefacts de touches (Key.space) dans la saisie captée",
     "3 façons de la nommer chez les salariés"
    ],
    "sequence": [
     "Cliquer sur Add New Rule",
     "Saisir le nom de la règle",
     "Choisir site web et groupes "
    ],
    "solution": "Skill « Création d'une règle de prix panier » : les étapes observées deviennent une automatisation, les décisions restent humaines (score 65/100)."
   }
  },
  {
   "id": 10,
   "cat": "Recherche",
   "path": "E-commerce, Opérations",
   "title": "Retrouver une fiche client par numéro de téléphone",
   "metaBits": [
    "190 fois / sem.",
    "1 h 00 / sem.",
    "Automatisable : partiel"
   ],
   "annualCost": 1748,
   "status": "À valider",
   "detail": {
    "description": "Recherche simple, mais l'origine des identifiants n'est pas visible ; automatisable surtout si une liste est fournie.",
    "lostPerWeek": "1 h 00",
    "confidence": "Moyenne",
    "observed": [
     "190 occurrences sur la semaine observée",
     "30 personnes concernées (E-commerce, Opérations)",
     "5 exception(s) relevée(s) : Recherche par nom via filtre plutôt que par mot-clé (#137)",
     "3 façons de la nommer chez les salariés"
    ],
    "sequence": [
     "Ouvrir la liste All Customer",
     "Ouvrir les filtres et saisir",
     "Appliquer les filtres"
    ],
    "solution": "Skill « Retrouver une fiche client par numéro de téléphone » : les étapes observées deviennent une automatisation, les décisions restent humaines (score 60/100)."
   }
  },
  {
   "id": 11,
   "cat": "Ressaisie",
   "path": "E-commerce, Opérations",
   "title": "Remettre un produit en stock",
   "metaBits": [
    "150 fois / sem.",
    "1 h 00 / sem.",
    "Automatisable : oui"
   ],
   "annualCost": 1748,
   "status": "À valider",
   "detail": {
    "description": "Filtres répétables en vue enregistrée, mais critères inconnus.",
    "lostPerWeek": "1 h 00",
    "confidence": "Élevée",
    "observed": [
     "150 occurrences sur la semaine observée",
     "30 personnes concernées (E-commerce, Opérations)",
     "2 exception(s) relevée(s) : Critères de filtre non visibles dans les moments 28 et 31",
     "3 façons de la nommer chez les salariés"
    ],
    "sequence": [
     "Rechercher le produit par mo",
     "Ouvrir la fiche avec Edit",
     "Passer l'état de stock à « I"
    ],
    "solution": "Skill « Remettre un produit en stock » : les étapes observées deviennent une automatisation, les décisions restent humaines (score 78/100)."
   }
  }
 ],
 "extraProblemsCount": 8,
 "extraProblemsHoursSupplement": "8 h 00 / sem.",
 "interactions": {
  "stats": [
   {
    "label": "Tâches communes aux 2 équipes",
    "value": "11",
    "sub": "sur 11 visibles"
   },
   {
    "label": "Écrans Magento utilisés",
    "value": "7",
    "sub": "sections du back-office"
   },
   {
    "label": "Écran le plus utilisé",
    "value": "Catalogue",
    "sub": ""
   },
   {
    "label": "Temps passé à attendre une info",
    "value": "Non mesuré",
    "sub": "un seul outil observé"
   }
  ],
  "weekLabel": "Du 13 au 19 octobre (5 jours travaillés)",
  "nodes": [
   {
    "id": "ecom",
    "label": "E-commerce",
    "sub": "30 pers. · 26 h 12",
    "x": 14,
    "y": 30
   },
   {
    "id": "ops",
    "label": "Opérations",
    "sub": "30 pers. · 27 h 35",
    "x": 14,
    "y": 72
   },
   {
    "id": "catalogue",
    "label": "Catalogue",
    "sub": "1276 min observées",
    "x": 80,
    "y": 8,
    "highlight": "goulot"
   },
   {
    "id": "commandes",
    "label": "Commandes",
    "sub": "777 min observées",
    "x": 80,
    "y": 25
   },
   {
    "id": "rapports",
    "label": "Rapports",
    "sub": "474 min observées",
    "x": 80,
    "y": 42
   },
   {
    "id": "avis",
    "label": "Avis",
    "sub": "302 min observées",
    "x": 80,
    "y": 59
   },
   {
    "id": "clients",
    "label": "Clients",
    "sub": "72 min observées",
    "x": 80,
    "y": 76
   },
   {
    "id": "marketing",
    "label": "Marketing",
    "sub": "147 min observées",
    "x": 80,
    "y": 93
   }
  ],
  "edges": [
   {
    "from": "ecom",
    "to": "catalogue",
    "label": "31 %",
    "detail": "E-commerce · Catalogue : 31 % de son temps",
    "level": "goulot"
   },
   {
    "from": "ops",
    "to": "catalogue",
    "label": "47 %",
    "detail": "Opérations · Catalogue : 47 % de son temps",
    "level": "goulot"
   },
   {
    "from": "ecom",
    "to": "commandes",
    "label": "23 %",
    "detail": "E-commerce · Commandes : 23 % de son temps",
    "level": "attente"
   },
   {
    "from": "ops",
    "to": "commandes",
    "label": "25 %",
    "detail": "Opérations · Commandes : 25 % de son temps",
    "level": "attente"
   },
   {
    "from": "ecom",
    "to": "rapports",
    "label": "20 %",
    "detail": "E-commerce · Rapports : 20 % de son temps",
    "level": "attente"
   },
   {
    "from": "ecom",
    "to": "avis",
    "label": "12 %",
    "detail": "E-commerce · Avis : 12 % de son temps",
    "level": "fluide"
   }
  ],
  "legend": [
   {
    "label": "moins de 15 % du temps",
    "level": "fluide"
   },
   {
    "label": "15 à 30 %",
    "level": "attente"
   },
   {
    "label": "plus de 30 %",
    "level": "goulot"
   }
  ],
  "legendNote": "Équipe → écran du back-office : part de son temps",
  "bottlenecks": [
   {
    "tag": "Travail refait",
    "title": "37 h 00 par semaine, dans 14 tâches",
    "text": "Mêmes plages de dates ressaisies à plusieurs reprises (1/1/10-1/13/24 sur #57-#60, 1/1/23-1/13/24 sur #88-#91)",
    "link": "Voir le problème n° 01",
    "problemId": 1
   },
   {
    "tag": "Allers-retours",
    "title": "26 h 00 par semaine, dans 11 tâches",
    "text": "Va-et-vient entre la liste des commandes et la liste des clients (#54, #55)",
    "link": "Voir le problème n° 02",
    "problemId": 2
   },
   {
    "tag": "Passage de relais",
    "title": "1 h 00 par semaine, dans 1 tâches",
    "text": "Le numéro de suivi vient d'une source extérieure non visible, saisi à la main",
    "link": null,
    "problemId": null
   }
  ],
  "waitTeams": [],
  "waitMatrix": [],
  "waitNote": "Non mesuré : Atelier Nova n'a été observé que dans Magento. Les attentes entre équipes demandent la messagerie (mail, chat) dans la capture."
 },
 "tools": {
  "stats": [
   {
    "label": "Temps dans votre outil métier",
    "value": "100 %",
    "sub": "Magento (seul outil observé)"
   },
   {
    "label": "Changements d'écran",
    "value": "326",
    "sub": "par jour et par poste"
   },
   {
    "label": "Allers-retours entre écrans",
    "value": "9 780",
    "sub": "sur la semaine"
   },
   {
    "label": "Temps en messagerie et tableurs",
    "value": "Non mesuré",
    "sub": "absent de ces données"
   }
  ],
  "appCategories": [
   "Rapports",
   "Catalogue",
   "Commandes",
   "Avis",
   "Clients",
   "Marketing",
   "Accueil"
  ],
  "byTeam": [
   {
    "team": "E-commerce",
    "values": [
     20,
     31,
     23,
     12,
     3,
     3,
     8
    ]
   },
   {
    "team": "Opérations",
    "values": [
     10,
     47,
     25,
     7,
     1,
     6,
     4
    ]
   }
  ],
  "byTeamTitle": "Répartition du temps par écran du back-office",
  "callout": "Le catalogue et les commandes concentrent l'essentiel du temps. Rapport ventes/produits sur une période revient 790 fois par semaine chez les 2 équipes.",
  "heatmapHours": [
   "8h",
   "9h",
   "10h",
   "11h",
   "12h",
   "13h",
   "14h",
   "15h",
   "16h",
   "17h",
   "18h"
  ],
  "heatmapDays": [
   "Mar 13",
   "Mer 14",
   "Jeu 15",
   "Ven 16",
   "Lun 19"
  ],
  "heatmapMatrix": [
   [
    0,
    3,
    3,
    3,
    3,
    2,
    2,
    2,
    2,
    1,
    0
   ],
   [
    0,
    2,
    3,
    3,
    3,
    3,
    4,
    2,
    2,
    2,
    0
   ],
   [
    0,
    4,
    2,
    2,
    2,
    2,
    2,
    3,
    2,
    2,
    0
   ],
   [
    0,
    3,
    2,
    3,
    4,
    5,
    3,
    4,
    3,
    1,
    0
   ],
   [
    0,
    1,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
   ]
  ],
  "heatmapPeakNote": "Pic : vendredi 16 oct., 13 h–14 h",
  "sequences": [
   {
    "path": "Accueil → Commandes → Accueil",
    "count": 1100
   },
   {
    "path": "Accueil → Catalogue → Accueil",
    "count": 1080
   },
   {
    "path": "Accueil → Rapports → Accueil",
    "count": 970
   },
   {
    "path": "Accueil → Avis → Accueil",
    "count": 910
   }
  ],
  "copyPasteTitle": "Allers-retours les plus fréquents",
  "copyPaste": [
   {
    "path": "Accueil → Catalogue",
    "count": 1150
   },
   {
    "path": "Accueil → Commandes",
    "count": 1130
   },
   {
    "path": "Accueil → Rapports",
    "count": 1100
   },
   {
    "path": "Catalogue → Accueil",
    "count": 1100
   }
  ]
 },
 "businessCase": {
  "stats": [
   {
    "label": "Coût annuel des tâches répétées observées",
    "value": "71 668 €",
    "sub": "41 h 00 par semaine, sur 19 tâches"
   },
   {
    "label": "Gain annuel récupérable",
    "value": "49 320 €",
    "sub": "69 % du temps de ces tâches",
    "accent": "good"
   },
   {
    "label": "Capacité libérée",
    "value": "0,81 ETP",
    "sub": "base 35 h / semaine"
   }
  ],
  "modules": [
   {
    "order": 1,
    "name": "Skill · Modifier le prix d'un produit ou d'une variante",
    "tag": "Gain rapide",
    "problems": "n° 03",
    "recovered": "4 h 46 / sem.",
    "gain": 8343,
    "delay": "1 sem."
   },
   {
    "order": 2,
    "name": "Skill · Rapport ventes/produits sur une période",
    "tag": null,
    "problems": "n° 01",
    "recovered": "4 h 09 / sem.",
    "gain": 7261,
    "delay": "2 sem."
   },
   {
    "order": 3,
    "name": "Skill · Consultation des commandes annulées",
    "tag": "Gain rapide",
    "problems": "n° 02",
    "recovered": "4 h 08 / sem.",
    "gain": 7220,
    "delay": "1 sem."
   },
   {
    "order": 4,
    "name": "Skill · Consulter les avis d'un produit depuis sa fiche",
    "tag": null,
    "problems": "n° 04",
    "recovered": "2 h 15 / sem.",
    "gain": 3933,
    "delay": "2 sem."
   },
   {
    "order": 5,
    "name": "Skill · Régénérer les variantes d'un produit configurable existant",
    "tag": null,
    "problems": "moins de 3 pers.",
    "recovered": "1 h 56 / sem.",
    "gain": 3371,
    "delay": "2 sem."
   }
  ],
  "modulesNote": "Tâches WONDERBREAD courtes (moins d'1 min 30) : les montants sont faibles, mais chaque chiffre vient d'une tâche observée et cliquable.",
  "beforeAfter": {
   "before": "41 h 00",
   "after": "12 h 47",
   "beforeH": 41.0,
   "afterH": 12.785,
   "note": "28 h 13 rendues chaque semaine aux 60 postes."
  },
  "investment": [
   {
    "label": "Étude (une fois)",
    "value": "[À COMPLÉTER]"
   },
   {
    "label": "Abonnement logiciel",
    "value": "[À COMPLÉTER]"
   },
   {
    "label": "Gain net la première année",
    "value": "[À COMPLÉTER]"
   },
   {
    "label": "Retour sur investissement",
    "value": "[À COMPLÉTER]"
   }
  ],
  "assumptions": [
   "Coût horaire chargé : 38 €/h",
   "Semaines travaillées : 46 / an",
   "Base : 5 jours d'observation, 6 postes, volumes ×10 (simulation)",
   "Fréquences = occurrences observées sur la semaine",
   "Gain = coût × score d'automatisation (fusion officielle)",
   "Résumés non relus par des humains : à confirmer"
  ]
 },
 "piloting": {
  "inProductionSince": "Projection · aucun module n'est encore en production",
  "stats": [
   {
    "label": "Heures récupérables par mois",
    "value": "108 h 09",
    "sub": "si les 5 skills sont déployées",
    "progress": 0
   },
   {
    "label": "Valeur annuelle visée",
    "value": "49 320 €",
    "sub": "pas encore générée"
   },
   {
    "label": "Tâches automatisables",
    "value": "5",
    "sub": "classées par gain"
   },
   {
    "label": "Adoption",
    "value": "—",
    "sub": "mesurée après déploiement"
   }
  ],
  "chart": {
   "xLabels": [
    "Étude",
    "Aujourd'hui"
   ],
   "measured": [
    41.0,
    41.0
   ],
   "objective": 12.78,
   "objectiveLabel": "12 h 47",
   "annotations": []
  },
  "modules": [
   {
    "name": "Skill · Modifier le prix d'un produit ou d'une variante",
    "status": "Planifié"
   },
   {
    "name": "Skill · Rapport ventes/produits sur une période",
    "status": "Planifié"
   },
   {
    "name": "Skill · Consultation des commandes annulées",
    "status": "Planifié"
   },
   {
    "name": "Skill · Consulter les avis d'un produit depuis sa fiche",
    "status": "Planifié"
   },
   {
    "name": "Skill · Régénérer les variantes d'un produit configurable existant",
    "status": "Planifié"
   }
  ],
  "toHandle": [
   {
    "icon": "warning",
    "title": "Cas d'arrêt à définir",
    "text": "La page « Dès que… » relève les exceptions de chaque tâche : il faut dire qui prévenir.",
    "link": "Ouvrir les déclencheurs"
   },
   {
    "icon": "info",
    "title": "54,0 h observées sur 10 h demandées",
    "text": "Les tâches WONDERBREAD sont courtes : le seuil du cabinet n'est pas atteint.",
    "link": "Voir les limites"
   },
   {
    "icon": "plus",
    "title": "Relecture par les salariés",
    "text": "Les résumés ont été validés pour la démo : une vraie campagne passe par la relecture.",
    "link": "Lancer la relecture"
   }
  ],
  "nextImpact": {
   "dateRange": "Après le module n° 1",
   "text": "3 jours d'observation pour mesurer le gain réel de la première skill.",
   "note": "Hors de ces campagnes, aucune capture d'écran : seuls les journaux des skills."
  },
  "requests": []
 },
 "dash": {
  "echelle": 10.0,
  "postes": 60,
  "equipes": {
   "E-commerce": 30,
   "Opérations": 30
  },
  "cout_horaire": 38.0,
  "heures_observees": 54.0,
  "jours": [
   "Mar 13",
   "Mer 14",
   "Jeu 15",
   "Ven 16",
   "Lun 19"
  ],
  "heures_par_jour": {
   "E-commerce": [
    6.57,
    5.23,
    6.59,
    6.82,
    0.99
   ],
   "Opérations": [
    4.86,
    8.47,
    5.5,
    8.75,
    0.0
   ]
  },
  "ecrans": [
   "Rapports",
   "Catalogue",
   "Commandes",
   "Avis",
   "Clients",
   "Marketing",
   "Accueil"
  ],
  "minutes_ecran_jour": {
   "E-commerce": [
    [
     156,
     153,
     0,
     42,
     0,
     5,
     37
    ],
    [
     107,
     76,
     47,
     52,
     1,
     3,
     27
    ],
    [
     12,
     133,
     150,
     0,
     40,
     36,
     24
    ],
    [
     36,
     124,
     119,
     92,
     13,
     0,
     27
    ],
    [
     0,
     8,
     47,
     0,
     0,
     0,
     3
    ]
   ],
   "Opérations": [
    [
     49,
     91,
     58,
     12,
     0,
     68,
     13
    ],
    [
     31,
     240,
     167,
     22,
     0,
     35,
     14
    ],
    [
     83,
     76,
     111,
     25,
     17,
     0,
     17
    ],
    [
     0,
     375,
     77,
     57,
     0,
     0,
     16
    ],
    [
     0,
     0,
     0,
     0,
     0,
     0,
     0
    ]
   ]
  },
  "chaleur": {
   "E-commerce": [
    [
     0,
     48,
     74,
     56,
     73,
     34,
     32,
     32,
     32,
     13,
     0
    ],
    [
     0,
     29,
     35,
     34,
     32,
     35,
     47,
     35,
     31,
     36,
     0
    ],
    [
     0,
     91,
     39,
     29,
     42,
     55,
     43,
     51,
     28,
     18,
     0
    ],
    [
     0,
     29,
     29,
     41,
     87,
     81,
     46,
     39,
     39,
     19,
     0
    ],
    [
     0,
     46,
     13,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0
    ]
   ],
   "Opérations": [
    [
     0,
     48,
     21,
     32,
     41,
     33,
     37,
     38,
     29,
     13,
     0
    ],
    [
     0,
     35,
     59,
     77,
     69,
     69,
     100,
     22,
     50,
     27,
     0
    ],
    [
     0,
     32,
     27,
     31,
     30,
     30,
     40,
     65,
     40,
     35,
     0
    ],
    [
     0,
     64,
     52,
     46,
     49,
     89,
     73,
     89,
     55,
     8,
     0
    ],
    [
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0
    ]
   ]
  },
  "minutes_ecran": {
   "E-commerce": [
    310,
    494,
    364,
    186,
    54,
    45,
    119
   ],
   "Opérations": [
    164,
    782,
    413,
    116,
    17,
    102,
    61
   ]
  },
  "taches": [
   {
    "titre": "Rapport ventes/produits sur une période",
    "court": "Rapport ventes",
    "personnes": 60,
    "equipes": [
     "E-commerce",
     "Opérations"
    ],
    "frequence": 790,
    "heures_semaine": 6.0,
    "cout_an": 10488,
    "gain_an": 7261,
    "heures_gagnees": 4.15,
    "score": 68,
    "categorie": "Ressaisie",
    "visible": true,
    "etapes": [
     "Ouvrir un rapport (Bestsellers, Orders, Tax, Shipping, Coupons, Refunds, Product Views)",
     "Saisir la date de début et la date de fin",
     "Choisir le regroupement (Day) pour certains rapports",
     "Cliquer sur Show Report",
     "Faire défiler et lire les résultats"
    ]
   },
   {
    "titre": "Consultation des commandes annulées",
    "court": "Commandes annulées",
    "personnes": 60,
    "equipes": [
     "E-commerce",
     "Opérations"
    ],
    "frequence": 520,
    "heures_semaine": 5.0,
    "cout_an": 8740,
    "gain_an": 7220,
    "heures_gagnees": 4.13,
    "score": 83,
    "categorie": "Recherche",
    "visible": true,
    "etapes": [
     "Ouvrir la liste Orders",
     "Ouvrir Filters et choisir le statut Canceled",
     "Appliquer les filtres",
     "Lire la liste filtrée"
    ]
   },
   {
    "titre": "Modifier le prix d'un produit ou d'une variante",
    "court": "Prix produit",
    "personnes": 50,
    "equipes": [
     "E-commerce",
     "Opérations"
    ],
    "frequence": 370,
    "heures_semaine": 5.0,
    "cout_an": 8740,
    "gain_an": 8343,
    "heures_gagnees": 4.77,
    "score": 93,
    "categorie": "Ressaisie",
    "visible": true,
    "etapes": [
     "Rechercher le produit par mot-clé dans le catalogue",
     "Ouvrir la fiche produit ou variante",
     "Saisir le nouveau prix dans le champ prix",
     "Enregistrer",
     "Vérifier que la modification est bien prise en compte"
    ]
   },
   {
    "titre": "Consulter les avis d'un produit depuis sa fiche",
    "court": "Avis produit",
    "personnes": 30,
    "equipes": [
     "E-commerce",
     "Opérations"
    ],
    "frequence": 260,
    "heures_semaine": 5.0,
    "cout_an": 8740,
    "gain_an": 3933,
    "heures_gagnees": 2.25,
    "score": 45,
    "categorie": "Recherche",
    "visible": true,
    "etapes": [
     "Chercher le produit par nom dans le catalogue",
     "Ouvrir la fiche produit",
     "Ouvrir la section « Product Reviews » de la fiche",
     "Lire les avis en faisant défiler",
     "Passer au produit suivant ou revenir en arrière"
    ]
   },
   {
    "titre": "Régénérer les variantes d'un produit configurable existant",
    "court": "Variantes produit",
    "personnes": 0,
    "equipes": [
     "Opérations"
    ],
    "frequence": 120,
    "heures_semaine": 3.0,
    "cout_an": 5244,
    "gain_an": 3371,
    "heures_gagnees": 1.93,
    "score": 64,
    "categorie": "Ressaisie",
    "visible": false,
    "etapes": []
   },
   {
    "titre": "Filtrer les commandes annulées",
    "court": "Filtre annulées",
    "personnes": 60,
    "equipes": [
     "E-commerce",
     "Opérations"
    ],
    "frequence": 280,
    "heures_semaine": 3.0,
    "cout_an": 5244,
    "gain_an": 3227,
    "heures_gagnees": 1.85,
    "score": 62,
    "categorie": "Recherche",
    "visible": true,
    "etapes": [
     "Ouvrir la liste des commandes",
     "Ouvrir les filtres",
     "Choisir le statut Annulée",
     "Appliquer les filtres et consulter le résultat"
    ]
   },
   {
    "titre": "Corriger l'adresse d'une commande",
    "court": "Adresse commande",
    "personnes": 40,
    "equipes": [
     "E-commerce",
     "Opérations"
    ],
    "frequence": 240,
    "heures_semaine": 2.0,
    "cout_an": 3496,
    "gain_an": 2447,
    "heures_gagnees": 1.4,
    "score": 64,
    "categorie": "Ressaisie",
    "visible": true,
    "etapes": [
     "Rechercher la commande par numéro",
     "Ouvrir l'adresse de livraison en édition",
     "Saisir la rue, sélectionner l'état, saisir la ville et le code postal",
     "Enregistrer l'adresse"
    ]
   },
   {
    "titre": "Rapport du nombre de commandes clients",
    "court": "Rapport commandes",
    "personnes": 40,
    "equipes": [
     "E-commerce",
     "Opérations"
    ],
    "frequence": 220,
    "heures_semaine": 2.0,
    "cout_an": 3496,
    "gain_an": 2447,
    "heures_gagnees": 1.4,
    "score": 75,
    "categorie": "Ressaisie",
    "visible": true,
    "etapes": [
     "Ouvrir Rapports > Clients > Order Count",
     "Saisir ou sélectionner la plage de dates",
     "Choisir le regroupement Day",
     "Cliquer sur Refresh",
     "Faire défiler le résultat"
    ]
   },
   {
    "titre": "Rechercher et filtrer les avis clients",
    "court": "Recherche avis",
    "personnes": 50,
    "equipes": [
     "E-commerce",
     "Opérations"
    ],
    "frequence": 470,
    "heures_semaine": 2.0,
    "cout_an": 3496,
    "gain_an": 1748,
    "heures_gagnees": 1.0,
    "score": 55,
    "categorie": "Recherche",
    "visible": true,
    "etapes": [
     "Ouvrir Marketing > User Content > All Reviews",
     "Choisir le critère de filtre : mot-clé, statut Approved ou plage de dates",
     "Saisir le mot-clé ou les dates From/To",
     "Lancer la recherche",
     "Lire les avis obtenus"
    ]
   },
   {
    "titre": "Création d'une règle de prix panier",
    "court": "Règle prix panier",
    "personnes": 30,
    "equipes": [
     "E-commerce",
     "Opérations"
    ],
    "frequence": 150,
    "heures_semaine": 1.0,
    "cout_an": 1748,
    "gain_an": 1049,
    "heures_gagnees": 0.6,
    "score": 65,
    "categorie": "Répétition",
    "visible": true,
    "etapes": [
     "Cliquer sur Add New Rule",
     "Saisir le nom de la règle",
     "Choisir site web et groupes de clients (ex. non connecté)",
     "Onglet Actions : type de remise en pourcentage et valeur",
     "Règle de promotion enregistrée"
    ]
   },
   {
    "titre": "Retrouver une fiche client par numéro de téléphone",
    "court": "Fiche client",
    "personnes": 30,
    "equipes": [
     "E-commerce",
     "Opérations"
    ],
    "frequence": 190,
    "heures_semaine": 1.0,
    "cout_an": 1748,
    "gain_an": 1049,
    "heures_gagnees": 0.6,
    "score": 60,
    "categorie": "Recherche",
    "visible": true,
    "etapes": [
     "Ouvrir la liste All Customers",
     "Ouvrir les filtres et saisir un numéro de téléphone",
     "Appliquer les filtres",
     "Consulter la fiche client trouvée"
    ]
   },
   {
    "titre": "Remettre un produit en stock",
    "court": "Remise en stock",
    "personnes": 30,
    "equipes": [
     "E-commerce",
     "Opérations"
    ],
    "frequence": 150,
    "heures_semaine": 1.0,
    "cout_an": 1748,
    "gain_an": 1398,
    "heures_gagnees": 0.8,
    "score": 78,
    "categorie": "Ressaisie",
    "visible": true,
    "etapes": [
     "Rechercher le produit par mot-clé",
     "Ouvrir la fiche avec Edit",
     "Passer l'état de stock à « In Stock »",
     "Enregistrer"
    ]
   },
   {
    "titre": "Mettre à jour la quantité en stock des déclinaisons",
    "court": "Stock déclinaisons",
    "personnes": 0,
    "equipes": [
     "Opérations"
    ],
    "frequence": 60,
    "heures_semaine": 1.0,
    "cout_an": 1748,
    "gain_an": 1311,
    "heures_gagnees": 0.75,
    "score": 91,
    "categorie": "Ressaisie",
    "visible": false,
    "etapes": []
   },
   {
    "titre": "Créer un nouveau produit configurable avec ses variantes",
    "court": "Nouveau produit",
    "personnes": 0,
    "equipes": [
     "Opérations"
    ],
    "frequence": 50,
    "heures_semaine": 1.0,
    "cout_an": 1748,
    "gain_an": 1311,
    "heures_gagnees": 0.75,
    "score": 80,
    "categorie": "Répétition",
    "visible": false,
    "etapes": []
   },
   {
    "titre": "Modifier le contenu d'une page CMS",
    "court": "Page CMS",
    "personnes": 0,
    "equipes": [
     "Opérations"
    ],
    "frequence": 90,
    "heures_semaine": 1.0,
    "cout_an": 1748,
    "gain_an": 1165,
    "heures_gagnees": 0.67,
    "score": 50,
    "categorie": "Répétition",
    "visible": false,
    "etapes": []
   },
   {
    "titre": "Expédier une commande avec numéro de suivi",
    "court": "Expédition",
    "personnes": 0,
    "equipes": [
     "Opérations"
    ],
    "frequence": 40,
    "heures_semaine": 1.0,
    "cout_an": 1748,
    "gain_an": 1165,
    "heures_gagnees": 0.67,
    "score": 70,
    "categorie": "Répétition",
    "visible": false,
    "etapes": []
   },
   {
    "titre": "Modération des avis en attente",
    "court": "Modération avis",
    "personnes": 0,
    "equipes": [
     "E-commerce",
     "Opérations"
    ],
    "frequence": 80,
    "heures_semaine": 1.0,
    "cout_an": 1748,
    "gain_an": 874,
    "heures_gagnees": 0.5,
    "score": 52,
    "categorie": "Ressaisie",
    "visible": false,
    "etapes": []
   },
   {
    "titre": "Filtrer la liste des commandes annulées",
    "court": "Liste annulées",
    "personnes": 0,
    "equipes": [
     "Opérations"
    ],
    "frequence": 50,
    "heures_semaine": 0.0,
    "cout_an": 0,
    "gain_an": 0,
    "heures_gagnees": 0.0,
    "score": 75,
    "categorie": "Recherche",
    "visible": false,
    "etapes": []
   },
   {
    "titre": "Consulter les termes de recherche par nombre de résultats",
    "court": "Termes recherche",
    "personnes": 0,
    "equipes": [
     "Opérations"
    ],
    "frequence": 20,
    "heures_semaine": 0.0,
    "cout_an": 0,
    "gain_an": 0,
    "heures_gagnees": 0.0,
    "score": 70,
    "categorie": "Recherche",
    "visible": false,
    "etapes": []
   }
  ],
  "a_automatiser": [
   "Modifier le prix d'un produit ou d'une variante",
   "Consultation des commandes annulées",
   "Rapport ventes/produits sur une période",
   "Consulter les avis d'un produit depuis sa fiche",
   "Régénérer les variantes d'un produit configurable existant"
  ],
  "goulots": [
   {
    "type": "Travail refait",
    "heures_semaine": 37.0,
    "taches": 14
   },
   {
    "type": "Allers-retours",
    "heures_semaine": 26.0,
    "taches": 11
   },
   {
    "type": "Passage de relais",
    "heures_semaine": 1.0,
    "taches": 1
   }
  ],
  "cout_an": 71668,
  "gain_an": 49320,
  "heures_semaine": 41.0,
  "heures_gagnees_semaine": 28.22,
  "chaine": {
   "captures": 55510,
   "gardees": 50480,
   "moments": 14470,
   "taches": 19,
   "problemes": 11,
   "skills": 5
  },
  "bascules": 9780,
  "avancement": 70,
  "etapes": [
   {
    "label": "Installation",
    "statut": "done"
   },
   {
    "label": "Observation",
    "statut": "done"
   },
   {
    "label": "Analyse par l'IA",
    "statut": "done"
   },
   {
    "label": "Restitution & rapport",
    "statut": "active"
   },
   {
    "label": "Logiciel sur mesure",
    "statut": "upcoming"
   }
  ]
 }
};
