#!/usr/bin/env python3

import os
import sys
import dask.dataframe as dd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

matplotlib.style.use('ggplot')
sns.set()

plots_dir = os.path.abspath('../plots')
events_filename = os.path.abspath('../data/EVENTS-short.csv')
icu_stays_filename = os.path.abspath('../data/ICUSTAYS.csv')

events_df = dd.read_csv(events_filename, parse_dates=['CHARTTIME', 'STORETIME'], dtype={
    'CGID': 'Int64', 'ICUSTAY_ID': 'Int64'
})


def plot_icu_histogram(icu_id, kind='scatter', dataframe=events_df):
    data = dataframe[['SUBJECT_ID', 'VALUENUM', 'ICUSTAY_ID', 'CHARTTIME', 'ITEMID']] \
        .query('ICUSTAY_ID == {}'.format(icu_id)) \
        .compute()

    plot = sns.relplot(x='CHARTTIME', y='VALUENUM', col='ICUSTAY_ID',
                       kind=kind,
                       height=8, aspect=2,
                       data=data) \
        .set(title='item\'s values over time for ICUSTAY_ID {}'.format(icu_id))

    ax = plt.gca()
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    plt.xticks(rotation=30)

    # plt.show()
    plot.figure.savefig(os.path.join(plots_dir, 'item-histogram.png'))


def items_frequency(dataframe=events_df):
    dataframe[['ITEMID', 'VALUENUM']].compute() \
        .groupby('ITEMID') \
        .count() \
        .hist()

    plt.title('Frequency of each item')

    ax = plt.gca()
    ax.set_xlabel('Item ID')
    ax.set_ylabel('Frequency')
    plt.xticks(rotation=20)


def item_plot(item_id, dataframe=events_df):
    dataframe[['ITEMID', 'CHARTTIME', 'VALUENUM']] \
        .query('ITEMID == {}'.format(item_id)) \
        .compute() \
        .plot(x='CHARTTIME', y='VALUENUM',
              style='.',
              figsize=(16, 7),
              title='Values for ITEMID {}'.format(item_id))

    ax = plt.gca()
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    plt.xticks(rotation=20)

def main():
    os.makedirs('../plots', exist_ok=True)
    plot_icu_histogram(261926, 'line')
    return 0


if __name__ == '__main__':
    sys.exit(main())
