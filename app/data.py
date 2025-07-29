from flask import Flask, render_template_string, url_for
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os
os.makedirs('static', exist_ok=True)


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

@app.route('/open_compare')
def open_compare():
    # Copy and prepare data
    df_05_open = df_05_08.copy()
    df_09_open = df_09_12.copy()
    df_13_open = df_13_17.copy()

    df_05_open['Year'] = df_05_open['Date'].dt.year
    df_09_open['Year'] = df_09_open['Date'].dt.year
    df_13_open['Year'] = df_13_open['Date'].dt.year

    # Group by Year and get average Open price
    avg_05_open = df_05_open.groupby('Year')['Open'].mean()
    avg_09_open = df_09_open.groupby('Year')['Open'].mean()
    avg_13_open = df_13_open.groupby('Year')['Open'].mean()

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(avg_05_open.index, avg_05_open.values, marker='o', label='2005–2008')
    plt.plot(avg_09_open.index, avg_09_open.values, marker='o', label='2009–2012')
    plt.plot(avg_13_open.index, avg_13_open.values, marker='o', label='2013–2017')
    plt.title('Yearly Avg Open Price (TSN)')
    plt.xlabel('Year')
    plt.ylabel('Avg Open Price')
    plt.legend()
    plt.grid(True)

    # Convert to image
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return f'<h2>Yearly Avg Open Comparison</h2><img src="data:image/png;base64,{plot_url}"/>'

@app.route('/volatility')
def volatility():
    # Ensure date columns are in datetime format
    df_05_08['Date'] = pd.to_datetime(df_05_08['Date'])
    df_09_12['Date'] = pd.to_datetime(df_09_12['Date'])
    df_13_17['Date'] = pd.to_datetime(df_13_17['Date'])

    # Calculate daily volatility
    df_05_08['Volatility'] = df_05_08['High'] - df_05_08['Low']
    df_09_12['Volatility'] = df_09_12['High'] - df_09_12['Low']
    df_13_17['Volatility'] = df_13_17['High'] - df_13_17['Low']

    # Group by year and take the mean
    vol_05_09 = df_05_08.groupby(df_05_08['Date'].dt.year)['Volatility'].mean()
    vol_10_14 = df_09_12.groupby(df_09_12['Date'].dt.year)['Volatility'].mean()
    vol_15_17 = df_13_17.groupby(df_13_17['Date'].dt.year)['Volatility'].mean()

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(vol_05_09.index, vol_05_09.values, label='2005–2009', marker='o')
    plt.plot(vol_10_14.index, vol_10_14.values, label='2010–2014', marker='s')
    plt.plot(vol_15_17.index, vol_15_17.values, label='2015–2017', marker='^')
    plt.title('Yearly Average Volatility (High - Low) for TSN')
    plt.xlabel('Year')
    plt.ylabel('Average Daily High-Low Spread')
    plt.legend()
    plt.grid(True)

    # Save and return image
    plot_path = os.path.join('static', 'volatility.png')
    plt.savefig(plot_path)
    plt.close()

    return render_template_string(f'''
    <!DOCTYPE html>
    <html>
    <head><title>Volatility Chart</title></head>
    <body>
        <h1>Price Volatility (High - Low)</h1>
        <img src="{url_for('static', filename='volatility.png')}" alt="Volatility Chart">
    </body>
    </html>
    ''')


if __name__ == '__main__':
    app.run(debug=True)
