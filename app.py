from flask import Flask, render_template, request
from email_automation import send_email, categorize_emails, schedule_email
from ai_generator import generate_email
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    email_body = generate_email(prompt)
    return render_template('index.html', email_body=email_body)

@app.route('/send', methods=['POST'])
def send():
    recipient = request.form['recipient']
    subject = request.form['subject']
    email_body = request.form['email_body']
    send_email(recipient, subject, email_body)
    return "Email Sent Successfully!"

@app.route('/schedule', methods=['POST'])
def schedule():
    recipient = request.form['recipient']
    subject = request.form['subject']
    email_body = request.form['email_body']
    send_time = request.form['time']
    schedule_email(recipient, subject, email_body, send_time)
    return "Email Scheduled Successfully!"

if __name__ == '__main__':
    app.run(debug=True)
