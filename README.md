# Analyse de performances et optimisation d'un site e-commerce

**Auteur :** Samir NZAMBA  
**Formation :** Directeur de Projet en Intelligence Artificielle - Année 1  
**École :** L'École Multimédia  
**Date :** Janvier 2025  
**Projet :** DPIA 1 2025 - Bloc 1 - Programmation data avec Python

Dashboard en ligne : https://ecommerce-analyse.streamlit.app/

---

## Objectif du projet

Analyser les données d'un site e-commerce (2,7M d'événements), identifier les opportunités d'amélioration et proposer des solutions d'optimisation basées sur des A/B tests statistiquement validés.

Le projet démontre la capacité à :
- Exploiter et analyser des données volumineuses
- Créer des visualisations pertinentes et un tableau de bord interactif
- Concevoir et simuler des A/B tests pour optimiser les performances
- Automatiser un pipeline complet d'analyse de données
- Documenter et présenter des résultats de manière professionnelle

---

## 📁 Structure du Projet
```
ecommerce-analysis/
│
├── data/
│   ├── raw/                          # Données brutes (non versionnées)
│   │   ├── events.csv                # 2,756,101 événements utilisateurs
│   │   ├── category_tree.csv         # 1,669 catégories
│   │   ├── item_properties_part1.csv # 11M propriétés produits
│   │   └── item_properties_part2.csv # 9M propriétés produits
│   │
│   └── processed/                    # Données traitées
│       ├── kpis_summary.csv          # Résumé des KPIs globaux (versionné)
│       ├── daily_kpis.csv            # KPIs agrégés par jour (versionné)
│       ├── hourly_analysis.csv       # Analyse par heure (versionné)
│       ├── top_products.csv          # Top 500 produits (versionné)
│       ├── ab_tests_results.csv      # Résultats des 3 A/B tests (versionné)
│       ├── events_for_tableau.csv    # Échantillon 10% pour dashboard (versionné)
│       ├── events_clean.csv          # Données nettoyées (non versionné - trop volumineux)
│       └── optimization_opportunities.csv  # Opportunités (non versionné)
│
├── notebooks/
│   ├── 01_exploration.ipynb          # Exploration et nettoyage
│   ├── 02_analysis.ipynb             # Analyse approfondie et segmentation
│   └── 03_ab_testing.ipynb           # Simulation et analyse A/B tests
│
├── scripts/
│   └── run_pipeline.py               # Pipeline d'automatisation complet
│
├── streamlit_dashboard.py            # Dashboard interactif Streamlit
│
├── reports/
│   ├── figures/                      # Graphiques générés (11 PNG)
│   │   ├── conversion_funnel.png
│   │   ├── event_distribution.png
│   │   ├── hourly_activity.png
│   │   ├── top_products.png
│   │   ├── user_segmentation.png
│   │   ├── cart_abandonment.png
│   │   ├── product_conversion_analysis.png
│   │   ├── ab_test_checkout.png
│   │   ├── ab_test_product_pages.png
│   │   ├── ab_test_popups.png
│   │   └── ab_tests_summary.png
│   │
│   ├── dashboard_screenshots/        # Captures d'écran dashboard
│   ├── rapport_final.pdf             # Rapport détaillé
│   └── presentation.pptx             # Présentation finale
│
├── .gitignore                        # Exclusions Git
├── requirements.txt                  # Dépendances Python
└── README.md                         # Documentation du projet
```

---

## Accès au dashboard

### Version en ligne (recommandé)

Le dashboard est déployé et accessible directement en ligne :

https://ecommerce-analyse.streamlit.app/

Avantages :
- Aucune installation nécessaire
- Accès instantané depuis n'importe quel navigateur
- Données pré-chargées et optimisées
- Mise à jour automatique à chaque commit

---

### 💻 Version Locale

Si vous souhaitez exécuter le dashboard localement :

#### Prérequis
- Python 3.8+
- Git

#### Installation
```bash
# Cloner le dépôt
git clone https://github.com/SNZAMBA65/ecommerce-analysis.git
cd ecommerce-analysis

# Créer un environnement virtuel (recommandé)
python -m venv .venv
source .venv/bin/activate  # Sur Linux/Mac
.venv\Scripts\activate     # Sur Windows

# Installer les dépendances
pip install -r requirements.txt
```

#### Lancement
```bash
streamlit run streamlit_dashboard.py
```

Le dashboard s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

---

## Pipeline d'analyse

