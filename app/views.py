import os
from datetime import datetime
from flask import Flask, abort, request
from app import app


@app.route('/')
def health_check():
    return f"I'm still alive. Debug Mode: {str(app.config['DEBUG'])}"

@app.route('/comment', methods=['POST'])
def new_comment():
    params = {
        'text': request.values.get('text', ''),
        'name': request.values.get('name', 'Anonymous'),
        'image': request.values.get('image', '')
    }

    if request.method == 'POST':
        text = params['text'].strip()
        if text == '':
            abort(400)

        lines = [
            '---',
            f'date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S %z")}',
            f'name: {params["name"].strip()}',
            f'image: {params["image"]}',
            '---',
            text,
            ''  # This gives us the blank line at EOF
        ]

        comment = os.linesep.join(lines)

        return comment
    else:
        abort(405)
    