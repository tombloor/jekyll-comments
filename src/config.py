import os
from dotenv import load_dotenv

load_dotenv()

# Enable Flask's debugging features. Should be False in production
DEBUG = os.getenv('DEBUG', False)
FLASK_RUN_PORT = os.getenv('FLASK_RUN_PORT')

COMMENT_MODE=os.getenv('COMMENT_MODE')

#abs path when in file mode, path from repo root when in git mode
COMMENT_PATH=os.getenv('COMMENT_PATH')

#COMMENT_GIT_REPOSITORY=
COMMENT_GIT_REPOSITORY=os.getenv('COMMENT_GIT_REPOSITORY')
COMMENT_GIT_TOKEN=os.getenv('COMMENT_GIT_TOKEN')
COMMENT_GIT_FOLDER=os.getenv('COMMENT_GIT_FOLDER')

TZ=os.getenv('TZ')