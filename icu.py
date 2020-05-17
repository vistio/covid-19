import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

def save_graph():
    file_name = 'Folkhalsomyndigheten_Covid19.xlsx'

    xl = pd.ExcelFile('data/'+file_name)
    #xl.sheet_names
    iva = xl.parse('Antal intensivvårdade per dag')

    iva.columns = ['date', 'daily']
    iva['date'] = iva['date'].dt.date
    iva['rolling'] = iva['daily'].rolling(10, center=True).mean()
    niva = pd.melt(iva, id_vars='date', var_name='typ', value_name='n')

    sns.set()

    plt.rcParams['patch.edgecolor'] = 'none'
    colors = ['blue/green', 'light grey blue']
    pal = sns.xkcd_palette(colors)
    sns.set_palette(pal)

    f, ax = plt.subplots(figsize=(16,8), dpi=300)


    x1 = niva.query('typ == "daily"')['date']
    x2 = np.arange(len(x1))

    g = sns.barplot(data=niva.query('typ == "daily"'), x=x1, y='n', ax=ax, zorder=2, label='Antal på IVA', color=sns.xkcd_rgb['blue/green'])
    sns.lineplot(data=niva.query('typ == "rolling"'), x=x2, y='n', ax=ax, zorder=1, label='Rullande medel')
    ax.fill_between(x2, niva.query('typ == "rolling"')['n'], alpha=0.5, color=sns.xkcd_rgb['light grey blue'])

    plt.xticks(rotation=90)
    ax.set_ylabel('Antal nyinskrivna på IVA')
    ax.set_xlabel('Datum')

    h, l = ax.get_legend_handles_labels()
    h.reverse()
    plt.legend(loc='upper left', title='Nyinskrivna på IVA', labels=['Dagligen', 'Rullande medel'], handles=h)

    plt.savefig('graphs/icu.png', bbox_inches='tight')

    return 'graphs/icu.png'

if __name__ == "__main__":
    save_graph()
