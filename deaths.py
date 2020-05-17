import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def save_graph():
    file_name = 'Folkhalsomyndigheten_Covid19.xlsx'

    xl = pd.ExcelFile('data/'+file_name)
    # xl.sheet_names
    dpd = xl.parse('Antal avlidna per dag', skipfooter=1)

    dpd['kumulativ'] = dpd['Antal_avlidna'].cumsum()

    dpd['rullande'] = dpd['Antal_avlidna'].rolling(7, center=True).mean()

    dpd.tail()

    ndpd = pd.melt(dpd, id_vars='Datum_avliden', var_name='typ', value_name='antal')

    ndpd['Datum_avliden'] = ndpd['Datum_avliden'].dt.date

    sns.set()

    plt.rcParams['patch.edgecolor'] = 'none'
    colors = ['blue/green', 'light grey blue']
    pal = sns.xkcd_palette(colors)
    sns.set_palette(pal)

    f, ax = plt.subplots(figsize=(14,8), dpi=300)

    plt.xticks(rotation=90)
    ax2 = ax.twinx()
    ax2.grid(False)

    x1 = ndpd['Datum_avliden']
    x2 = np.arange(len(x1)/3)

    g = sns.barplot(data=ndpd.query("typ in ['Antal_avlidna']"), x=x1, y='antal', color=sns.xkcd_rgb["blue/green"], ax=ax, label='antal', zorder=2)
    sns.lineplot(data=ndpd.query("typ in ['rullande']"), x=x2, y='antal', color=sns.xkcd_rgb['blue/green'], ax=ax, label='rullande', linewidth=2, alpha=.5, zorder=1)
    sns.lineplot(data=ndpd.query("typ == 'kumulativ'"), x=x2, y='antal', ax=ax2, color='k', label='Kumulativa', linewidth=3, zorder=4)

    ax.fill_between(x2, ndpd.query("typ in ['rullande']")['antal'], alpha=0.5, color=sns.xkcd_rgb['light grey blue'])

    g.legend_.remove()
    h,l = ax.get_legend_handles_labels()
    h.reverse()
    h2, l2 = ax2.get_legend_handles_labels()
    plt.legend(loc='upper left', handles=h+h2, title='Avlidna', labels=['Registrerade', 'Rullande medel', 'Kumulativt'])

    ax.set_xlabel('Datum')
    ax.set_ylabel('Antal')
    ax2.set_ylabel('Antal totalt')

    ax.set_ylim(0,120)
    ax2.set_ylim(0,3600)
    ax2.set_yticks([0,600,1200,1800,2400,3000,3600])

    plt.savefig('graphs/deaths.png', bbox_inches='tight')

    return 'graphs/deaths.png'

if __name__ == "__main__":
    save_graph()
