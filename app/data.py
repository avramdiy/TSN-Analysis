from flask import Flask, render_template_string
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64


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

@app.route('/close_compare')
def close_compare():
    # Group by year and calculate average Close price
    df_05_avg = df_05_08.copy()
    df_09_avg = df_09_12.copy()
    df_13_avg = df_13_17.copy()

    df_05_avg['Year'] = df_05_avg['Date'].dt.year
    df_09_avg['Year'] = df_09_avg['Date'].dt.year
    df_13_avg['Year'] = df_13_avg['Date'].dt.year

    avg_05 = df_05_avg.groupby('Year')['Close'].mean()
    avg_09 = df_09_avg.groupby('Year')['Close'].mean()
    avg_13 = df_13_avg.groupby('Year')['Close'].mean()

    # Plot
    plt.figure(figsize=(10,6))
    plt.plot(avg_05.index, avg_05.values, marker='o', label='2005–2008')
    plt.plot(avg_09.index, avg_09.values, marker='o', label='2009–2012')
    plt.plot(avg_13.index, avg_13.values, marker='o', label='2013–2017')
    plt.title('Yearly Avg Close Price (TSN)')
    plt.xlabel('Year')
    plt.ylabel('Avg Close Price')
    plt.legend()
    plt.grid(True)

    # Convert plot to image
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return f'<h2>Yearly Avg Close Comparison</h2><img src="data:image/png;base64,{plot_url}"/>'


if __name__ == '__main__':
    app.run(debug=True)
