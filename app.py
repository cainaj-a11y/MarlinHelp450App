import streamlit as st
import pandas as pd
import plotly.express as px
## from google.colab import drive

# Mount Google Drive to access CSV files
## drive.mount('/content/drive')

IPUMS_csv_file_path = 'IPUMS.csv'
OCC_csv_file_path = 'OccupationCodes.csv'

try:
    df = pd.read_csv(IPUMS_csv_file_path)
    OCC_df = pd.read_csv(OCC_csv_file_path)

    # Data Cleaning and Preparation steps (replicated from earlier notebook cells)
    df = df.dropna()
    df['OCC'] = df['OCC'].astype(str)
    df = pd.merge(df, OCC_df, left_on='OCC', right_on='OCC Code', how='left')
    df = df[(df['UHRSWORKT'] >= 30) & (df['UHRSWORKT'] <= 60)]
    df = df[(df['INCWAGE'] >= 10000) & (df['INCWAGE'] <= 200000)]
    df = df[df['WKSWORK1'] > 0]
    df = df.drop(columns=['Unnamed: 3', 'OCC Code'])
    df = df.dropna(subset=['Occupation Title'])

    # Feature Engineering (replicated from earlier notebook cells)
    median_income = df['INCWAGE'].median()
    df['HighEarner'] = (df['INCWAGE'] > median_income).astype(int)
    df["HourlyEfficiency"] = df["INCWAGE"] / (df["WKSWORK1"] * df["UHRSWORKT"])
    df["EdWorkIntensity"] = df["EDUC"] * df["UHRSWORKT"]

except FileNotFoundError:
    st.error("Error: Required CSV files not found. Please ensure 'IPUMS.csv' and 'OccupationCodes.csv' are in your Google Drive.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred during data loading or preprocessing: {e}")
    st.stop()

st.title("Workforce Dashboard")

# Bar chart: Workforce Distribution
horizontal_bar_chart = px.bar(df['Major Category'].value_counts().reset_index(),
                    x='count',
                    y='Major Category',
                    orientation='h',
                    title='Workforce Distribution: Number of Employees per Sector',
                    labels={'count': 'Number of Employees', 'Major Category': 'Job Sector'},
                    color='Major Category')
horizontal_bar_chart.update_layout(showlegend=False)
st.plotly_chart(horizontal_bar_chart)

# Histogram: Distribution of Weekly Hours Worked
histogram = px.histogram(df,
                    x='UHRSWORKT',
                    title='Workplace Culture: Distribution of Weekly Hours Worked',
                    labels={'UHRSWORKT': 'Hours Worked Per Week', 'count': 'Number of Employees', 'y': 'Number of Employees'},
                    color_discrete_sequence=['#1f77b4'])
histogram.update_layout(yaxis_title="Number of Employees")
st.plotly_chart(histogram)

st.dataframe(df)
