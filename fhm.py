import flattening
import deaths
import icu
import reported_cases
import deaths_per_region
import imgur_upload
import telegram_bot

links = {}

title_flattening = 'COVID-19, Are we flattening the curve?'
img_flattening = flattening.save_graph()
links['Kurvans riktning'] = imgur_upload.upload_file(img_flattening, title_flattening)

title_deaths = 'COVID-19 Deaths per day, Sweden'
img_deaths = deaths.save_graph()
links['Antal avlidna per dag'] = imgur_upload.upload_file(img_deaths, title_deaths)

title_icu = 'COVID-19 Daily admissions to ICU, Sweden'
img_icu = icu.save_graph()
links['Antal nyinskrivna på intensivvård per dag'] = imgur_upload.upload_file(img_icu, title_icu)

title_rc = 'COVID-19 Reported cases for 20 regions, Sweden'
img_rc = reported_cases.save_graph()
links['Rapporterade fall i 20 regioner'] = imgur_upload.upload_file(img_rc, title_rc)

title_rc = 'COVID-19 Reported deaths for 20 regions, Sweden'
img_rc = deaths_per_region.save_graph()
links['Rapporterade avlidna per dag i 20 regioner'] = imgur_upload.upload_file(img_rc, title_rc)

msg = '**Dagens grafer**:\n'
for key, val in links.items():
    # print(key+': '+val+'\n')
    msg = msg+f'\n{key}:\n{val}\n'

telegram_bot.send(msg)