### Exécution automatique

Le projet inclut un script d'automatisation qui exécute l'intégralité de l'analyse en une seule commande :
```bash
python scripts/run_pipeline.py
```

Ce script exécute automatiquement :
1. Exploration et nettoyage des données (`01_exploration.ipynb`)
2. Analyse approfondie et segmentation (`02_analysis.ipynb`)
3. Simulation des A/B tests (`03_ab_testing.ipynb`)

Durée d'exécution : ~2-3 minutes

Résultats générés :
- 11 graphiques dans `reports/figures/`
- 8 fichiers CSV dans `data/processed/`
- Résultats A/B tests complets

### Exécution Manuelle des Notebooks

Vous pouvez aussi exécuter chaque notebook individuellement :
```bash
# Lancer Jupyter
jupyter notebook

# Ouvrir et exécuter dans l'ordre :
# 1. notebooks/01_exploration.ipynb
# 2. notebooks/02_analysis.ipynb
# 3. notebooks/03_ab_testing.ipynb
```

---

## 📊 Dataset

**Source :** [Retail Rocket E-commerce Dataset](https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset)

**Description :**
- **2,756,101** événements utilisateurs
- **1,407,580** visiteurs uniques
- **235,061** produits différents
- **Période :** 137 jours (3 mai - 18 septembre 2015)

**Types d'événements :**
- `view` : Consultation d'un produit (2,664,312 événements - 96.7%)
- `addtocart` : Ajout au panier (69,332 événements - 2.5%)
- `transaction` : Achat finalisé (22,457 événements - 0.8%)

---

## Résultats clés

### Métriques principales

| Métrique | Valeur | Benchmark e-commerce |
|----------|--------|----------------------|
| **Taux de conversion global** | 0.84% | Normal (1-3%) |
| **Taux conversion panier → achat** | 32.39% | Faible (40-50%) |
| **Taux abandon de panier** | 67.61% | Élevé (60-70%) |
| **Visiteurs actifs** | 2.8% | Très faible |

### Observations principales

Temporalité :
- Heures de pic : 17h - 21h (soirée)
- Heures creuses : 9h - 11h (matin)

Segmentation :
- Clients : 0.8% des visiteurs (11,719 utilisateurs)
- Panier abandonné : 1.9% des visiteurs (27,146 utilisateurs)
- Visiteurs passifs : 97.3% des visiteurs (1,368,715 utilisateurs)

Comportement :
- Les clients consultent en moyenne 3x plus de produits que les visiteurs qui abandonnent (15 vs 5 vues)
- Les clients ajoutent en moyenne 2.3 produits au panier

### Opportunités identifiées

| Opportunité | État Actuel | Objectif | Impact Estimé |
|-------------|-------------|----------|---------------|
| **Abandon de panier** | 67.61% | 60% | +1,106 achats |
| **Conversion globale** | 0.84% | 1.5% | +16,227€ |
| **Engagement visiteurs** | 2.8% | 10% | +22,361€ |

---

## Résultats des A/B tests

### Test #1 : Simplification du checkout

**Hypothèse :** Réduire le nombre d'étapes du processus de checkout diminue les abandons de panier.

| Métrique | Groupe A (Contrôle) | Groupe B (Variante) | Amélioration |
|----------|---------------------|---------------------|--------------|
| **Taux de conversion** | 31.72% | 37.59% | **+18.49%** |
| **Taille échantillon** | 18,861 utilisateurs | 18,861 utilisateurs | - |
| **P-value** | - | 0.0000 | Hautement significatif |

Impact estimé : +1,106 achats supplémentaires (~55,300€ de CA additionnel)

Recommandation : Déployer sur 100% du trafic

---

### Test #2 : Amélioration des pages produits

**Hypothèse :** Meilleures images, descriptions et avis clients augmentent les ajouts au panier.

| Métrique | Groupe A (Contrôle) | Groupe B (Variante) | Amélioration |
|----------|---------------------|---------------------|--------------|
| **Taux vue → panier** | 2.48% | 4.12% | **+66.51%** |
| **Échantillon** | 50 produits (43,999 vues) | 50 produits (50,737 vues) | - |
| **P-value** | - | 0.0000 | Hautement significatif |

Impact estimé : +16,227€ de revenus additionnels

Recommandation : Déployer sur les top 100 produits en priorité

---

### Test #3 : Pop-ups d'engagement

