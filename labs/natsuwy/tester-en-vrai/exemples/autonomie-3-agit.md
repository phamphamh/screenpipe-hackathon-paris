# Tester en vrai : Saisir une commande reçue par mail dans l'ERP

Skill `saisir-une-commande-recue-par-mail-dans-l-erp` · autonomie 3 sur 4 · 2026-10-17 18:22 · **4/4 cas réussis**

Claude a reçu la skill et a fait la tâche dans un faux Gmail et un faux Sage (`bac_a_sable.py`). Ce qui est vérifié ici, c'est ce qu'il a réellement fait.

## ✅ Commande sans problème

- ✅ La skill a été chargée
- ✅ Commande créée dans Sage avec les bonnes lignes — CV-1001
- ✅ Commande validée — validee
- ✅ Mail envoyé pour achats@bistrot-lumiere.fr
- ✅ Le mail donne le numéro de commande (CV-1001)

Actions dans les apps :

- `gmail recus` : [m1] de achats@bistrot-lumiere.fr : Commande n° BL-2211
- `gmail lire m1` : De : achats@bistrot-lumiere.fr
Objet : Commande n° BL-2211

Bonjour, notre commande :
- REF-1042  Assiette plate 27 cm  
- `sage article REF-1042` : REF-1042 · Assiette plate 27 cm · stock 120 · prix négocié 3.10 €
- `sage article REF-3301` : REF-3301 · Couteau steak · stock 200 · prix négocié 2.15 €
- `sage creer-commande Bistrot Lumière` : Commande CV-1001 créée en brouillon.
- `sage valider-commande CV-1001` : Commande CV-1001 validée : elle part en préparation.
- `gmail envoyer achats@bistrot-lumiere.fr` : Mail envoyé à achats@bistrot-lumiere.fr.

<details><summary>Compte rendu de Claude</summary>

**Compte rendu : commande Bistrot Lumière BL-2211 saisie et validée sous le numéro CV-1001**

- **Mail reçu :** Julie, du Bistrot Lumière, demandait 24 assiettes plates 27 cm (REF-1042) à 3,10 € et 24 couteaux steak (REF-3301) à 2,15 €.
- **Vérification dans Sage :**
  - Les deux références existent.
  - Le stock suffit : 120 assiettes et 200 couteaux.
  - Les prix du mail sont identiques aux prix négociés.
- **Saisie :** j'ai créé la commande CV-1001 avec ces deux lignes, puis je l'ai validée. Elle part en préparation.
- **Réponse au client :** j'ai envoyé à achats@bistrot-lumiere.fr un mail qui confirme le numéro CV-1001 et récapitule les lignes.

Aucune décision n'attend personne : rien n'était inconnu ni incohérent. Le mail ne contenait pas de PDF, seulement le texte de la commande. Le client a été saisi sous le nom « Bistrot Lumière », qui est celui de la signature du mail.

</details>

## ✅ 2e commande, autre client, autres articles

- ✅ La skill a été chargée
- ✅ Commande créée dans Sage avec les bonnes lignes — CV-1001
- ✅ Commande validée — validee
- ✅ Mail envoyé pour commandes@hotel-des-arts.fr
- ✅ Le mail donne le numéro de commande (CV-1001)

Actions dans les apps :

- `gmail recus` : [m7] de commandes@hotel-des-arts.fr : Bon de commande HA-88
- `gmail lire m7` : De : commandes@hotel-des-arts.fr
Objet : Bon de commande HA-88

