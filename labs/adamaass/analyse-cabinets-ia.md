# Comment les cabinets français vendent la « transformation IA » — et où le Wrapped s'insère

Recherche du 16/10/2026 au soir (adamaass + Claude). Seul **Lonestone** a été lu en détail sur son propre site.
Les autres noms viennent de classements en ligne, souvent écrits par les cabinets eux-mêmes : à lire avec recul.

## 1. Le paysage (France)
| Type | Exemples | Pour qui |
|---|---|---|
| Stratégie et Big 4 | McKinsey (QuantumBlack), BCG X, Accenture, Deloitte, EY, KPMG, PwC | grands comptes, niveau comex |
| ESN et intégrateurs | Capgemini Invent (Quantmetry), Wavestone, Sia Partners, Onepoint, Devoteam, Octo, Publicis Sapient | grands comptes, mise en production |
| Spécialistes data et IA | Artefact, Ekimetrics, Eleven Strategy, Avisia, Aquila Data Enabler | ETI et grands comptes |
| Boutiques et agences IA | Lonestone, AI Partners, Spicy Advisory, Koïno, Palmer, Delos, Cartelis, Atheïa, Stema Partners, Pionarius, ISSKAR | PME et ETI — **notre cible** |

## 2. Les étapes d'une mission d'automatisation IA (Lonestone, page « Automatisation IA »)
1. **Échange de découverte** (gratuit) : processus, données, cas d'usage prometteurs.
2. **Devis et signature** (sous 48 h).
3. **Kick-off** : équipe, critères de succès.
4. **Shadowing terrain** : un consultant **observe les salariés au quotidien** pour repérer usages réels, irritants, habitudes.
5. **Cadrage** : choix des cas d'usage prioritaires et des solutions.
6. **Développement et intégration** : connecteurs (MCP, ERP, CRM, Slack, Teams), IA dans les outils existants.
7. **Déploiement et suivi** : temps gagné, taux d'erreur, satisfaction.
8. **Formation** pour l'adoption.

Ailleurs chez Lonestone, le même découpage sous forme d'offres : Explore (vision) → Shape (cadrage) → POC → Build → Run / Host / Scale → Learn.

## 3. Les prix et durées publiés (Lonestone)
| Offre | Durée | Prix |
|---|---|---|
| Audit (code, design, cyber) | 1 à 5 jours | 800 € HT / jour |
| Audit IA | 1 à 5 jours | 1 100 € HT / jour |
| POC | 2 à 4 semaines | à partir de 6 000 € |
| Sprint de développement | 2 semaines | à partir de 8 000 € |
| MVP | 2 à 3 mois | non publié |
| Formation « harness IA » | 1 jour + 3 demi-journées sur 6 semaines | non publié |

Éligible Crédit Impôt Innovation et aides Bpifrance (selon eux).

## 4. Leurs outils IA en interne
- **Claude et Claude Code** (cités sur la page Formation harness) ; les skills marchent aussi avec Codex, Pi.dev, Opencode.
- Méthode « harness » : règles + contexte métier + procédures écrites en langage courant (« skills ») + outils branchés.
- Ils disent avoir mis « des dizaines » de leurs procédures en skills (premier contact, comptes rendus, relances) et produit 8 propositions commerciales en 4 jours à 2 personnes.
- **Aucun outil nommé pour les audits** eux-mêmes.

## 5. Ce que ça veut dire pour le Wrapped
- **Les étapes 4 et 5 (shadowing + cadrage) sont exactement ce que le Wrapped automatise.** Aujourd'hui un consultant observe à la main, quelques jours, sur quelques personnes ; nous mesurons une semaine entière, sur toute l'équipe volontaire, avec une preuve par chiffre.
- **Ordre de grandeur à battre** : un audit IA de 5 jours chez Lonestone = 5 500 € HT, avant tout développement. C'est le prix de référence pour le pitch (question ouverte §10 du découpage).
- **Leur formation harness fait écrire les skills à la main.** Notre slide 9 (« Lancer l'automatisation n°1 ») génère le premier brouillon de skill depuis l'observation.
- **Deux positionnements possibles**, à trancher avec Louis samedi 18h :
  1. **outil pour les cabinets** (ils achètent le Wrapped pour remplacer le shadowing et vendre plus vite le POC) ;
  2. **concurrent direct** du shadowing pour les PME qui n'ont pas 5 000 € à mettre dans un audit.

## 6. À quoi ressemble un rapport d'audit IA (exemples publics)
Aucun cabinet français ne publie un vrai rapport client. Les exemples les plus proches :
- **Sunco, « Sample AI Readiness Report »** (rapport complet pour une entreprise fictive, Northgate Millwork) :
  score global (55 %, « grade B », « Moderate Risk ») → méthode (34 questions notées 0 à 3, normes ISO/IEC 42001) →
  tableau par domaine (stratégie, données, sécurité, infra, équipes, gouvernance) → « en place » (3) → « à travailler » (29),
  chaque lacune avec explication, « How Sunco closes this », référence et source. https://sunco.ca/Files/Assessment/AI_Readiness_Sample_Reportv2.html
- **Hyperstack (agence FR)** : 6 livrables systématiques — note de cartographie des processus, matrice des opportunités,
  périmètre V1 chiffré au jour, architecture cible, hypothèses et risques, note sécurité des données (RGPD, LLM).
  Flash 1-2 j (800-2 400 €), Cadrage 2-4 j (2 400-6 400 €), Complet 5-10 j (6 400-24 000 €), TJM 800 € HT.
  La cartographie se fait par **interviews et observation des écrans**. https://www.hyperstack.studio/blog/audit-ia-entreprise
- **Structure qui revient partout** : cartographie → liste de cas d'usage (5 à 80) → priorisation impact × faisabilité × risque
  (notes de 1 à 5) → feuille de route en 3 horizons (lancer / préparer / écarter) → note RGPD. Rapport de 15 à 25 pages.
- **Task mining (UiPath, Power Automate)** : carte du processus, temps par variante, usage des apps, activités candidates à
  l'automatisation ; UiPath exporte un squelette d'automatisation (PDD, XAML).

**Pour le Wrapped** : nos slides couvrent déjà cartographie (2), cas d'usage (3-4), goulots (5), priorisation (7) et inconnues (8).
Ce qui manque par rapport à un vrai rapport : la **faisabilité technique** (API disponibles), le **risque / RGPD par cas d'usage**
et la **feuille de route en 3 horizons**. Avantage du Wrapped : chaque chiffre est mesuré, pas déclaré en interview.

## 7. Non vérifié
- Les méthodes des autres cabinets (seul Lonestone a été lu).
- Si Lonestone utilise Claude Code pour ses audits (probable, pas confirmé).
- Les prix réels payés (les prix publiés sont « à partir de »).

Sources : lonestone.io (accueil, /solutions/automatisation-ia, /offres/audit, /solutions/formation-harness, /realisations) ; classements Lonestone, Cartelis, Hashtech, AI Partners, Spicy Advisory, Koïno, intelligence-artificielle.com.
