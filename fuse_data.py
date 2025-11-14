import pandas as pd
import os

# Create fused_data directory if it doesn't exist
os.makedirs('fused_data', exist_ok=True)

# Read the three CSV files
print("Reading CSV files...")
food_df = pd.read_csv('data/daily_food_nutrition_dataset_cleaned.csv')
diet_df = pd.read_csv('data/diet_recommendations_clean.csv')
gym_df = pd.read_csv('data/gym_members_exercise_tracking_clean.csv')

print(f"Food dataset: {food_df.shape}")
print(f"Diet dataset: {diet_df.shape}")
print(f"Gym dataset: {gym_df.shape}")

# Standardize column names for merging
# Convert height in gym_df from meters to cm to match diet_df
gym_df['height_cm'] = gym_df['height_m'] * 100

# Standardize gender column (capitalize first letter)
gym_df['gender'] = gym_df['gender'].str.capitalize()
diet_df['Gender'] = diet_df['Gender'].str.capitalize()

# Rename columns for consistency
gym_df_renamed = gym_df.rename(columns={
    'age': 'Age',
    'gender': 'Gender',
    'weight_kg': 'Weight_kg',
    'height_cm': 'Height_cm',
    'bmi': 'BMI'
})

diet_df_renamed = diet_df.rename(columns={
    'Age': 'Age',
    'Gender': 'Gender',
    'Weight_kg': 'Weight_kg',
    'Height_cm': 'Height_cm',
    'BMI_Calculated': 'BMI'
})

# Method 1: Merge diet and gym data on demographic attributes
print("\nMerging diet and gym data on demographic attributes...")
diet_gym_merged = pd.merge(
    diet_df_renamed,
    gym_df_renamed,
    on=['Age', 'Gender', 'Weight_kg', 'Height_cm', 'BMI'],
    how='outer',
    suffixes=('_diet', '_gym')
)

print(f"Merged diet-gym dataset: {diet_gym_merged.shape}")

# Method 2: Create a comprehensive user profile dataset
# First, let's create user profiles from each dataset

# From diet data - create user profiles
diet_profiles = diet_df_renamed[['Patient_ID', 'Age', 'Gender', 'Weight_kg', 'Height_cm', 
                                  'Disease_Type', 'Severity', 'Physical_Activity_Level',
                                  'Daily_Caloric_Intake', 'Cholesterol_mg/dL', 'Blood_Pressure_mmHg',
                                  'Glucose_mg/dL', 'Dietary_Restrictions', 'Allergies',
                                  'Preferred_Cuisine', 'Weekly_Exercise_Hours', 
                                  'Adherence_to_Diet_Plan', 'Diet_Recommendation', 'BMI']].copy()

# From gym data - create user profiles (we'll need to create IDs)
gym_profiles = gym_df_renamed[['Age', 'Gender', 'Weight_kg', 'Height_cm', 'BMI',
                                'max_bpm', 'avg_bpm', 'resting_bpm', 'session_duration_hours',
                                'calories_burned', 'workout_type', 'fat_percentage',
                                'water_intake_liters', 'workout_frequency_days_week',
                                'experience_level']].copy()
gym_profiles['Gym_ID'] = range(1, len(gym_profiles) + 1)
gym_profiles['Gym_ID'] = 'G' + gym_profiles['Gym_ID'].astype(str).str.zfill(4)

# Merge diet and gym profiles on demographic matching
print("\nCreating comprehensive user profiles...")
user_profiles = pd.merge(
    diet_profiles,
    gym_profiles,
    on=['Age', 'Gender', 'Weight_kg', 'Height_cm', 'BMI'],
    how='outer',
    suffixes=('_diet', '_gym')
)

# Method 3: Create a fully fused dataset with all information
# Aggregate food data by User_ID to get daily summaries
print("\nAggregating food data by user...")
food_aggregated = food_df.groupby('User_ID').agg({
    'Calories (kcal)': ['sum', 'mean', 'count'],
    'Protein (g)': 'sum',
    'Carbohydrates (g)': 'sum',
    'Fat (g)': 'sum',
    'Fiber (g)': 'sum',
    'Sugars (g)': 'sum',
    'Sodium (mg)': 'sum',
    'Cholesterol (mg)': 'sum',
    'Water_Intake (ml)': 'mean'
}).reset_index()

