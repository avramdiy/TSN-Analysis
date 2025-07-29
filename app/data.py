from flask import Flask, render_template_string
import pandas as pd

app = Flask(__name__)

# Load and preprocess the data
file_path = r"C:\Users\avram\OneDrive\Desktop\TRG Week 34\tsn.us.txt"
df = pd.read_csv(file_path, sep=",", parse_dates=['Date'], engine="python")

# Drop 'OpenInt' column if it exists
if 'OpenInt' in df.columns:
    df = df.drop(columns=['OpenInt'])

# Filtered DataFrames
df_05_08 = df[(df['Date'] >= '2005-02-25') & (df['Date'] <= '2008-12-31')]
df_09_12 = df[(df['Date'] >= '2009-01-01') & (df['Date'] <= '2012-12-31')]
df_13_17 = df[(df['Date'] >= '2013-01-01') & (df['Date'] <= '2017-11-10')]

# Convert to HTML
def dataframe_to_html(df_subset):
    return df_subset.to_html(classes='table table-striped', index=False)

@app.route('/')
def home():
    return "<h2>Available Routes: /05_08, /09_12, /13_17</h2>"

@app.route('/05_08')
def show_05_08():
    return dataframe_to_html(df_05_08)

@app.route('/09_12')
def show_09_12():
    return dataframe_to_html(df_09_12)

@app.route('/13_17')
def show_13_17():
    return dataframe_to_html(df_13_17)

if __name__ == '__main__':
    app.run(debug=True)
