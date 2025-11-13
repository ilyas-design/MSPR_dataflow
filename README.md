# Nettoyage du Dataset Nutritionnel

## Description

Script de nettoyage pour le dataset `daily_food_nutrition_dataset.csv`.

## Transformations effectuées

1. **Suppression des lignes vides** - Supprime les lignes complètement vides

2. **Valeurs manquantes numériques** - Remplacement par la médiane
   - Colonnes : Calories, Protein, Carbohydrates, Fat, Fiber, Sugars, Sodium, Cholesterol, Water_Intake

3. **Valeurs manquantes textuelles** - Remplacement par la valeur la plus fréquente
   - Colonnes : Food_Item, Category, Meal_Type

4. **Dates manquantes** - Suppression des lignes sans date

5. **Conversion des types** - Date en datetime, colonnes numériques en float, User_ID en int

6. **Suppression des doublons** - Élimine les lignes identiques

7. **Valeurs négatives** - Remplace par 0 (impossible pour la nutrition)

8. **Nettoyage du texte** - Supprime les espaces, remplace les chaînes vides par 'Unknown'

9. **Cohérence logique** - Vérifie que Fibres ≤ Glucides et Sucres ≤ Glucides

## Utilisation

```bash
python clean_dataset.py
```

## Fichiers

- **Source** : `daily_food_nutrition_dataset.csv`
- **Script** : `clean_dataset.py`
- **Sortie** : `daily_food_nutrition_dataset_cleaned.csv`
