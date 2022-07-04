import os
import sys
import json
import syslog


class Config:
    def __init__(self, filename='config.json'):
        self.filename = filename
        self.cfg = {}
        self.load()

    def load(self) -> object:
        if os.path.exists(self.filename):
            with open(self.filename) as f:
                self.cfg = json.load(f)
        else:
            syslog.syslog(f"Creating new configuration file {self.filename}")
            self.cfg = {'state': 'New'}

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.cfg, f)

    def get(self, key=None, default=None):
        return self.cfg.get(key, default)

    def update(self, **kwargs):
        self.cfg.update(kwargs)

    def set_state(self, state):
        cur_state = self.get_state()
        self.update(state=state)
        return cur_state

    def get_state(self):
        return self.get("state", "New")

    def get_filename(self):
        return self.filename
