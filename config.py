import os
from dotenv import load_dotenv

load_dotenv()

# Enable Flask's debugging features. Should be False in production
DEBUG = os.getenv('DEBUG', False)

COMMENT_MODE=os.getenv('COMMENT_MODE')

#abs path when in file mode, path from repo root when in git mode
COMMENT_PATH=os.getenv('COMMENT_PATH')

#COMMENT_GIT_REPOSITORY=
#COMMENT_GIT_USERNAME=
#COMMENT_GIT_PASSWORD=
#COMMENT_GIT_BRANCH_PREFIX=

TZ=os.getenv('TZ')