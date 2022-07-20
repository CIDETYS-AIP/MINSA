from django.conf import settings
from pathlib import PosixPath
import git
import logging

logger = logging.getLogger(__name__)


class GitHubStrategy:
    repository_path: 'PosixPath' = ''
    branch = ''

    def __init__(self, repository_path, branch, *args, **kwargs):
        self.repository_path = settings.ROOT_DIR / repository_path
        self.branch = branch

    def get_local_state(self) -> str:
        '''
        If parameter to Repo is empty, it will attempt to use the project that runs the code.
        '''
        repository = git.Repo(self.repository_path)
        local_state = repository.head.commit.hexsha

        return local_state

    def get_remote_state(self) -> str:
        '''
        If parameter to Repo is empty, it will attempt to use the project that runs the code.
        '''
        repository = git.Repo(self.repository_path)
        remote_state = repository.remotes.origin.refs[self.branch].commit.hexsha

        return remote_state

    def should_update(self, local_state=None, remote_state=None) -> bool:
        should_update = False
        '''
        Because strings are falsy values, if either state is empty or falsy,
        this method will not evaluate to true and thus it will not make a comparison.
        '''
        if local_state and remote_state:
            if local_state != remote_state:
                should_update = True
        return should_update

    def pre_update_action(self) -> bool:
        '''
        Unnecessary for now, so we will just return True to signal it took place.
        '''
        return True

    def update(self) -> bool:
        try:
            remote_repo = git.Repo(self.repository_path)
            origin = remote_repo.remotes.origin
            '''
            The remote branch to pull is either main or master, depending on the repo.
            It can be any other branch, but main or master will generally contain the
            authoritative version of the information.

            By default, will attempt to pull from master.
            '''
            origin.pull(self.branch)
            return True
        except Exception as e:
            logger.error(f'Could not updated remote repository. Exception: {e}')
            raise e

    def post_update_action(self) -> bool:
        '''
        Unnecessary for now, so we will just return True to signal it took place.
        '''
        return True
