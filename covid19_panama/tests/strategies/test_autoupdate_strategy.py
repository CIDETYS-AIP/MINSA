from covid19_panama.autoupdate_module.autoupdate import AutoUpdate
from covid19_panama.autoupdate_module.autoupdate_strategy import AutoUpdateStrategy
from covid19_panama.autoupdate_module.strategies.strategy_github import GitHubStrategy
from covid19_panama.exceptions import NoStrategyProvidedException
from django.conf import settings
from django.test import TestCase, override_settings
from unittest.mock import patch, Mock


class AutoUpdateStrategyGithubTestCase(TestCase):
    @patch('git.Repo')
    def test_get_local_state(self, mock_repo):
        mock_instance = mock_repo.return_value
        mock_instance.head.commit.hexsha = 'db87cc0ad992ba24ab79588d0423ae23d2d8ccbe'

        autoupdate = AutoUpdateStrategy(
            autoupdate_strategy=GitHubStrategy(
                repository_path='',
                branch=''
            )
        )

        expected_local_state = 'db87cc0ad992ba24ab79588d0423ae23d2d8ccbe'

        local_state = autoupdate.get_local_state()

        self.assertEqual(local_state, expected_local_state)

    @override_settings(REPOSITORY_BRANCH_TO_PULL='hello')
    @patch('git.Repo')
    def test_get_remote_state(self, mock_repo):
        mock_instance = mock_repo.return_value
        (
            mock_instance
            .remotes
            .origin
            .refs[settings.REPOSITORY_BRANCH_TO_PULL]
            .commit
            .hexsha
        ) = '1f37178ce7cead0119944f5e46735b2dc2972849'

        autoupdate = AutoUpdateStrategy(
            autoupdate_strategy=GitHubStrategy(
                repository_path='',
                branch=''
            )
        )

        remote_state = autoupdate.get_remote_state()

        expected_remote_state = '1f37178ce7cead0119944f5e46735b2dc2972849'

        self.assertEqual(remote_state, expected_remote_state)

    def test_should_update(self):
        autoupdate = AutoUpdateStrategy(
            autoupdate_strategy=GitHubStrategy(
                repository_path='',
                branch=''
            )
        )

        local_state = 'db87cc0ad992ba24ab79588d0423ae23d2d8ccbf'
        remote_state = '1f37178ce7cead0119944f5e46735b2dc2972848'

        should_update = autoupdate.should_update(local_state=local_state, remote_state=remote_state)

        self.assertTrue(should_update)

    def test_should_not_update(self):
        autoupdate = AutoUpdateStrategy(
            autoupdate_strategy=GitHubStrategy(
                repository_path='',
                branch=''
            )
        )

        local_state = 'db87cc0ad992ba24ab79588d0423ae23d2d8ccbf'
        remote_state = 'db87cc0ad992ba24ab79588d0423ae23d2d8ccbf'

        should_update = autoupdate.should_update(local_state=local_state, remote_state=remote_state)

        self.assertFalse(should_update)

    def test_should_not_update_empty_states(self):
        autoupdate = AutoUpdateStrategy(
            autoupdate_strategy=GitHubStrategy(
                repository_path='',
                branch=''
            )
        )

        local_state = ''
        remote_state = ''

        should_update = autoupdate.should_update(local_state=local_state, remote_state=remote_state)

        self.assertFalse(should_update)

    def test_should_not_update_one_empty_state(self):
        autoupdate = AutoUpdateStrategy(
            autoupdate_strategy=GitHubStrategy(
                repository_path='',
                branch=''
            )
        )

        local_state = 'db87cc0ad992ba24ab79588d0423ae23d2d8ccbf'
        remote_state = ''

        should_update = autoupdate.should_update(local_state=local_state, remote_state=remote_state)

        self.assertFalse(should_update)

    def test_pre_update_action(self):
        autoupdate = AutoUpdateStrategy(
            autoupdate_strategy=GitHubStrategy(
                repository_path='',
                branch=''
            )
        )

        completed = autoupdate.pre_update_action()

        self.assertTrue(completed)

    def test_post_update_action(self):
        autoupdate = AutoUpdateStrategy(
            autoupdate_strategy=GitHubStrategy(
                repository_path='',
                branch=''
            )
        )

        completed = autoupdate.post_update_action()

        self.assertTrue(completed)

    @patch('git.Repo')
    def test_update(self, mock_repo):
        mock_instance = mock_repo.return_value
        mock_instance.remotes.origin = Mock()
        mock_instance.remotes.origin.pull = Mock()

        autoupdate = AutoUpdateStrategy(
            autoupdate_strategy=GitHubStrategy(
                repository_path='',
                branch=''
            )
        )

        updated = autoupdate.update()

        self.assertTrue(updated)
        self.assertTrue(mock_instance.remotes.origin.pull.called)

    def test_update_throws_exception(self):
        autoupdate = AutoUpdateStrategy(
            autoupdate_strategy=GitHubStrategy(
                repository_path='asdfasdf',
                branch=''
            )
        )

        with self.assertRaises(Exception):
            updated = autoupdate.update()
            self.assertFalse(updated)


class AutoupdateTestCase(TestCase):
    def test_autoupdate_has_correct_strategy(self):
        autoupdate = AutoUpdate(
            strategy='github',
            repository='asdfasdf',
            branch_to_pull='asdfasdf'

        )
        self.assertTrue(isinstance(autoupdate.strategy, GitHubStrategy))

    def test_unsupported_strategy(self):
        autoupdate = AutoUpdate(strategy='')
        self.assertEqual(autoupdate.strategy, None)

    def test_execute_raises_exception(self):
        autoupdate = AutoUpdate(strategy='')
        with self.assertRaises(NoStrategyProvidedException):
            autoupdate.execute()

    @patch('covid19_panama.autoupdate_module.autoupdate_strategy.AutoUpdateStrategy.post_update_action')
    @patch('covid19_panama.autoupdate_module.autoupdate_strategy.AutoUpdateStrategy.update')
    @patch('covid19_panama.autoupdate_module.autoupdate_strategy.AutoUpdateStrategy.pre_update_action')
    @patch('covid19_panama.autoupdate_module.autoupdate_strategy.AutoUpdateStrategy.should_update')
    @patch('covid19_panama.autoupdate_module.autoupdate_strategy.AutoUpdateStrategy.get_remote_state')
    @patch('covid19_panama.autoupdate_module.autoupdate_strategy.AutoUpdateStrategy.get_local_state')
    def test_autoupdate_calls_strategy_methods(
        self, mock_local_state, mock_remote_state, mock_should_update, mock_pre_update_action, mock_update,
        mock_post_update_action
    ):
        autoupdate = AutoUpdate(
            repository='asdfasdf',
            branch_to_pull='asdfasdf',
            strategy='github',
        )
        autoupdate.execute()
        self.assertTrue(mock_local_state.called)
        self.assertTrue(mock_remote_state.called)
        self.assertTrue(mock_should_update.called)
        self.assertTrue(mock_pre_update_action.called)
        self.assertTrue(mock_update.called)
        self.assertTrue(mock_post_update_action.called)
