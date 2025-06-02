import pandas as pd
from user_analysis import UserAnalysis


class BookingAnalysis(UserAnalysis):
    def __init__(self):
        self.df = self.__clean_data(pd.read_csv('Bookings.csv', sep=','))
        self.df.rename(columns={'subscriber_id': 'sub_id'}, inplace=True)
        print(f"Dataframe Columns: {self.df.columns}")

    def _run(self):
        user_ids = self.df['sub_id'].unique()
        print(user_ids, self.df.shape)
        df_result = pd.DataFrame()
        i = 0
        for sub_id in user_ids:
            df_usr = self.df[self.df['sub_id'] == sub_id]
            df_usr = df_usr.sort_values(by=['booking_date'])

            df_result = pd.concat([df_result, self._analyze_user(df_usr)])
            if i % 100 == 0:
                print(f'iteration: {i} df_usr.shape: {df_usr.shape}')
            i += 1

        return df_result

    def _analyze_user(self, df):
        sub_months_count = self.__count_user_confirmed_bookings(df)
        df_usr = pd.DataFrame({'sub_id': df['sub_id'].unique(), 'confirmed_bookings': sub_months_count})
        return df_usr

    @classmethod
    def __clean_data(cls, df):
        return cls._clean_columns(df)

    @staticmethod
    def __count_user_confirmed_bookings(df):
        return df[df['booking_status'] == 'Confirmed'].shape[0]