# Flatten column names
food_aggregated.columns = ['User_ID', 'Total_Calories', 'Avg_Calories', 'Meal_Count',
                           'Total_Protein', 'Total_Carbs', 'Total_Fat', 'Total_Fiber',
                           'Total_Sugars', 'Total_Sodium', 'Total_Cholesterol', 'Avg_Water_Intake']

# Create a comprehensive fused dataset
# Since User_ID, Patient_ID, and Gym_ID are different systems, we'll create a master dataset
print("\nCreating comprehensive fused dataset...")

# Create a master user list from all datasets
all_user_ids = set(food_df['User_ID'].unique())
all_patient_ids = set(diet_df['Patient_ID'].unique())
all_gym_ids = set(gym_profiles['Gym_ID'].unique())

# Create a comprehensive dataset by combining all information
# We'll use an outer join approach to preserve all records

# Start with food data aggregated
fused_df = food_aggregated.copy()

# Add diet information where User_ID might match Patient_ID (if they're numeric)
# For now, we'll create separate columns for each dataset's information
fused_df['User_ID_str'] = 'U' + fused_df['User_ID'].astype(str).str.zfill(4)

# Save different versions of the fused data
print("\nSaving fused datasets...")

# Version 1: Diet + Gym merged (demographic matching)
diet_gym_merged.to_csv('fused_data/diet_gym_merged.csv', index=False)
print("Saved: fused_data/diet_gym_merged.csv")

# Version 2: User profiles (diet + gym)
user_profiles.to_csv('fused_data/user_profiles_merged.csv', index=False)
print("Saved: fused_data/user_profiles_merged.csv")

# Version 3: Food aggregated data
food_aggregated.to_csv('fused_data/food_aggregated.csv', index=False)
print("Saved: fused_data/food_aggregated.csv")

# Version 4: Comprehensive fusion - combine all three with all columns
# Create a master fusion by concatenating all unique information
comprehensive_fusion = pd.concat([
    food_df.assign(Source='Food'),
    diet_df.assign(Source='Diet'),
    gym_df.assign(Source='Gym')
], ignore_index=True, sort=False)

comprehensive_fusion.to_csv('fused_data/comprehensive_fusion.csv', index=False)
print("Saved: fused_data/comprehensive_fusion.csv")

# Version 5: Smart fusion - try to match users across datasets
# Match based on demographic data where available
print("\nCreating smart fusion based on demographic matching...")

# Prepare food data with user demographics (we'll need to infer or match)
# For this, we'll create a mapping based on available data
food_by_user = food_df.groupby('User_ID').first().reset_index()

# Create a smart fusion by matching demographics
smart_fusion_list = []

for idx, diet_row in diet_df.iterrows():
    # Try to find matching gym record
    matching_gym = gym_df[
        (gym_df['age'] == diet_row['Age']) &
        (gym_df['gender'].str.capitalize() == diet_row['Gender']) &
        (abs(gym_df['weight_kg'] - diet_row['Weight_kg']) < 2) &
        (abs(gym_df['height_m'] * 100 - diet_row['Height_cm']) < 5)
    ]
    
    # Try to find matching food records (by User_ID if we can map it)
    # For now, we'll create a combined record
    combined_record = diet_row.to_dict()
    
    if not matching_gym.empty:
        gym_record = matching_gym.iloc[0]
        for col in gym_df.columns:
            if col not in ['age', 'gender', 'weight_kg', 'height_m', 'bmi']:
                combined_record[f'Gym_{col}'] = gym_record[col]
    
    smart_fusion_list.append(combined_record)

smart_fusion = pd.DataFrame(smart_fusion_list)
smart_fusion.to_csv('fused_data/smart_fusion.csv', index=False)
print("Saved: fused_data/smart_fusion.csv")

print("\n" + "="*50)
print("Fusion complete! Generated files:")
print("="*50)
print("1. diet_gym_merged.csv - Diet and Gym data merged on demographics")
print("2. user_profiles_merged.csv - User profiles from diet and gym")
print("3. food_aggregated.csv - Food data aggregated by user")
print("4. comprehensive_fusion.csv - All data concatenated with source labels")
print("5. smart_fusion.csv - Smart matching based on demographics")
print("="*50)

