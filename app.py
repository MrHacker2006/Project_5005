from flask import Flask, render_template, request
# Naye imports add karne hain 
from main_pipeline import process_geopolitics_headline
from db_integration import save_prediction_to_db

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', result=None)

@app.route('/predict', methods=['POST'])
def predict():
    # 1. Data Capture
    user_news = request.form.get('headline_text')
    
    # 2. Pipeline Execution (ML tags extract karna)
    api_response = process_geopolitics_headline(user_news)
    
    # 3. Database Execution (MySQL mein log karna)
    save_prediction_to_db(api_response)
    
    # 4. Frontend Rendering (Strict mapping ke sath)
    return render_template('index.html', result=api_response)

if __name__ == '__main__':
    app.run(debug=True)