from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            df = pd.read_excel(file)
            # Assuming the date is in a column named 'Policy End Date'
            dates = df['Policy End Date'].tolist()
            # Convert dates to string for display
            dates = [date.strftime('%Y-%m-%d') if isinstance(date, datetime) else str(date) for date in dates]
            return render_template('confirm_dates.html', dates=dates)
    return render_template('upload.html')

@app.route('/confirm', methods=['POST'])
def confirm_dates():
    # Get the confirmed dates from the form
    confirmed_dates = request.form.getlist('dates')
    # Here you would save the dates and set up notifications
    return "Dates confirmed: " + ", ".join(confirmed_dates)

if __name__ == '__main__':
    app.run(debug=True)
