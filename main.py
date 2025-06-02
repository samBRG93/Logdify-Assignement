from booking_analysis import BookingAnalysis
from sub_analysis import SubscriptionsAnalysis


def _run_users_analysis():
    booking_analysis = BookingAnalysis()
    sub_analysis = SubscriptionsAnalysis()

    df_ba = booking_analysis.execute()
    df_sa = sub_analysis.execute()

    df = df_ba.merge(df_sa, on='sub_id', how='inner')
    df.to_csv('user_analysis.cs v')


if __name__ == '__main__':
    _run_users_analysis()
