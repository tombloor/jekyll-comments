from flask import Flask
from app import app


@app.route('/')
def health_check():
    return f"I'm still alive. Debug Mode: {str(app.config['DEBUG'])}"

@app.route('/comment')
def new_comment():
    ret = "New comment, config should say where it's going n how it's created."
    ret += f" Comment will be saved at {app.config['COMMENT_PATH']}"
    return ret
    