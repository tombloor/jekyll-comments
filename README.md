# jekyll-comments
A flask application for generating comments as static files

The following environment variables will control the application

```
# Debug should always be false for production
DEBUG=False  

# Comment mode controls whether the application will write comment files to
# the local file system, or create them as pull requests in a github repository
#COMMENT_MODE='git'  
#COMMENT_MODE='local'

# Comment path controls where the comment files will be saved. 
# When using local comments mode, this should be an absolute path to the 
# desired location on the file system.
# When using git mode, this should be a path relative to your repository root
COMMENT_PATH=

# When using git mode, the repository you want to connect to (user/repo)
COMMENT_GIT_REPOSITORY=''

# Git access token
COMMENT_GIT_TOKEN=''

# When using git mode new comments will be created as branches with a pull
# request. The git folder will create all comment branches as folder/comment.
# it will set the base branch of the pull requests to folder/moderated, so that
# you can merge comments back to your master branch in batches
COMMENT_GIT_FOLDER=''

# This is the port the application will run on
FLASK_RUN_PORT=

# Timezone
TZ='America/Chicago'
```

If running the application directly, these can be provided in an env file which
should be placed at `src/.env`

If the application is being run in a docker environment, you can either pass
the variables inline with the run command, or define them in a docker compose
file.
