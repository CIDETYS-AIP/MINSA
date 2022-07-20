class AutoUpdateStrategy:
    def __init__(self, autoupdate_strategy=None):
        self.autoupdate_strategy = autoupdate_strategy

    def get_local_state(self, *args, **kwargs):
        return self.autoupdate_strategy.get_local_state(*args, **kwargs)

    def get_remote_state(self, *args, **kwargs):
        return self.autoupdate_strategy.get_remote_state(*args, **kwargs)

    def should_update(self, local_state, remote_state):
        return self.autoupdate_strategy.should_update(
            local_state=local_state,
            remote_state=remote_state
        )

    def pre_update_action(self, *args, **kwargs):
        return self.autoupdate_strategy.pre_update_action(*args, **kwargs)

    def update(self, *args, **kwargs):
        return self.autoupdate_strategy.update(*args, **kwargs)

    def post_update_action(self, *args, **kwargs):
        return self.autoupdate_strategy.post_update_action(*args, **kwargs)