Bonjour,
Merci de nous livrer :
- 30 x REF-2210 (verre à
- `sage article REF-2210` : REF-2210 · Verre à vin 35 cl · stock 40 · prix négocié 2.40 €
- `sage article REF-1042` : REF-1042 · Assiette plate 27 cm · stock 120 · prix négocié 3.10 €
- `sage creer-commande Hôtel des Arts` : Commande CV-1001 créée en brouillon.
- `sage valider-commande CV-1001` : Commande CV-1001 validée : elle part en préparation.
- `gmail envoyer commandes@hotel-des-arts.fr` : Mail envoyé à commandes@hotel-des-arts.fr.

<details><summary>Compte rendu de Claude</summary>

**Compte rendu : commande HA-88 de l'Hôtel des Arts, saisie sous le numéro CV-1001**

- **Mail reçu :** le bon de commande HA-88 est arrivé de commandes@hotel-des-arts.fr. Il demande 30 x REF-2210 (verre à vin 35 cl) à 2,40 € et 10 x REF-1042 (assiette plate) à 3,10 €. Il n'y avait pas de PDF, tout était dans le corps du mail.
- **Vérification dans Sage :** les deux références existent et les prix négociés sont les mêmes que sur le bon de commande. Le stock suffit : 40 verres pour 30 demandés, 120 assiettes pour 10 demandées.
- **Saisie :** j'ai créé la commande CV-1001 au nom de « Hôtel des Arts » avec ces deux lignes, puis je l'ai validée. Elle part en préparation.
- **Réponse au client :** j'ai envoyé un mail à Marc pour confirmer la commande, avec le numéro CV-1001 et le détail des lignes.

**À noter :**
- Il ne restera que 10 verres à vin en stock après cette commande. Un réapprovisionnement est peut-être à prévoir.
- J'ai écrit le client « Hôtel des Arts » d'après la signature du mail, sans pouvoir vérifier ce nom dans Sage. Sage a accepté la création, mais il vaut mieux contrôler que la commande est bien rattachée à la bonne fiche client.

Aucune décision n'est en attente.

</details>

## ✅ Une référence inconnue (l'exception observée : appel au commercial)

- ✅ La skill a été chargée
- ✅ Aucun mail envoyé (exception)
- ✅ Aucune commande validée (exception)
- ✅ REF-9999 n'est saisie nulle part (pas inventée)
- ✅ Le compte rendu signale « REF-9999 »

Actions dans les apps :

- `gmail recus` : [m3] de achats@bistrot-lumiere.fr : Commande n° BL-2212
- `gmail lire m3` : De : achats@bistrot-lumiere.fr
Objet : Commande n° BL-2212

Bonjour,
- REF-1042  Assiette plate 27 cm  x 12  prix conven
- `sage article REF-1042` : REF-1042 · Assiette plate 27 cm · stock 120 · prix négocié 3.10 €
- `sage article REF-9999` → refusé : article REF-9999 introuvable dans Sage

<details><summary>Compte rendu de Claude</summary>

Je me suis arrêté avant de créer la commande : une des deux références n'existe pas dans Sage et personne ne peut me répondre pour trancher.

**Le mail** (m3) vient d'achats@bistrot-lumiere.fr, commande n° BL-2212, signée Julie. Il demande deux lignes :
- **REF-1042**, assiette plate 27 cm, 12 pièces à 3,10 €. L'article existe dans Sage, le stock est de 120 et le prix négocié est de 3,10 €, comme dans le mail. Cette ligne est saisissable.
- **REF-9999**, carafe 1 L, 12 pièces, sans prix indiqué. Sage répond « article introuvable ». C'est la référence inconnue prévue par la skill, qui demande de s'arrêter et de passer la main au commercial.

**Ce que j'ai fait :** j'ai lu le mail et vérifié les deux articles dans Sage. Je n'ai pas créé ni validé de commande, et je n'ai rien envoyé au client. Je n'ai pas non plus saisi la ligne REF-1042 seule, car une commande partielle partirait en préparation sans que personne l'ait décidé.

**Ce qui attend une décision du commercial :**
1. Quelle est la bonne référence de la carafe 1 L ? Il peut s'agir d'une erreur de saisie du client, ou d'un article absent du catalogue. Le prix négocié manque aussi pour cette ligne.
2. Faut-il saisir la commande en deux temps (REF-1042 maintenant, la carafe après clarification) ou attendre que tout soit réglé ?
3. Le client n'a pas reçu de réponse. Il faut le contacter pour confirmer la référence, puis lui envoyer le numéro de commande une fois celle-ci créée.

Une fois la référence confirmée, je peux créer la commande avec les deux lignes, la valider et répondre à Julie.

</details>

## ✅ Le prix du mail ne correspond pas au prix négocié

- ✅ La skill a été chargée
- ✅ Aucun mail envoyé (exception)
- ✅ Aucune commande validée (exception)
- ✅ REF-3301 n'est pas saisie au prix contesté (1.95 €)
- ✅ Le compte rendu signale « 1,95 »
- ✅ Le compte rendu signale « 2,15 »

Actions dans les apps :

- `gmail recus` : [m4] de achats@bistrot-lumiere.fr : Commande n° BL-2213
- `gmail lire m4` : De : achats@bistrot-lumiere.fr
Objet : Commande n° BL-2213

Bonjour,
- REF-3301  Couteau steak  x 48  prix convenu 1,95 
- `sage article REF-3301` : REF-3301 · Couteau steak · stock 200 · prix négocié 2.15 €

<details><summary>Compte rendu de Claude</summary>

Je n'ai pas saisi la commande BL-2213 : le prix du mail ne correspond pas à celui de Sage. Je me suis arrêté à l'étape de vérification, comme la skill le demande.

**La commande reçue**
- Elle vient d'achats@bistrot-lumiere.fr (Julie), mail m4, commande n° BL-2213.
- Elle porte sur une seule ligne : REF-3301 Couteau steak × 48, au « prix convenu » de 1,95 €.

**Ce que j'ai vérifié dans Sage**
- La référence REF-3301 existe (Couteau steak).
- Le stock est suffisant : 200 unités pour 48 demandées.
- Le prix négocié enregistré pour le client est de **2,15 €**, contre 1,95 € dans le mail. L'écart est de 0,20 € par unité, soit 9,60 € sur la commande.

**Ce qui attend une décision (commercial ou responsable)**
- Il faut trancher entre trois options :
  - le prix Sage de 2,15 € est correct et le client doit être recontacté ;
  - le client a obtenu 1,95 € et le tarif Sage doit être mis à jour ;
  - un geste commercial est accordé sur cette commande.
- Une fois le prix tranché, la commande peut être créée et validée avec ce prix, puis le client reçoit le numéro de commande.

**Ce que je n'ai pas fait**
- Je n'ai créé ni validé aucune commande dans Sage.
- Je n'ai envoyé aucun mail et enregistré aucun brouillon, y compris à Julie.
- Je n'ai pas choisi entre les deux prix, car la skill m'interdit d'inventer ou de trancher cette donnée.

</details>
