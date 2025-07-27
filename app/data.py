from flask import Flask, render_template_string
import pandas as pd

app = Flask(__name__)

# Load and preprocess the data
file_path = r"C:\Users\avram\OneDrive\Desktop\TRG Week 34\tsn.us.txt"
df = pd.read_csv(file_path, sep=",", parse_dates=['Date'], engine="python")

# Drop 'OpenInt' column if it exists
if 'OpenInt' in df.columns:
    df = df.drop(columns=['OpenInt'])

@app.route('/')
def show_tsn():
    table_html = df.to_html(classes='table table-bordered table-striped', index=False)
    return render_template_string(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>TSN Stock Data</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container mt-4">
            <h1>TSN Stock Data</h1>
            {table_html}
        </div>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(debug=True)
