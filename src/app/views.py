import base64
import hashlib 
import os
import pathlib
import pytz
import requests

from datetime import datetime
from flask import Flask, abort, request, Response
from github import Github
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
        
        tz = pytz.timezone(app.config["TZ"])
        date = tz.localize(datetime.now())

        image = get_image_data(params['persona'].strip().lower())

        lines = [
            '---',
            f'date: {date.isoformat()}',
            f'perma: "{perma}"',
            f'name: "{params["name"].strip()}"',
            f'image: "data:image/png;base64, {image}"',
            '---',
            '',
            text,
            ''  # This gives us the blank line at EOF
        ]

        perma_strip = perma.rstrip('/')
        slug = perma_strip[perma_strip.rfind('/') + 1:]
        d = date.strftime("%Y%m%d_%H%M%S")
        filename = f'{d}_{slug}.md'

        if app.config['COMMENT_MODE'] == 'local':
            comment = os.linesep.join(lines)
            write_comment_local(app.config['COMMENT_PATH'], filename, comment)
            return Response(status=200)
        elif app.config['COMMENT_MODE'] == 'git':
            comment = '\n'.join(lines)
            write_comment_git(app.config['COMMENT_PATH'], filename, comment)
            return Response(status=200)
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

def write_comment_git(path, filename, comment):
    g = Github(app.config['COMMENT_GIT_TOKEN'])

    repo = g.get_repo(app.config['COMMENT_GIT_REPOSITORY'])

    default_branch = repo.get_branch(repo.default_branch).commit.sha
    base = None
    try:
        base = repo.get_branch(app.config['COMMENT_GIT_FOLDER'] + '/moderated')
    except Exception as err:
        repo.create_git_ref(app.config['COMMENT_GIT_FOLDER'] + '/moderated', default_branch)
        base = repo.get_branch(app.config['COMMENT_GIT_FOLDER'] + '/moderated')

    new_branchname = filename.replace('.md', '')
    branch = repo.create_git_ref(f"refs/heads/{app.config['COMMENT_GIT_FOLDER']}/{new_branchname}", default_branch)
    
    p = pathlib.Path(path) / filename
    commit_msg = f'New comment: {new_branchname}'
    repo.create_file(str(p), commit_msg, comment, branch=branch.ref)

    pr = repo.create_pull(title=commit_msg, body=f"```{comment}```", head=branch.ref, base=base.name)
    return pr