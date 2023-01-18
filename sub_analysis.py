from datetime import datetime
import pandas as pd
from dateutil import relativedelta

from user_analysis import UserAnalysis


class SubscriptionsAnalysis(UserAnalysis):
    def __init__(self):
        self.df = self.__clean_data(pd.read_csv('Subscription.csv', sep=','))
        print(self.df.columns)

    def _run(self):
        user_ids = self.df['sub_id'].unique()
        print(user_ids, self.df.shape)
        df_result = pd.DataFrame()

        i = 0
        for sub_id in user_ids:
            df_usr = self.df[self.df['sub_id'] == sub_id]
            df_usr = df_usr.sort_values(by=['dates'])

            df_result = pd.concat([df_result, self._analyze_user(df_usr)])
            if i % 100 == 0:
                print(f'iteration: {i} df_usr.shape: {df_usr.shape}')

            i += 1

        return df_result

    def _analyze_user(self, df):
        sub_months_count = self.__months_since_first_sub(df)
        active_count, cancelled_count = self.__status_values_months_count(df)
        change_count = self.__months_since_last_sub_change(df)

        df_usr = pd.DataFrame({'sub_id': df['sub_id'].unique(),
                               'months_since_first_sub': sub_months_count,
                               'active_months': active_count,
                               'cancelled_months': cancelled_count,
                               'months_since_last_sub_change': change_count})
        return df_usr

    @classmethod
    def __clean_data(cls, df):
        df = cls.__add_user_sub_history_status_column(df)
        user_ids = df['sub_id'].unique()
        df_clean = pd.DataFrame()
        i = 0
        print(user_ids, df.shape)

        for sub_id in user_ids:
            df_usr = df[df['sub_id'] == sub_id]

            _df_temp = df_usr[df_usr.duplicated(subset=['dates'], keep=False)]
            dates = _df_temp['dates'].tolist()
            for date in dates:
                _df_temp = df_usr[df_usr['dates'] == date]
                if _df_temp['status'].nunique() > 1:
                    df_usr = df_usr[df_usr['dates'] != date]

            df_usr = df_usr.sort_values(by=['dates'])
            if df_usr['status'].iloc[0] == 'canceled':
                df_usr['usr_sub_history_status'] = 'dirty'
            else:
                df_usr['usr_sub_history_status'] = 'clean'

            df_clean = pd.concat([df_clean, df_usr], ignore_index=True)

            if i % 100 == 0:
                print(f'cleaning data: {i} df_usr.shape: {df_usr.shape}')
            i += 1

        df_clean = cls._clean_columns(df_clean)
        return df_clean

    @staticmethod
    def __add_user_sub_history_status_column(df):
        df['usr_sub_history_status'] = None
        return df

    @staticmethod
    def __months_since_first_sub(df):
        try:
            start_date = datetime.strptime(df['dates'].min(), '%Y-%m')
            end_date = datetime.strptime(df['dates'].max(), '%Y-%m')
            delta = relativedelta.relativedelta(end_date, start_date)
            sub_months_count = delta.years * 12 + delta.months
        except Exception as e:
            raise e

        return sub_months_count

    @classmethod
    def __status_values_months_count(cls, df):
        periods = []
        periods.extend(cls.__status_values_months_count_start_period(df))
        if periods and list(periods[-1].keys())[0] != df.iloc[-1]['status']:
            periods.extend(cls.__status_values_months_count_end_period(df))

        active_count = 0
        canceled_count = 0
        for period in periods:
            if 'canceled' in period:
                canceled_count += period['canceled']
            if 'active' in period:
                active_count += period['active']

        return active_count, canceled_count

    @classmethod
    def __status_values_months_count_start_period(cls, df):
        df = df.sort_values(by=['dates'])
        start_status = df['status'].iloc[0]
        cursor_date = datetime.strptime(df['dates'].iloc[0], '%Y-%m')

        return cls.__status_values_months_count_period(df, cursor_date, start_status)

    # todo: controllare se da risultati giusti
    @classmethod
    def __status_values_months_count_end_period(cls, df):
        try:
            df = df.reset_index(drop=False)
            end_status = df['status'].iloc[-1]
            cursor_date = None
            for index, row in df.iloc[::-1].iterrows():
                if row['status'] != end_status:
                    df = df.iloc[(index + 1):]
                    cursor_date = datetime.strptime(df['dates'].iloc[0], '%Y-%m')
                    break

            if cursor_date:
                return cls.__status_values_months_count_period(df, cursor_date, end_status)
            else:
                return []
        except Exception as e:
            raise e

        return periods

    @staticmethod
    def __status_values_months_count_period(df, cursor_date, start_status):
        df = df.drop_duplicates(subset=['dates'], keep='first')
        row_date = datetime.strptime(df['dates'].iloc[0], '%Y-%m')
        periods = []
        for index, row in df.iloc[1:].iterrows():
            row_date = datetime.strptime(row['dates'], '%Y-%m')

            if row['status'] != start_status:
                delta = relativedelta.relativedelta(row_date, cursor_date)
                period = delta.years * 12 + delta.months
                periods.append({start_status: period})
                start_status = row['status']
                cursor_date = row_date

        if len(periods) == 0:
            delta = relativedelta.relativedelta(row_date, cursor_date)
            period = delta.years * 12 + delta.months + 1
            periods.append({start_status: period})
        return periods

    @staticmethod
    def __months_since_last_sub_change(df):
        try:
            change_count = 0
            end_date = datetime.strptime(df['dates'].max(), '%Y-%m')
            end_status = df['status'].max()

            for index, row in df.iloc[:-1].iloc[::-1].iterrows():
                if row['status'] != end_status:
                    start_date = datetime.strptime(row['dates'], '%Y-%m')
                    delta = relativedelta.relativedelta(end_date, start_date)
                    change_count = delta.years * 12 + delta.months
                    break
        except Exception as e:
            raise e

        return change_count
