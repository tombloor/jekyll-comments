import base64
import hashlib 
import os
import pathlib
import requests

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
        'persona': request.values.get('persona', '')
    }

    if request.method == 'POST':
        text = params['text'].strip()
        perma = params['perma'].strip()
        if text == '' or perma == '':
            abort(400)
        date = datetime.now()

        image = get_image_data(params['persona'].strip().lower())

        lines = [
            '---',
            f'date: {date.strftime("%Y-%m-%d %H:%M:%S")}',
            f'perma: "{perma}"',
            f'name: "{params["name"].strip()}"',
            f'image: "data:image/png;base64, {image}"',
            '---',
            '',
            text,
            ''  # This gives us the blank line at EOF
        ]

        comment = os.linesep.join(lines)

        if app.config['COMMENT_MODE'] == 'local':
            perma_strip = perma.rstrip('/')
            slug = perma_strip[perma_strip.rfind('/') + 1:]
            d = date.strftime("%Y%m%d_%H%M%S")
            filename = f'{d}_{slug}.md'
            write_comment_local(app.config['COMMENT_PATH'], filename, comment)
            return Response(status=200)
        elif app.config['COMMENT_MODE'] == 'git':
            # https://developer.github.com/v3/repos/contents/#create-or-update-a-file
            # https://developer.github.com/v3/pulls/#create-a-pull-request
            pass
        else:
            return comment
    else:
        abort(405)

def get_image_data(persona):
    if persona == '':
        return ''

    if persona[0] == '@':
        url = f'https://twitter.com/{persona}/profile_image?size=normal'
    elif '@' in persona:
        md5 = hashlib.md5(persona.encode('utf-8')).hexdigest()
        url = f'http://www.gravatar.com/avatar/{md5}?s=80'
    else:
        url = f'https://github.com/{persona}.png?size=80'

    return base64.b64encode(requests.get(url).content).decode("utf-8")
    
def write_comment_local(path, filename, comment):
    p = pathlib.Path(path)
    p.mkdir(0o775, True, True)

    p /= filename

    with p.open('w') as f:
        f.write(comment)
