from datetime import datetime
import pandas as pd
from dateutil import relativedelta

from abc import ABC, abstractmethod


class UserAnalysis(ABC):
    def __init__(self):
        self.df = None

    @abstractmethod
    def _analyze_user(self, df):
        pass

    @staticmethod
    def _clean_columns(df):
        return df.drop(columns=['Unnamed: 0'])

    @abstractmethod
    def _run(self):
        pass

    def execute(self):
        return self._run()

    def show_users(self):
        self._run(print)
