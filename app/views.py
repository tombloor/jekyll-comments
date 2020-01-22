from flask import Flask
from app import app


@app.route('/')
def health_check():
    return "I'm still alive"

@app.route('/comment')
def new_comment():
    return "New comment, config should say where it's going n how it's created"
    