import os
import joblib
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import cohere

load_dotenv()
app = Flask(__name__)
CORS(app)
API_KEY = os.getenv("API_KEY")
co = cohere.Client(API_KEY)

#find job method
def get_job(resume):
    #run ml model on resume to get job
    model = joblib.load('./model/resume-classifier')
    category_index = model.predict(resume)
    category_index = category_index[0]
    categories = ["Advocate", "Arts", "Automation Testing", "Blockchain", "Business Analyst", "Civil Engineer", "Data Science", "Database", "DevOps Engineer", "DotNet Developer", "ETL Developer", 
                  "Electrical Engineering", "HR", "Hadoop", "Health and fitness", "Java Developer", "Mechanical Engineer", "Network Security Engineer",
                  "Operations Manager", "PMO", "Python Developer", "SAP Developer", "Sales", "Testing", "Web Designing"];
    job = categories[category_index]
    return job


#get feedback method
@app.route('/api/feedback', methods=['POST'])
def get_recommendations():
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
        return 'Content-Type not supported!'
    
    resume = request.json['resume']
    job = get_job(resume)
    prompt = "Give feedback on the quality of this resume belonging to a " + job + ", check if the bullets focus on impact: " + resume
    res = co.generate( 
        model='xlarge', 
        prompt = prompt,
        max_tokens=40, 
        temperature=0.8,
        stop_sequences=["--"]
        )

    feedback = res.generations[0].text
    print(feedback)
    return jsonify({"feedback": str(feedback)})

app.run()