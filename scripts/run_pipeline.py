"""
Pipeline d'automatisation complète - Analyse E-commerce
Auteur: Samir Zamba
Date: Janvier 2025

Ce script automatise l'intégralité du pipeline d'analyse :
1. Traitement des données brutes
2. Génération des visualisations
3. Exécution des A/B tests
4. Export des résultats pour Tableau

Usage:
    python scripts/run_pipeline.py
"""

import subprocess
import os
from datetime import datetime

def log(message):
    """Affiche un message avec timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def run_notebook(notebook_path):
    """Exécute un notebook Jupyter"""
    log(f"Exécution de {notebook_path}...")
    result = subprocess.run(
        ['jupyter', 'nbconvert', '--to', 'notebook', '--execute', 
         '--inplace', notebook_path],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        log(f"✅ {notebook_path} terminé")
    else:
        log(f"❌ Erreur dans {notebook_path}")
        print(result.stderr)
        return False
    return True

def main():
    """Fonction principale - Exécute le pipeline complet"""
    
    print("=" * 70)
    print("🚀 PIPELINE D'AUTOMATISATION - ANALYSE E-COMMERCE")
    print("=" * 70)
    
    # Vérifier que nous sommes dans le bon dossier
    if not os.path.exists('notebooks'):
        print("❌ Erreur: Dossier 'notebooks' introuvable")
        print("   Exécutez ce script depuis la racine du projet")
        return
    
    # Liste des notebooks à exécuter dans l'ordre
    notebooks = [
        'notebooks/01_exploration.ipynb',
        'notebooks/02_analysis.ipynb',
        'notebooks/03_ab_testing.ipynb'
    ]
    
    log("Début du pipeline d'analyse automatisé")
    
    # Exécuter chaque notebook
    for i, notebook in enumerate(notebooks, 1):
        print(f"\n{'='*70}")
        print(f"ÉTAPE {i}/{len(notebooks)}: {os.path.basename(notebook)}")
        print('='*70)
        
        if not run_notebook(notebook):
            log("❌ Pipeline interrompu suite à une erreur")
            return
    
    # Résumé final
    print("\n" + "="*70)
    print("✅ PIPELINE TERMINÉ AVEC SUCCÈS")
    print("="*70)
    
    log("Fichiers générés :")
    log("  📊 Graphiques dans reports/figures/")
    log("  📁 Données traitées dans data/processed/")
    log("  🧪 Résultats A/B tests sauvegardés")
    
    print("\n💡 Prochaines étapes :")
    print("  1. Consultez les graphiques dans reports/figures/")
    print("  2. Importez les CSV dans Tableau depuis data/processed/")
    print("  3. Consultez le résumé dans data/processed/ab_tests_results.csv")

if __name__ == "__main__":
    main()