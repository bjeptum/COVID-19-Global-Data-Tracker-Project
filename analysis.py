import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load dataset
df = pd.read_csv("owid-covid-data.csv")

# Explore the dataset
print(df.columns)
print(df.head())
print(df.isnull().sum())

# Filter countries of interest
df = df[df['location'].isin(['Kenya', 'USA', 'India'])]

# Drop rows with missing critical values
df.dropna(subset=['total_cases', 'total_deaths'], inplace=True)

# Convert 'date' to datetime format
df['date'] = pd.to_datetime(df['date'])

# Handle missing numeric values (e.g., vaccinations)
df['total_vaccinations'].fillna(0, inplace=True)

# Exploratory Data Analysis (EDA)
# Total cases over time
plt.figure(figsize=(10, 6))
for country in ['Kenya', 'USA', 'India']:
    country_data = df[df['location'] == country]
    plt.plot(country_data['date'], country_data['total_cases'], label=country)
plt.title("Total Cases Over Time")
plt.xlabel("Date")
plt.ylabel("Total Cases")
plt.legend()
plt.show()

# Total deaths over time
plt.figure(figsize=(10, 6))
for country in ['Kenya', 'USA', 'India']:
    country_data = df[df['location'] == country]
    plt.plot(country_data['date'], country_data['total_deaths'], label=country)
plt.title("Total Deaths Over Time")
plt.xlabel("Date")
plt.ylabel("Total Deaths")
plt.legend()
plt.show()

# Daily new cases comparison
df['new_cases'] = df.groupby('location')['new_cases'].fillna(0)
plt.figure(figsize=(10, 6))
sns.barplot(x='location', y='new_cases', data=df)
plt.title("Daily New Cases Comparison")
plt.show()

# Calculate the death rate
df['death_rate'] = df['total_deaths'] / df['total_cases']
print(df[['location', 'death_rate']].head())

# Visualizing vaccination progress
# Cumulative vaccinations over time
plt.figure(figsize=(10, 6))
for country in ['Kenya', 'USA', 'India']:
    country_data = df[df['location'] == country]
    plt.plot(country_data['date'], country_data['total_vaccinations'], label=country)
plt.title("Cumulative Vaccinations Over Time")
plt.xlabel("Date")
plt.ylabel("Total Vaccinations")
plt.legend()
plt.show()

# Compare vaccinated population percentage
df['vaccinated_percentage'] = (df['total_vaccinations'] / df['population']) * 100
sns.barplot(x='location', y='vaccinated_percentage', data=df)
plt.title("Vaccinated Population Comparison")
plt.show()

# Optional: Build a choropleth map
latest_data = df[df['date'] == df['date'].max()][['location', 'total_cases', 'total_vaccinations']]
fig = px.choropleth(latest_data, locations="location", locationmode="country names",
                    color="total_cases", hover_name="location", color_continuous_scale="Viridis",
                    title="COVID-19 Total Cases by Country")
fig.show()