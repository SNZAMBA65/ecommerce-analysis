# 📊 Analyse de Performances et Optimisation d'un Site E-commerce

**Auteur :** Samir NZAMBA  
**Formation :** Directeur de Projet en Intelligence Artificielle - Année 1  
**École :** L'École Multimédia  
**Date :** Janvier 2025  
**Projet :** DPIA 1 2025 - Bloc 1 - Programmation data avec Python

---

## 🎯 Objectif du Projet

Analyser les données d'un site e-commerce, identifier les opportunités d'amélioration et proposer des solutions d'optimisation basées sur des A/B tests statistiquement validés.

Le projet démontre la capacité à :
- Exploiter et analyser des données volumineuses (2,7M d'événements)
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
│   ├── raw/                      # Données brutes (non versionnées)
│   │   ├── events.csv            # 2,7M événements utilisateurs
│   │   ├── category_tree.csv     # Arbre des catégories
│   │   ├── item_properties_part1.csv
│   │   └── item_properties_part2.csv
│   │
│   └── processed/                # Données traitées (non versionnées)
│       ├── events_clean.csv      # Données nettoyées et enrichies
│       ├── kpis_summary.csv      # Résumé des KPIs globaux
│       ├── daily_kpis.csv        # KPIs agrégés par jour
│       ├── hourly_analysis.csv   # Analyse par heure de la journée
│       ├── top_products.csv      # Top 500 produits
│       ├── events_for_tableau.csv # Échantillon pour Tableau (10%)
│       ├── ab_tests_results.csv  # Résultats des A/B tests
│       └── optimization_opportunities.csv
│
├── notebooks/
│   ├── 01_exploration.ipynb      # Exploration et nettoyage des données
│   ├── 02_analysis.ipynb         # Analyse approfondie et segmentation
│   └── 03_ab_testing.ipynb       # Simulation et analyse des A/B tests
│
├── scripts/
│   └── run_pipeline.py           # Automatisation du pipeline complet
│
├── reports/
│   └── figures/                  # Graphiques générés
│       ├── conversion_funnel.png
│       ├── event_distribution.png
│       ├── hourly_activity.png
│       ├── top_products.png
│       ├── user_segmentation.png
│       ├── cart_abandonment.png
│       ├── product_conversion_analysis.png
│       ├── ab_test_checkout.png
│       ├── ab_test_product_pages.png
│       ├── ab_test_popups.png
│       └── ab_tests_summary.png
│
├── tableau/
│   └── dashboard.twbx            # Dashboard Tableau interactif
│
├── presentation/
│   └── slides.pptx               # Présentation finale
│
├── .gitignore                    # Fichiers exclus du versionnement
├── requirements.txt              # Dépendances Python
└── README.md                     # Documentation du projet
```

---

## 🚀 Installation et Utilisation

### Prérequis

- Python 3.8+
- Tableau Public Desktop (gratuit)
- Git

### Installation
```bash
# Cloner le dépôt
git clone https://github.com/SNZAMBA65/ecommerce-analysis.git
cd ecommerce-analysis

# Installer les dépendances
pip install -r requirements.txt
```

### Exécution du Pipeline Automatisé

Le projet inclut un script d'automatisation qui exécute l'intégralité de l'analyse :
```bash
python scripts/run_pipeline.py
```

**Ce script exécute automatiquement :**
1. ✅ Exploration et nettoyage des données (`01_exploration.ipynb`)
2. ✅ Analyse approfondie et segmentation (`02_analysis.ipynb`)
3. ✅ Simulation des A/B tests (`03_ab_testing.ipynb`)

**Durée d'exécution :** ~2-3 minutes

**Résultats générés :**
- 📊 11 graphiques dans `reports/figures/`
- 📁 8 fichiers CSV dans `data/processed/`
- 🧪 Résultats A/B tests complets

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
- 2,756,101 événements utilisateurs
- 1,407,580 visiteurs uniques
- 235,061 produits différents
- Période : 137 jours (Mai - Septembre 2015)

**Types d'événements :**
- `view` : Consultation d'un produit (2,664,312 événements - 96.7%)
- `addtocart` : Ajout au panier (69,332 événements - 2.5%)
- `transaction` : Achat finalisé (22,457 événements - 0.8%)

---

## 🔍 Résultats Clés

### Métriques Principales

| Métrique | Valeur | Benchmark E-commerce |
|----------|--------|----------------------|
| **Taux de conversion global** | 0.84% | ✅ Normal (1-3%) |
| **Taux conversion panier** | 32.39% | ⚠️ Faible (40-50%) |
| **Taux abandon de panier** | 71.96% | 🔴 Élevé (60-70%) |
| **Visiteurs simples** | 97.2% | 🔴 Très élevé |

### Insights Comportementaux

📌 **Heures de pic d'activité :** 17h - 21h (soirée)  
📌 **Heures creuses :** 9h - 11h (matin)  
📌 **Acheteurs vs Abandons :** Les acheteurs consultent **3x plus** de produits (15 vs 5 vues)

### Opportunités Identifiées

1. **🔴 Abandon de panier (71.96%)**
   - Objectif : Réduire à 60%
   - Action : Simplifier le checkout, ajouter réassurance

2. **🟡 Conversion globale (0.84%)**
   - Objectif : Augmenter à 1.5%
   - Action : Améliorer pages produits, recommandations

3. **🟡 Engagement visiteurs (2.8% actifs)**
   - Objectif : Atteindre 10%
   - Action : Pop-ups, offres personnalisées

---

## 🧪 Résultats des A/B Tests

### Test #1 : Simplification du Checkout

**Hypothèse :** Réduire les étapes du checkout diminue les abandons

| Métrique | Groupe A (Contrôle) | Groupe B (Variante) | Amélioration |
|----------|---------------------|---------------------|--------------|
| Taux de conversion | 31.72% | 37.59% | **+18.49%** |
| P-value | - | 0.0000 | ✅ Significatif |
| Recommandation | - | **Déployer immédiatement** | - |

**Impact estimé :** +1,106 achats supplémentaires sur la période

---

### Test #2 : Amélioration des Pages Produits

**Hypothèse :** Meilleures images et descriptions augmentent les ajouts au panier

| Métrique | Groupe A (Contrôle) | Groupe B (Variante) | Amélioration |
|----------|---------------------|---------------------|--------------|
| Taux vue → panier | 2.48% | 4.12% | **+66.51%** |
| P-value | - | 0.0000 | ✅ Significatif |
| Recommandation | - | **Déployer sur top produits** | - |

**Impact estimé :** +16,227€ de revenus additionnels

---

### Test #3 : Pop-ups d'Engagement

**Hypothèse :** Pop-up avec offre augmente l'engagement des visiteurs passifs

| Métrique | Groupe A (Contrôle) | Groupe B (Variante) | Amélioration |
|----------|---------------------|---------------------|--------------|
| Taux d'engagement | 3.04% | 11.97% | **+293.47%** |
| P-value | - | 0.0000 | ✅ Significatif |
| Recommandation | - | **Tester sur segment ciblé** | - |

**Impact estimé :** +44,722 visiteurs engagés

---

## 🛠️ Technologies Utilisées

**Langages et Outils :**
- Python 3.13
- Jupyter Notebook
- Tableau Public Desktop
- Git / GitHub

**Bibliothèques Python :**
- `pandas` : Manipulation et analyse de données
- `numpy` : Calculs numériques
- `matplotlib` : Visualisations
- `seaborn` : Graphiques statistiques
- `scipy` : Tests statistiques (Chi-carré)

---

## 📈 Compétences Démontrées

### B-2 : Architecture de Données
✅ Élaboration d'un cahier des charges d'architecture de données  
✅ Intégration des contraintes techniques et normes  
✅ Réponse aux besoins spécifiques de l'entreprise

### C-3 : Automatisation des Flux
✅ Automatisation du pipeline de données  
✅ Optimisation des performances de l'infrastructure  
✅ Utilisation de la programmation pour l'automatisation

### C-5 : Contrôle Qualité
✅ Développement de procédures de contrôle qualité  
✅ Correction des erreurs dans les pipelines  
✅ Garantie de la qualité des données

---

## 📚 Documentation

- **Rapport complet :** `reports/rapport_final.pdf`
- **Présentation :** `presentation/slides.pptx`
- **Dashboard interactif :** `tableau/dashboard.twbx`
- **Code source commenté :** `notebooks/` et `scripts/`

---

## 🎓 Bonnes Pratiques Appliquées

✅ **Code propre :** Respect de PEP 8, commentaires détaillés  
✅ **Versionnement :** Commits réguliers et descriptifs sur GitHub  
✅ **Reproductibilité :** Pipeline automatisé en 1 commande  
✅ **Documentation :** README complet, docstrings, rapport détaillé  
✅ **Visualisations :** Graphiques clairs et professionnels  
✅ **Rigueur statistique :** Tests Chi-carré, p-values, intervalles de confiance

---

## 🔗 Liens

- **GitHub :** https://github.com/SNZAMBA65/ecommerce-analysis
- **Dataset :** https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset
- **Tableau Public :** *(lien à ajouter après publication)*

---

## 📧 Contact

**Samir NZAMBA**  
Étudiant - Directeur de Projet en Intelligence Artificielle  
L'École Multimédia  
[samirnzamba069@gmail.com]  
[GitHub](https://github.com/SNZAMBA65)
[Portfolio](https://samir-nzamba.fr)

---

**⭐ N'hésitez pas à explorer le code et les analyses !**