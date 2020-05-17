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
    cases = xl.parse('Antal per dag region')

    cases = cases[(cases['Statistikdatum'] > '2020-03-13')]
    cases['Statistikdatum'] = cases['Statistikdatum'].dt.date
    cases = cases.set_index('Statistikdatum')
    del cases['Totalt_antal_fall']
    cases = cases.fillna(0).astype('int32')
    #del cases['Stockholm']

    sns.set()
    # sns.set_context("notebook", font_scale=.8)

    # f, ax = plt.subplots(figsize=(10,10), dpi=300)
    # sns.heatmap(data=cases, ax=ax, annot=True, fmt='d', cmap='Blues')
    # plt.savefig('graphs/cases_heatmap.png', bbox_inches='tight')

    plt.rcParams['patch.edgecolor'] = 'none'
    colors = ['blue/green']
    pal = sns.xkcd_palette(colors)
    sns.set_palette(pal)

    f2, ax2 = plt.subplots(nrows=5, ncols=4, figsize=(12,12), dpi=200)

    regions = [
        'Stockholm',
        'Västra_Götaland',
        'Östergötland',
        'Sörmland',
        
        'Uppsala',
        'Örebro',
        'Dalarna',
        'Västmanland',
        
        'Jönköping',
        'Skåne',
        'Kronoberg',
        'Halland',
        
        'Gävleborg',
        'Västerbotten',
        'Norrbotten',
        'Jämtland_Härjedalen',
        
        'Kalmar',
        'Västernorrland',
        'Blekinge',
        'Värmland'
    ]

    g = [None] * len(regions)

    i, j = (0,0)
    for r in regions:
        g[i] = sns.barplot(data=cases[:-1], x=cases.index[:-1], y=r, ax=ax2[i][j], color=sns.xkcd_rgb['blue/green'])
        rolling = cases[r].rolling(10, center=False).mean()
        sns.lineplot(x=np.arange(len(cases.index[:-1])), y=rolling[:-1], ax=ax2[i][j], zorder=1, color=sns.xkcd_rgb['dark blue grey'])
        ax2[i][j].set_xlabel(r)
        # ax2[i][j].set_ylabel()
        if r == 'Stockholm' or r == 'Västra_Götaland':
            ax2[i][j].set_ylim(0,300)
        else:
            ax2[i][j].set_ylim(0,150)
        y_axis = ax2[i][j].axes.get_yaxis()
        y_label = y_axis.get_label()
        y_label.set_visible(False)
        i = i+1
        if i==5:
            j = j+1
            i = 0

    f2.suptitle('COVID-19 Reported cases from 2020-03-13 to ' + str(cases.index[-2]))
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    #tmp = plt.setp(ax2, xticks=[], ylabel=None, ylim=(0,300))
    tmp = plt.setp(ax2, xticks=[], ylabel='')

    plt.savefig('graphs/reported_cases.png', bbox_inches='tight')

    return 'graphs/reported_cases.png'

if __name__ == "__main__":
    save_graph()
