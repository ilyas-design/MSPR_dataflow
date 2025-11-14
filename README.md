# MSPR Dataflow Project - HealthAI Coach

## Project Overview

This project is part of the MSPR (Mise en Situation Professionnelle Reconstituée) for the HealthAI Coach platform. The goal is to create a complete backend system that collects, cleans, transforms, and stores heterogeneous data from multiple sources.

## What Was Done

### Data Fusion

Three CSV datasets were successfully fused using Python:

1. **daily_food_nutrition_dataset_cleaned.csv** - Contains daily food intake and nutritional values
2. **diet_recommendations_clean.csv** - Contains health profiles and dietary recommendations
3. **gym_members_exercise_tracking_clean.csv** - Contains exercise tracking and fitness metrics

### Fusion Process

The fusion script (`fuse_data.py`) performs the following operations:

- Standardizes column names and data types across datasets
- Converts units (e.g., height from meters to centimeters)
- Matches records based on demographic attributes (age, gender, weight, height, BMI)
- Aggregates food data by user ID
- Creates multiple fusion strategies for different use cases

### Generated Files

The following fused datasets were created in the `fused_data/` folder:

1. **diet_gym_merged.csv** - Diet and Gym data merged on demographic attributes
2. **user_profiles_merged.csv** - Comprehensive user profiles combining diet and gym information
3. **food_aggregated.csv** - Food data aggregated by user with totals and averages
4. **comprehensive_fusion.csv** - All three datasets concatenated with source labels
5. **smart_fusion.csv** - Smart matching of diet records with gym records based on demographic similarity

## Data Sources

- **Daily Food & Nutrition Dataset** (Kaggle)
- **Diet Recommendations Dataset** (Kaggle)
- **Gym Members Exercise Dataset** (Kaggle)
