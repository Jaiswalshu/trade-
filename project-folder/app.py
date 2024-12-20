from flask import Flask, render_template, request, redirect
import pandas as pd
import os

app = Flask(__name__)

# Path to save uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    symbol_summary = None
    total_profit_usd = None
    error_message = None

    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

            try:
                # Load and process the dataset
                data = pd.read_csv(filename)

                # Check for necessary columns
                if 'symbol' not in data.columns or 'profit_usd' not in data.columns:
                    error_message = "CSV must contain 'symbol' and 'profit_usd' columns."
                    return render_template('index.html', error=error_message)

                # Group data by 'symbol' and calculate the count of trades and sum of 'profit_usd'
                symbol_summary = data.groupby('symbol').agg(
                    trade_count=('symbol', 'count'),
                    total_profit_usd=('profit_usd', 'sum')
                ).reset_index()

                # Calculate the total profit across all symbols
                total_profit_usd = symbol_summary['total_profit_usd'].sum()

            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
                return render_template('index.html', error=error_message)

    # Convert DataFrame to HTML string if symbol_summary is not None
    if symbol_summary is not None:
        symbol_summary_html = symbol_summary.to_html(classes='summary-table', index=False)
    else:
        symbol_summary_html = None

    return render_template('index.html', symbol_summary=symbol_summary_html, total_profit_usd=total_profit_usd, error=error_message)

if __name__ == '__main__':
    # Make the 'uploads' folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
