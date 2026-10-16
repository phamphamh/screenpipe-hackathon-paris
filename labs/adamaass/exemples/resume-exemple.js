// Résumé INVENTÉ d'un salarié, au format de la brique B (labs/phamphamh/resume/exemple-resume.json),
// avec une tâche qui contient volontairement des infos sensibles pour tester la relecture.
window.RESUME = {
  "personne": "anonyme-exemple",
  "periode": { "debut": "2026-10-16T09:00:00+02:00", "fin": "2026-10-16T18:00:00+02:00" },
  "heures_captees": 6.8,
  "temps_par_app": [
    { "app": "Gmail", "minutes": 95 }, { "app": "HubSpot", "minutes": 80 }, { "app": "Google Sheets", "minutes": 70 },
    { "app": "Slack", "minutes": 60 }, { "app": "ChatGPT", "minutes": 35 }, { "app": "Spotify", "minutes": 40 }, { "app": "Doctolib", "minutes": 6 }
  ],
  "temps_par_categorie": [
    { "categorie": "Relances clients", "minutes": 120 }, { "categorie": "Reporting", "minutes": 90 },
    { "categorie": "Échanges internes", "minutes": 70 }, { "categorie": "Rédaction avec l'IA", "minutes": 35 }
  ],
  "usage_ia": [{ "outil": "ChatGPT", "minutes": 35, "usages": ["reformuler des mails", "résumer un appel"] }],
  "taches": [
    { "titre": "Relancer un client sans réponse", "frequence_par_semaine": 12, "duree_moyenne_min": 8, "apps": ["HubSpot", "Gmail"],
      "etapes": [
        { "type": "input", "texte": "Repérer les devis sans réponse depuis 7 jours", "app": "HubSpot", "statut": "observé" },
        { "type": "action", "texte": "Copier le nom et le montant du devis", "app": "HubSpot", "statut": "observé" },
        { "type": "output", "texte": "Envoyer un mail de relance à partir d'un modèle", "app": "Gmail", "statut": "observé" },
        { "type": "decision", "texte": "Si le client a répondu entre-temps, ne pas relancer", "app": "Gmail", "statut": "supposé" }
      ],
      "exceptions": ["client sans email → appel"], "goulots": [{ "type": "switching", "detail": "copier-coller HubSpot → Gmail à chaque relance" }],
      "automatisable": { "score": 80, "pourquoi": "étapes identiques à chaque fois, une seule décision simple" }, "confiance": 0.8,
      "preuves": [{ "debut": "2026-10-16T09:12:00+02:00", "fin": "2026-10-16T09:20:00+02:00", "app": "HubSpot" }] },
    { "titre": "Négocier la remise du devis Brasserie Kléber (18 400 €)", "frequence_par_semaine": 2, "duree_moyenne_min": 25, "apps": ["Gmail", "HubSpot"],
      "etapes": [
        { "type": "input", "texte": "Lire la contre-proposition de j.martin@brasserie-kleber.fr", "app": "Gmail", "statut": "observé" },
        { "type": "decision", "texte": "Accepter ou non une remise de 12 %", "app": "Gmail", "statut": "supposé" }
      ],
      "exceptions": [], "goulots": [{ "type": "waiting", "detail": "attente de l'accord du gérant" }],
      "automatisable": { "score": 20, "pourquoi": "négociation, jugement humain" }, "confiance": 0.5,
      "preuves": [{ "debut": "2026-10-16T11:30:00+02:00", "fin": "2026-10-16T11:55:00+02:00", "app": "Gmail" }] },
    { "titre": "Mettre à jour le tableau de suivi hebdo", "frequence_par_semaine": 1, "duree_moyenne_min": 55, "apps": ["HubSpot", "Google Sheets", "Slack"],
      "etapes": [
        { "type": "input", "texte": "Exporter les ventes de la semaine", "app": "HubSpot", "statut": "observé" },
        { "type": "action", "texte": "Coller et recalculer les totaux", "app": "Google Sheets", "statut": "observé" },
        { "type": "output", "texte": "Poster le résumé dans le canal équipe", "app": "Slack", "statut": "observé" }
      ],
      "exceptions": [], "goulots": [{ "type": "rework", "detail": "formules cassées après le collage, refaites à la main" }],
      "automatisable": { "score": 70, "pourquoi": "export et calcul répétitifs ; le commentaire reste humain" }, "confiance": 0.7,
      "preuves": [{ "debut": "2026-10-16T16:05:00+02:00", "fin": "2026-10-16T17:00:00+02:00", "app": "Google Sheets" }] }
  ],
  "limites": ["Données fictives, uniquement pour construire le site.", "Une seule journée : les fréquences par semaine sont extrapolées."],
  "tri_80_20": { "captures_regardees": 2400, "captures_gardees": 650, "part": 0.27 },
  "valide_par_la_personne": false
};
