# Dès que… — les déclencheurs (labs/phamphamh/demo/resumes)

9 tâches relues, 22 déclencheurs détectés.
(tâches et chiffres de la fusion officielle)

## Saisir une commande reçue par mail dans l'ERP
*31×/sem · 11 min · chez moins de 3 personnes · apps : Gmail, Sage*

| Dès que… | Lancer | Voie | Partager | Preuve |
|---|---|---|---|---|
| un bon de commande PDF arrive par mail | démarrer la tâche (la skill) sans attendre | connecteur Gmail → Sage (API Gmail, API Sage) |  | « Ouvrir le bon de commande PDF reçu par mail » — Gmail |
| référence inconnue | appel au commercial (rien d'automatique) | notification | appel au commercial → commercial | « référence inconnue → appel au commercial » |
| la tâche est finie | Répondre au client avec le numéro de commande | API Gmail | Répondre au client avec le numéro de commande → client | « Répondre au client avec le numéro de commande » — Gmail |

## Relancer les devis sans réponse
*29×/sem · 7 min · chez 3 personnes · apps : HubSpot, Gmail*

| Dès que… | Lancer | Voie | Partager | Preuve |
|---|---|---|---|---|
| le balayage tourne — devis envoyés il y a plus de 7 jours | démarrer la tâche (la skill) sans attendre | connecteur HubSpot → Gmail (API HubSpot, API Gmail) |  | « Filtrer les devis envoyés il y a plus de 7 jours » — HubSpot |
| client sans email | appel (rien d'automatique) | notification | appel → client | « client sans email → appel » |
| la tâche est finie | Envoyer le mail de relance depuis un modèle | API Gmail | Envoyer le mail de relance depuis un modèle → à définir | « Envoyer le mail de relance depuis un modèle » — Gmail |

## Traiter une demande de retour produit
*12×/sem · 15 min · chez moins de 3 personnes · apps : Zendesk, Sage, Gmail*

| Dès que… | Lancer | Voie | Partager | Preuve |
|---|---|---|---|---|
| un ticket et les photos du client arrivent | démarrer la tâche (la skill) sans attendre | connecteur Zendesk → Sage (API Zendesk, API Sage) |  | « Lire le ticket et les photos du client » — Zendesk |
| produit hors garantie | devis de réparation (rien d'automatique) | notification | devis de réparation → à définir | « produit hors garantie → devis de réparation » |
| la tâche est finie | Créer le bon de retour et prévenir le client | API Gmail | Créer le bon de retour et prévenir le client → client | « Créer le bon de retour et prévenir le client » — Gmail |

## Créer un devis à partir d'une demande mail
*8×/sem · 18 min · chez moins de 3 personnes · apps : Gmail, Sage, Excel*

| Dès que… | Lancer | Voie | Partager | Preuve |
|---|---|---|---|---|
| une demande du client arrive | démarrer la tâche (la skill) sans attendre | connecteur Gmail → Excel (API Gmail, fichier local) |  | « Lire la demande du client » — Gmail |
| demande floue | appel (rien d'automatique) | notification | appel → à définir | « demande floue → appel » |
| la tâche est finie | Créer le devis dans Sage et l'envoyer | API Sage | Créer le devis dans Sage et l'envoyer → à définir | « Créer le devis dans Sage et l'envoyer » — Sage |

## Répondre aux demandes de délai de livraison
*35×/sem · 6 min · chez moins de 3 personnes · apps : Gmail, Sage, Site transporteur, Zendesk*

| Dès que… | Lancer | Voie | Partager | Preuve |
|---|---|---|---|---|
| une demande du client arrive | démarrer la tâche (la skill) sans attendre | connecteur Gmail → Sage (API Gmail, API Sage) |  | « Lire la demande du client » — Gmail |
| la tâche est finie | Répondre avec la date estimée | API Gmail | Répondre avec la date estimée → à définir | « Répondre avec la date estimée » — Gmail |

## Préparer le reporting hebdo des ventes
*4×/sem · 49 min · chez 4 personnes · apps : HubSpot, Excel, Gmail, Slack, Sage, Pennylane*

| Dès que… | Lancer | Voie | Partager | Preuve |
|---|---|---|---|---|
| le balayage tourne — chiffres de la semaine | démarrer la tâche (la skill) sans attendre | connecteur HubSpot → Excel (API HubSpot, fichier local) |  | « Exporter les chiffres de la semaine » — HubSpot |
| la tâche est finie | Envoyer le tableau à la direction | API Gmail | Envoyer le tableau à la direction → direction | « Envoyer le tableau à la direction » — Gmail |

## Rapprocher les factures fournisseurs des bons de commande
*30×/sem · 6 min · chez moins de 3 personnes · apps : Pennylane, Sage*

| Dès que… | Lancer | Voie | Partager | Preuve |
|---|---|---|---|---|
| une facture fournisseur arrive | démarrer la tâche (la skill) sans attendre | connecteur Pennylane → Sage (API Pennylane, API Sage) |  | « Ouvrir la facture fournisseur » — Pennylane |
| écart de prix | mail au fournisseur (rien d'automatique) | notification | mail au fournisseur → fournisseur | « écart de prix → mail au fournisseur » |

## Chercher la fiche technique d'un produit
*37×/sem · 4 min · chez 3 personnes · apps : Google Drive, Google Chrome*

| Dès que… | Lancer | Voie | Partager | Preuve |
|---|---|---|---|---|
| une question client sur un produit arrive | démarrer la tâche (la skill) sans attendre | connecteur Gmail → Google Drive (API Gmail, API Google Drive) |  | « Recevoir une question client sur un produit » — Gmail |
| la tâche est finie | Envoyer la fiche ou la réponse au client | API Gmail | Envoyer la fiche ou la réponse au client → client | « Envoyer la fiche ou la réponse au client » — Gmail |

## Relancer les factures impayées
*10×/sem · 10 min · chez moins de 3 personnes · apps : Pennylane, Gmail*

| Dès que… | Lancer | Voie | Partager | Preuve |
|---|---|---|---|---|
| le balayage tourne — factures échues | démarrer la tâche (la skill) sans attendre | connecteur Pennylane → Gmail (API Pennylane, API Gmail) |  | « Lister les factures échues » — Pennylane |
| la tâche est finie | Envoyer la relance | API Gmail | Envoyer la relance → à définir | « Envoyer la relance » — Gmail |

*Formulations par règles à partir des étapes relues ; chaque ligne garde sa preuve. Tâches et chiffres : fusion officielle.*
