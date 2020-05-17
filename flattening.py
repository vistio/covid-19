import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import seaborn as sns
import os
from datetime import datetime, timedelta

def save_graph():
    base_name = 'Folkhalsomyndigheten_Covid19'
    fhm = 'data/FHM/'
    days_to_cut = 8

    list_of_files = os.listdir(fhm)

    beginning_n = len(base_name)
    list_of_files = [x for x in list_of_files if x[:beginning_n] == base_name]
    list_of_files.sort()

    datelist = pd.date_range('2020-03-13', datetime.today()).tolist()

    df = pd.DataFrame()
    df['date'] = datelist
    df['date'] = df['date'].dt.date

    for file_name in list_of_files:
        xl = pd.ExcelFile(fhm+file_name)
        dpd = xl.parse('Antal avlidna per dag', skipfooter=1)
        df[file_name[-15:-5]] = pd.Series(dpd.query('Datum_avliden > "2020-03-12"')['Antal_avlidna'].astype(int).tolist()[:-days_to_cut])

    df = df.set_index('date')

    new_date = datetime.today()

    dates = []

    for i in range(8):
        dates.append(str(new_date.date()))
        new_date = new_date-timedelta(days=4)

    dates.reverse()

    # dates = [
    #     '2020-04-07',
    #     '2020-04-10',
    #     '2020-04-13',
    #     '2020-04-16',
    #     '2020-04-19',
    #     '2020-04-22',
    #     '2020-04-25',
    #     '2020-04-28',
    #         ]

    days_to_polyfit = 12

    num_dates = len(dates)
    g = [None] * num_dates
    h = g

    sns.set(style='dark')

    plt.rcParams['patch.edgecolor'] = 'none'
    colors = ['blue/green', 'light grey blue']
    pal = sns.xkcd_palette(colors)
    sns.set_palette(pal)

    f, ax = plt.subplots(nrows=num_dates, figsize=(6,12), dpi=300)

    i = 0
    for date in dates:
        end_date = pd.to_datetime(dates[i])-pd.DateOffset(days=days_to_cut)
        start_date = pd.to_datetime('2020-03-13')
        data = df.loc[start_date:end_date]
        x = data.index
        y = data[date]
        
        # plot dots
        g[i] = sns.scatterplot(data=data, x=x, y=y, ax=ax[i], color=sns.xkcd_rgb["light grey blue"], size=1, linewidth=0)
        g[i].legend_ = None
        
        # fit line to curve for the last 10 days
        poly_coeff = np.polyfit(np.arange(days_to_polyfit), y[-days_to_polyfit:], 1)
        ynew=np.poly1d(poly_coeff)
        new_line = ynew(np.arange(days_to_polyfit))

        h[i] = sns.lineplot(data=data, x=x[-days_to_polyfit:], y=new_line, ax=ax[i])
        h[i].legend_ = None
        
        ax[i].set_title('Gradient: '+str(np.round(poly_coeff[0],2)), fontsize=10, y=0.7)
        
        x_axis = ax[i].axes.get_xaxis()
        x_label = x_axis.get_label()
        x_label.set_visible(False)

        # set dates
        ax[i].set_xticks([start_date, end_date])
        ax[i].set_xlim(start_date, end_date)
        ax[i].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        print(end_date.date())
        
        i = i+1
        
    tmp = plt.setp(ax, ylim=(0,120))
    f.suptitle('COVID-19 deaths in Sweden')
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])

    plt.savefig('graphs/flattening.png', bbox_inches='tight')

    return 'graphs/flattening.png'

if __name__ == "__main__":
    save_graph()
