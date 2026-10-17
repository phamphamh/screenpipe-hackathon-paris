// Généré par construire.py à partir des données Atelier Nova (WONDERBREAD, salariés fictifs) : ne pas éditer à la main.
const DATA = {
 "verdicts": {
  "overview": "Observation terminée. <b>Rapport ventes/produits sur une période</b> revient 79 fois par semaine chez les 6 postes : c'est la première tâche à regarder.",
  "problems": "<b>11 problèmes</b> à valider avec vous. Les 3 premiers pèsent 48 % du temps perdu.",
  "interactions": "Les 2 équipes font <b>les mêmes 11 tâches</b>. C'est l'écran <b>Catalogue</b> qui concentre le plus de temps.",
  "tools": "Tout le travail observé se passe dans Magento, avec <b>33 changements d'écran</b> par jour et par poste.",
  "business": "<b>5 skills</b> récupèrent 5 700 € par an. La première se construit en 1 sem.",
  "piloting": "Rien n'est encore en production. Cet écran prendra le relais une fois la première skill déployée."
 },
 "maxKpi": 3,
 "firm": "CAIbinet",
 "client": {
  "name": "Atelier Nova",
  "postes": 6,
  "equipes": 2,
  "abonnement": "Pas encore d'abonnement (projection)"
 },
 "consultant": "Équipe hackathon",
 "studyLabel": "Étude d'efficacité opérationnelle",
 "demoTag": "Données WONDERBREAD · salariés fictifs",
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
    "value": "5 700 €",
    "sub": "en automatisant 5 tâches",
    "accent": "good"
   },
   {
    "label": "Postes observés",
    "value": "6 / 6",
    "sub": "2 équipes de 3 · back-office Magento"
   },
   {
    "label": "Heures de travail observées",
    "value": "5,4 h",
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
    "value": 1.14,
    "known": true
   },
   {
    "day": "Mer 14",
    "value": 1.37,
    "known": true
   },
   {
    "day": "Jeu 15",
    "value": 1.21,
    "known": true
   },
   {
    "day": "Ven 16",
    "value": 1.56,
    "known": true
   },
   {
    "day": "Lun 19",
    "value": 0.1,
    "known": true
   }
  ],
  "teamCoverage": [
   {
    "team": "E-commerce",
    "have": 3,
    "total": 3
   },
   {
    "team": "Opérations",
    "have": 3,
    "total": 3
   }
  ],
  "signals": [
   {
    "tag": "Ressaisie",
    "path": "E-commerce, Opérations",
    "text": "Rapport ventes/produits sur une période",
    "meta": "79 fois / sem. · 36 min / sem.",
    "confidence": "Confiance élevée"
   },
   {
    "tag": "Recherche",
    "path": "E-commerce, Opérations",
    "text": "Consultation des commandes annulées",
    "meta": "52 fois / sem. · 30 min / sem.",
    "confidence": "Confiance élevée"
   },
   {
    "tag": "Ressaisie",
    "path": "E-commerce, Opérations",
    "text": "Modifier le prix d'un produit ou d'une variante",
    "meta": "37 fois / sem. · 30 min / sem.",
    "confidence": "Confiance élevée"
   }
  ],
  "signalsUpdated": "à la fin de l'observation",
  "toRelaunch": [],
  "toRelaunchEmpty": "Aucun : les 6 postes ont validé leur résumé (validation de démo, sans relecture humaine).",
  "compliance": [
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
  "hoursPerWeek": "3 h 18",
  "annualCost": 5770,
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
    "79 fois / sem.",
    "36 min / sem.",
    "Automatisable : partiel"
   ],
   "annualCost": 1049,
   "status": "À valider",
   "detail": {
    "description": "Les paramètres sont connus et répétitifs ; un export planifié ou un appel API éviterait la saisie manuelle, mais la finalité de la lecture n'est pas observée.",
    "lostPerWeek": "36 min",
    "confidence": "Élevée",
    "observed": [
     "79 occurrences sur la semaine observée",
     "6 personnes concernées (E-commerce, Opérations)",
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
    "52 fois / sem.",
    "30 min / sem.",
    "Automatisable : oui"
   ],
   "annualCost": 874,
   "status": "À valider",
   "detail": {
    "description": "Le filtre et le tri sont toujours identiques ; une vue enregistrée ou un rapport automatique des annulations suffirait.",
    "lostPerWeek": "30 min",
    "confidence": "Élevée",
    "observed": [
     "52 occurrences sur la semaine observée",
     "6 personnes concernées (E-commerce, Opérations)",
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
    "37 fois / sem.",
    "30 min / sem.",
    "Automatisable : oui"
   ],
   "annualCost": 874,
   "status": "À valider",
   "detail": {
    "description": "Séquence très régulière (recherche, ouverture, saisie, enregistrement) répétée sur les variantes ; une mise à jour en masse ou un import CSV éviterait les allers-retours.",
    "lostPerWeek": "30 min",
    "confidence": "Élevée",
    "observed": [
     "37 occurrences sur la semaine observée",
     "5 personnes concernées (E-commerce, Opérations)",
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
    "26 fois / sem.",
    "30 min / sem.",
    "Automatisable : partiel"
   ],
   "annualCost": 874,
   "status": "À valider",
   "detail": {
    "description": "Le parcours est identique à chaque fois et la lecture pourrait être remplacée par une vue ou un export des avis par produit ; l'objectif de la lecture reste inconnu.",
    "lostPerWeek": "30 min",
    "confidence": "Moyenne",
    "observed": [
     "26 occurrences sur la semaine observée",
     "3 personnes concernées (E-commerce, Opérations)",
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
    "28 fois / sem.",
    "18 min / sem.",
    "Automatisable : partiel"
   ],
   "annualCost": 524,
   "status": "À valider",
   "detail": {
    "description": "Filtres identiques à chaque fois ; une vue enregistrée suffirait. Valeurs saisies non captées, donc incertain.",
    "lostPerWeek": "18 min",
    "confidence": "Moyenne",
    "observed": [
     "28 occurrences sur la semaine observée",
     "6 personnes concernées (E-commerce, Opérations)",
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
    "24 fois / sem.",
    "12 min / sem.",
    "Automatisable : partiel"
   ],
   "annualCost": 350,
   "status": "À valider",
   "detail": {
    "description": "Lecture d'information pour décision humaine ; un export des détails pourrait remplacer l'ouverture une à une.",
    "lostPerWeek": "12 min",
    "confidence": "Moyenne",
    "observed": [
     "24 occurrences sur la semaine observée",
     "4 personnes concernées (E-commerce, Opérations)",
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
    "22 fois / sem.",
    "12 min / sem.",
    "Automatisable : oui"
   ],
   "annualCost": 350,
   "status": "À valider",
   "detail": {
    "description": "Même rapport avec des paramètres de dates seulement ; réutilisable par un export ou une requête.",
    "lostPerWeek": "12 min",
    "confidence": "Élevée",
    "observed": [
     "22 occurrences sur la semaine observée",
     "4 personnes concernées (E-commerce, Opérations)",
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
    "47 fois / sem.",
    "12 min / sem.",
    "Automatisable : partiel"
   ],
   "annualCost": 350,
   "status": "À valider",
   "detail": {
    "description": "Les recherches par mots-clés d'opinion pourraient être faites par un tri automatique ; la modération elle-même demande un jugement.",
    "lostPerWeek": "12 min",
    "confidence": "Moyenne",
    "observed": [
     "47 occurrences sur la semaine observée",
     "5 personnes concernées (E-commerce, Opérations)",
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
    "15 fois / sem.",
    "6 min / sem.",
    "Automatisable : partiel"
   ],
   "annualCost": 175,
   "status": "À valider",
   "detail": {
    "description": "Formulaire identique d'une règle à l'autre ; seuls nom et pourcentage varient.",
    "lostPerWeek": "6 min",
    "confidence": "Élevée",
    "observed": [
     "15 occurrences sur la semaine observée",
     "3 personnes concernées (E-commerce, Opérations)",
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
    "19 fois / sem.",
    "6 min / sem.",
    "Automatisable : partiel"
   ],
   "annualCost": 175,
   "status": "À valider",
   "detail": {
    "description": "Recherche simple, mais l'origine des identifiants n'est pas visible ; automatisable surtout si une liste est fournie.",
    "lostPerWeek": "6 min",
    "confidence": "Moyenne",
    "observed": [
     "19 occurrences sur la semaine observée",
     "3 personnes concernées (E-commerce, Opérations)",
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
    "15 fois / sem.",
    "6 min / sem.",
    "Automatisable : oui"
   ],
   "annualCost": 175,
   "status": "À valider",
   "detail": {
    "description": "Filtres répétables en vue enregistrée, mais critères inconnus.",
    "lostPerWeek": "6 min",
    "confidence": "Élevée",
    "observed": [
     "15 occurrences sur la semaine observée",
     "3 personnes concernées (E-commerce, Opérations)",
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
 "extraProblemsHoursSupplement": "48 min / sem.",
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
    "sub": "3 pers. · 2 h 37",
    "x": 14,
    "y": 30
   },
   {
    "id": "ops",
    "label": "Opérations",
    "sub": "3 pers. · 2 h 46",
    "x": 14,
    "y": 72
   },
   {
    "id": "catalogue",
    "label": "Catalogue",
    "sub": "128 min observées",
    "x": 80,
    "y": 8,
    "highlight": "goulot"
   },
   {
    "id": "commandes",
    "label": "Commandes",
    "sub": "78 min observées",
    "x": 80,
    "y": 25
   },
   {
    "id": "rapports",
    "label": "Rapports",
    "sub": "47 min observées",
    "x": 80,
    "y": 42
   },
   {
    "id": "avis",
    "label": "Avis",
    "sub": "30 min observées",
    "x": 80,
    "y": 59
   },
   {
    "id": "clients",
    "label": "Clients",
    "sub": "7 min observées",
    "x": 80,
    "y": 76
   },
   {
    "id": "marketing",
    "label": "Marketing",
    "sub": "15 min observées",
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
    "title": "3 h 42 par semaine, dans 14 tâches",
    "text": "Mêmes plages de dates ressaisies à plusieurs reprises (1/1/10-1/13/24 sur #57-#60, 1/1/23-1/13/24 sur #88-#91)",
    "link": "Voir le problème n° 01",
    "problemId": 1
   },
   {
    "tag": "Allers-retours",
    "title": "2 h 36 par semaine, dans 11 tâches",
    "text": "Va-et-vient entre la liste des commandes et la liste des clients (#54, #55)",
    "link": "Voir le problème n° 02",
    "problemId": 2
   },
   {
    "tag": "Passage de relais",
    "title": "6 min par semaine, dans 1 tâches",
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
    "value": "33",
    "sub": "par jour et par poste"
   },
   {
    "label": "Allers-retours entre écrans",
    "value": "978",
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
  "callout": "Le catalogue et les commandes concentrent l'essentiel du temps. Rapport ventes/produits sur une période revient 79 fois par semaine chez les 2 équipes.",
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
    "count": 110
   },
   {
    "path": "Accueil → Catalogue → Accueil",
    "count": 108
   },
   {
    "path": "Accueil → Rapports → Accueil",
    "count": 97
   },
   {
    "path": "Accueil → Avis → Accueil",
    "count": 91
   }
  ],
  "copyPasteTitle": "Allers-retours les plus fréquents",
  "copyPaste": [
   {
    "path": "Accueil → Catalogue",
    "count": 115
   },
   {
    "path": "Accueil → Commandes",
    "count": 113
   },
   {
    "path": "Accueil → Rapports",
    "count": 110
   },
   {
    "path": "Catalogue → Accueil",
    "count": 110
   }
  ]
 },
 "businessCase": {
  "stats": [
   {
    "label": "Coût annuel des tâches répétées observées",
    "value": "7 167 €",
    "sub": "4 h 06 par semaine, sur 19 tâches"
   },
   {
    "label": "Gain annuel récupérable",
    "value": "5 700 €",
    "sub": "80 % du temps de ces tâches",
    "accent": "good"
   },
   {
    "label": "Capacité libérée",
    "value": "0,09 ETP",
    "sub": "base 35 h / semaine"
   }
  ],
  "modules": [
   {
    "order": 1,
    "name": "Skill · Modifier le prix d'un produit ou d'une variante",
    "tag": "Gain rapide",
    "problems": "n° 03",
    "recovered": "33 min / sem.",
    "gain": 948,
    "delay": "1 sem."
   },
   {
    "order": 2,
    "name": "Skill · Consultation des commandes annulées",
    "tag": "Gain rapide",
    "problems": "n° 02",
    "recovered": "30 min / sem.",
    "gain": 876,
    "delay": "1 sem."
   },
   {
    "order": 3,
    "name": "Skill · Rapport ventes/produits sur une période",
    "tag": null,
    "problems": "n° 01",
    "recovered": "28 min / sem.",
    "gain": 816,
    "delay": "2 sem."
   },
   {
    "order": 4,
    "name": "Skill · Consulter les avis d'un produit depuis sa fiche",
    "tag": null,
    "problems": "n° 04",
    "recovered": "14 min / sem.",
    "gain": 408,
    "delay": "2 sem."
   },
   {
    "order": 5,
    "name": "Skill · Régénérer les variantes d'un produit configurable existant",
    "tag": null,
    "problems": "moins de 3 pers.",
    "recovered": "14 min / sem.",
    "gain": 408,
    "delay": "2 sem."
   }
  ],
  "modulesNote": "Tâches WONDERBREAD courtes (moins d'1 min 30) : les montants sont faibles, mais chaque chiffre vient d'une tâche observée et cliquable.",
  "beforeAfter": {
   "before": "4 h 06",
   "after": "50 min",
   "beforeH": 4.1,
   "afterH": 0.839,
   "note": "3 h 16 rendues chaque semaine aux 6 postes observés."
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
   "Base : 5 jours d'observation, 6 postes",
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
    "value": "12 h 30",
    "sub": "si les 5 skills sont déployées",
    "progress": 0
   },
   {
    "label": "Valeur annuelle visée",
    "value": "5 700 €",
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
    4.1,
    4.1
   ],
   "objective": 0.84,
   "objectiveLabel": "50 min",
   "annotations": []
  },
  "modules": [
   {
    "name": "Skill · Modifier le prix d'un produit ou d'une variante",
    "status": "Planifié"
   },
   {
    "name": "Skill · Consultation des commandes annulées",
    "status": "Planifié"
   },
   {
    "name": "Skill · Rapport ventes/produits sur une période",
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
    "title": "5,4 h observées sur 10 h demandées",
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
 }
};
