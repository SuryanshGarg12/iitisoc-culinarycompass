import streamlit as st
import pandas as pd


# Load the dataset
@st.cache_data
def load_data():
    return pd.read_csv('df_final.csv')



df = load_data()

st.title('Recipe Recommendation System')

# User input for ingredients
ingredients = st.text_input('Enter ingredients (comma-separated):')
ingredients_list = [ingredient.strip().lower() for ingredient in ingredients.split(',') if ingredient.strip()]

# User input for cuisine
cuisine = st.text_input('Enter cuisine (optional):')


# Function to display recipe details
def display_recipe_details(recipe):
    st.write(f"Time: {recipe['Time']}")
    st.write(f"Servings: {recipe['Servings']}")

    st.write("Ingredients:")
    ingredients = recipe['TranslatedIngredients'].split(',')
    for ingredient in ingredients:
        st.markdown(f"- {ingredient.strip()}")

    st.write("Instructions:")
    instructions = recipe['Instructions'].split('.')
    for instruction in instructions:
        if instruction.strip():
            st.markdown(f"- {instruction.strip()}")

    st.write(f"URL: {recipe['URL']}")


if st.button('Recommend Recipes'):
    if ingredients_list:
        # Filter recipes based on ingredients and cuisine
        mask = df['tags'].apply(lambda x: all(ingredient in str(x).lower() for ingredient in ingredients_list))
        if cuisine:
            mask &= df['tags'].str.contains(cuisine, case=False)

        recommended_recipes = df[mask]

        if not recommended_recipes.empty:
            st.subheader('Recommended Recipes:')
            for _, recipe in recommended_recipes.iterrows():
                with st.expander(recipe['RecipeName']):
                    display_recipe_details(recipe)
        else:
            st.write("No recipes found matching your criteria. Try different ingredients or cuisine.")
    else:
        st.write("Please enter at least one ingredient.")