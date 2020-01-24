import os
import pathlib
from datetime import datetime
from flask import Flask, abort, request, Response
from app import app


@app.route('/')
def health_check():
    return f"I'm still alive. Debug Mode: {str(app.config['DEBUG'])}"

@app.route('/comment', methods=['POST'])
def new_comment():
    params = {
        'perma': request.values.get('perma', ''),
        'text': request.values.get('text', ''),
        'name': request.values.get('name', 'Anonymous'),
        'image': request.values.get('image', '')
    }

    if request.method == 'POST':
        text = params['text'].strip()
        perma = params['perma'].strip()
        if text == '' or perma == '':
            abort(400)
        date = datetime.now()
        lines = [
            '---',
            f'date: {date.strftime("%Y-%m-%d %H:%M:%S")}',
            f'perma: "{perma}"',
            f'name: "{params["name"].strip()}"',
            f'image: "{params["image"]}"',
            '---',
            '',
            text,
            ''  # This gives us the blank line at EOF
        ]

        comment = os.linesep.join(lines)

        if app.config['COMMENT_MODE'] == 'file':
            slug = perma[perma.rstrip('/').rfind('/') + 1:]
            d = date.strftime("%Y%m%d_%H%M%S")
            filename = f'{d}_{slug}.md'
            write_comment_file(app.config['COMMENT_PATH'], filename, comment)
            return Response(status=200)
        elif app.config['COMMENT_MODE'] == 'git':
            pass
        else:
            return comment
    else:
        abort(405)
    
def write_comment_file(path, filename, comment):
    p = pathlib.Path(path)
    p.mkdir(0o775, True, True)

    p /= filename

    with p.open('w') as f:
        f.write(comment)
