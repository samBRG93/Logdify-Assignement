from abc import ABC, abstractmethod


class UserAnalysis(ABC):
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