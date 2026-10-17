---
name: saisir-une-commande-recue-par-mail-dans-l-erp
description: Saisir une commande reçue par mail dans l'ERP. À utiliser quand quelqu'un chez Maison Corvo doit faire cette tâche (Gmail, Sage).
---

# Saisir une commande reçue par mail dans l'ERP

Observé chez Maison Corvo pendant la campagne Wrapped : environ 31 fois par semaine, 11 min à chaque fois, dans Gmail, Sage.
Noms donnés par les équipes : Saisir une commande reçue par mail dans l'ERP ; Saisie des commandes mail dans Sage.

## Étapes
1. **Entrée** (Gmail) : Ouvrir le bon de commande PDF reçu par mail
2. **Action** (Sage) : Créer la commande et saisir les lignes article par article
3. **Vérification** (Sage) : Vérifier le stock et le prix négocié
4. **Sortie** (Gmail) : Répondre au client avec le numéro de commande

## Déclencheurs
- Dès qu'un bon de commande PDF arrive par mail → démarrer la tâche (la skill) sans attendre (connecteur Gmail → Sage).
- Dès que référence inconnue → appel au commercial (rien d'automatique) — à prévenir : commercial.
- Dès que la tâche est finie → Répondre au client avec le numéro de commande (API Gmail) — à prévenir : client.

## Exceptions
- référence inconnue → appel au commercial

## Ce qui ralentit aujourd'hui
- recopier chaque ligne du PDF dans Sage
- erreurs de référence corrigées après coup

## Garde-fous
- Ne rien envoyer à l'extérieur (mail, message, commande) sans la confirmation d'un humain.
- En cas d'exception non listée ci-dessus, s'arrêter et demander.
