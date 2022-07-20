from covid19_panama.autoupdate_module.autoupdate_strategy import AutoUpdateStrategy
from covid19_panama.autoupdate_module.strategies.strategy_github import GitHubStrategy
from covid19_panama.exceptions import NoStrategyProvidedException
import logging

logger = logging.getLogger(__name__)


class AutoUpdate:
    strategy = None

    def __init__(self, strategy='', repository='', branch_to_pull=''):
        if strategy.lower() == 'github':
            if repository and branch_to_pull:
                self.strategy = GitHubStrategy(
                    repository_path=repository,
                    branch=branch_to_pull
                )
                logger.info(f'REPOSITORY: {repository}:{branch_to_pull}')

    def execute(self) -> bool:
        executed = False
        if self.strategy:
            logger.info(f'Attempting autoupdate with strategy: {self.strategy}')

            autoupdate_strategy = AutoUpdateStrategy(self.strategy)

            logger.info('Attempting to obtain local state.')

            local_state = autoupdate_strategy.get_local_state()

            logger.info(f'Local state: {local_state}')

            logger.info('Attempting to obtain remote state.')

            remote_state = autoupdate_strategy.get_remote_state()

            logger.info(f'Remote state: {remote_state}')

            should_update = autoupdate_strategy.should_update(
                local_state=local_state,
                remote_state=remote_state
            )

            logger.info(f'Should update: {should_update}')

            if should_update:
                logger.info('Attempting pre-update action.')
                if autoupdate_strategy.pre_update_action():
                    logger.info('Pre-update action completed. Attempting update.')
                    if autoupdate_strategy.update():
                        logger.info('Update completed. Attempting post-update action.')
                        if autoupdate_strategy.post_update_action():
                            logger.info('Post-update action completed.')
                            executed = True
                        else:
                            logger.info('Could not perform post-update action.')
                    else:
                        logger.info('Could not perform the update.')
            else:
                logger.info('No need to auto update.')
            return executed
        else:
            raise NoStrategyProvidedException