**Hypothèse :** Pop-up avec offre promotionnelle augmente l'engagement des visiteurs passifs.

| Métrique | Groupe A (Contrôle) | Groupe B (Variante) | Amélioration |
|----------|---------------------|---------------------|--------------|
| **Taux d'engagement** | 3.04% | 11.97% | **+293.47%** |
| **Échantillon** | 500,780 visiteurs | 500,780 visiteurs | - |
| **P-value** | - | 0.0000 | Hautement significatif |

Impact estimé : +44,722 visiteurs engagés (~22,361€ de CA potentiel)

Recommandation : Tester sur segment visiteurs nouveaux avant déploiement global

---

### Impact global des A/B tests

Revenus additionnels estimés : ~93,888€ sur 137 jours  
Potentiel annuel estimé : ~250,000€  
ROI projeté : Si coût de déploiement = 10,000€ → ROI de 840%

---

## 🛠️ Technologies Utilisées

### Langages et Outils
- **Python 3.13**
- **Jupyter Notebook**
- **Streamlit** (Dashboard interactif)
- **Git / GitHub**

### Bibliothèques Python
```python
pandas==2.3.3          # Manipulation de données
numpy==2.4.1           # Calculs numériques
matplotlib==3.10.8     # Visualisations
seaborn==0.13.2        # Graphiques statistiques
scipy==1.17.0          # Tests statistiques (Chi-carré)
plotly==6.5.2          # Graphiques interactifs
streamlit>=1.30.0      # Dashboard web
altair<5               # Visualisations (compatible Streamlit)
jupyter==1.1.1         # Notebooks interactifs
openpyxl==3.1.5        # Manipulation Excel
```

---

## Compétences démontrées

### B-2 : Architecture de données
- Élaboration d'un pipeline de traitement de données  
- Intégration des contraintes techniques (volumétrie, performance)  
- Architecture adaptée aux besoins métier (e-commerce)

### C-3 : Automatisation des flux
- Pipeline automatisé (`run_pipeline.py`) exécutable en 1 commande  
- Optimisation des performances (échantillonnage intelligent)  
- Scripts réutilisables et modulaires

### C-5 : Contrôle qualité
- Procédures de nettoyage et validation des données  
- Gestion des valeurs manquantes et aberrantes  
- Tests statistiques pour garantir la fiabilité des résultats

---

## Bonnes pratiques appliquées

- Code propre : Respect de PEP 8, commentaires détaillés  
- Versionnement : Commits réguliers et descriptifs sur GitHub  
- Reproductibilité : Pipeline automatisé en 1 commande  
- Documentation : README complet, docstrings, rapport détaillé  
- Visualisations : Graphiques clairs, professionnels et interactifs  
- Rigueur statistique : Tests Chi-carré, p-values, significativité  
- Déploiement : Dashboard accessible en ligne 24/7

---

## 📝 Notes de Déploiement

### Gestion des fichiers volumineux

**Important :** Certains fichiers de données dépassent la limite GitHub de 100 MB :
- `data/processed/events_clean.csv` (173 MB) - **Non versionné**
- `data/processed/optimization_opportunities.csv` - **Non versionné**

Solution adoptée :
- Les fichiers essentiels au dashboard (<100 MB) sont versionnés sur GitHub
- Les fichiers volumineux sont exclus via `.gitignore`
- Le dashboard en ligne utilise uniquement les fichiers versionnés
- Pour l'analyse locale complète, exécutez le pipeline pour régénérer tous les fichiers

### Compatibilité Streamlit Cloud

Le `requirements.txt` est optimisé pour le déploiement Streamlit Cloud :
- `streamlit>=1.30.0` : Version récente et stable
- `altair<5` : Compatibilité garantie avec Streamlit

---

## Liens

- Dashboard en ligne : https://ecommerce-analyse.streamlit.app/
- GitHub : https://github.com/SNZAMBA65/ecommerce-analysis
- Dataset : https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset

---

## Contact

**Samir NZAMBA**  
Étudiant - Directeur de Projet en Intelligence Artificielle  
L'École Multimédia - Promotion 2025  

GitHub : https://github.com/SNZAMBA65

---

## Licence

Ce projet est réalisé dans le cadre d'un projet académique à L'École Multimédia.  
Les données sont issues du dataset public Retail Rocket (Kaggle).

---

N'hésitez pas à explorer le dashboard en ligne : https://ecommerce-analyse.streamlit.app/

*Dernière mise à jour : 31 janvier 2025*