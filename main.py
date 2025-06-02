import pandas as pd

from booking_analysis import BookingAnalysis
from sub_analysis import SubscriptionsAnalysis
import matplotlib

matplotlib.use('MacOSX')
import matplotlib.pyplot as plt


def _run_users_analysis():
    booking_analysis = BookingAnalysis()
    sub_analysis = SubscriptionsAnalysis()

    df_ba = booking_analysis.execute()
    df_sa = sub_analysis.execute()

    df = df_ba.merge(df_sa, on='sub_id', how='inner')

    df.to_csv('user_analysis.csv')


def plot_user_analysis():
    df = pd.read_csv('user_analysis.csv')
    df = df[["confirmed_bookings", "months_since_first_sub", "active_months", "cancelled_months",
             "months_since_last_sub_change"]]

    stats = pd.DataFrame({
        'Mean': df.mean(),
        'Max': df.max(),
        'Min': df.min(),
        'Std': df.std()
    })

    stats.plot(kind='bar', figsize=(12, 6))
    plt.title('User Analysis')
    plt.xlabel('Columns')
    plt.ylabel('Values')
    plt.xticks(rotation=45)
    plt.legend(title="Users Stats")
    plt.tight_layout()
    # plt.show()
    plt.savefig('user_analysis.png')


if __name__ == '__main__':
    # _run_users_analysis()
    plot_user_analysis()
