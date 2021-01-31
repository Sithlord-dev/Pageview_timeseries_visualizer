import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data
df = pd.read_csv('files/forum-pageviews.csv', 
                 header = 0,
                 names=['Date', 'Views'],
                 parse_dates=['Date'], 
                 index_col='Date')

# Clean data
mask = (df['Views'] >= df['Views'].quantile(0.025)) & (df['Views'] <= df['Views'].quantile(0.975))
df_cln = df[mask]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(13,8))
    df_cln.plot(
      kind = 'line', 
      title = 'Daily freeCodeCamp Forum Page Views',
      xlabel = 'Date',
      ylabel = 'Page views',
      legend = False,
      ax=ax
    )

    # Save image and return fig 
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df_cln.copy()
    df_bar['Month'] = df_bar.index.month_name()
    df_bar['Year'] = df_bar.index.year
    df_bar['month_index'] = df_bar.index.month
    df_bar = df_bar.sort_values(by='month_index')

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(12,12))
    sns.barplot(
    data=df_bar, 
    y='Views', 
    x='Year', 
    hue='Month',
    ci=None,
    ax=ax)
    plt.legend(loc='upper left')

    # Save image and return fig
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Copy and modify data for box plots 
    df_box = df_cln.copy()
    df_box['Month'] = df_box.index.month_name().str.slice(stop=3)
    df_box['Year'] = df_box.index.year
    df_box['month_index'] = df_box.index.month
    df_box = df_box.sort_values(by='month_index')

    # Draw box plots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 16), tight_layout=True)

    sns.boxplot(
    data = df_box,
    x = 'Year', 
    y = 'Views',
    ax=ax1
    )
    sns.boxplot(
    data = df_box,
    x = 'Month', 
    y = 'Views', 
    ax=ax2
    )

    ax1.set_ylabel('Page views')
    ax1.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_ylabel('Page views')
    ax2.set_title('Year-wise Box Plot (Trend)')

    # Save image and return fig
    fig.savefig('box_plot.png')
    return fig
