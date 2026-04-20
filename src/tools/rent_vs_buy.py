# %% [markdown]
# # Mutuo o affitto?

# %%
from statistics import mean

# %% [markdown]
# *Location Data*

# %%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

driver = webdriver.Firefox()
driver.get("https://www1.agenziaentrate.gov.it/servizi/Consultazione/ricerca.htm")


# %%
def show_options(dropdown_xpath):
    options = Select(driver.find_element(By.XPATH, dropdown_xpath))
    for i, option in enumerate(options.options):
        print(i+1, '-', option.text)
    return options

# %%
def pick_option(options):
    option_idx = None
    while option_idx == None:
        try:
            option_idx = int(input("Scegli il numero associato alla tua provincia: "))
            option_idx -= 1
            if option_idx > len(options.options):
                raise ValueError
            return option_idx
        except ValueError:
            print("Valore non valido")
            option_idx = None

# %%
def select_and_click(options, selection):
    options.select_by_index(selection)
    button = driver.find_element(By.XPATH, "//input[@id = 'bottone_invio']")
    button.click()

# %%
province = show_options("//select[@id = 'pr']")
provincia = pick_option(province)
select_and_click(province, provincia)

# %%
comuni = show_options("//select[@id = 'co' and @name = 'co']")
comune = pick_option(comuni)
select_and_click(comuni, comune)

# %%
fasce = show_options("//select[@id = 'linkzonastrada' and @name = 'linkzonastrada']")
fascia = pick_option(fasce)
select_and_click(fasce, fascia)

# %%
utilizzi = Select(driver.find_element(By.XPATH, "//select[@id = 'utilizzo' and @name = 'utilizzo']"))
utilizzi.select_by_visible_text("Residenziale")
button = driver.find_element(By.XPATH, "//input[@id = 'bottone_invio']")
button.click()


# %%
row = driver.find_element(By.XPATH, "//tr[td[normalize-space()='Abitazioni civili']]").text.replace(',','.').rsplit(' ', maxsplit = 7)

# %%
driver.quit()

# %%
dati_zona = {
    'Tipo': row[0],
    'valore_medio_compravendita_mq': mean([
        float(row[2]),
        float(row[3])]
    ),
    'valore_medio_affitto_mq': mean([
        float(row[5]),
        float(row[6])]
    )
}

# %%
dati_zona['%_affitto_su_vendita'] = dati_zona["valore_medio_affitto_mq"] / dati_zona["valore_medio_compravendita_mq"]

# %%
dati_zona

# %% [markdown]
# # Calculations

# %%
prezzo_acquisto = 200000
rivalutazione_catastale = 2.18

perc_spese_condominio_proprietario = 0.005
acquisto_da_privato = False
spese_notarili = 1500
anni_cambio_casa = 20
anni_ristrutturazione = 40
avg_invest_y_return = 0.05
interessi_mutuo = 0.025


# %%
class Proprietario():
    def __init__(
                    self,
                    prezzo_acquisto,
                    rivalutazione_catastale,
                    perc_spese_condominio_proprietario,
                    acquisto_da_privato,
                    spese_notarili,
                    anni_cambio_casa,
                    anni_ristrutturazione,
                    avg_invest_y_return = 0,
                    interessi_mutuo = 0,
                ):

        self.valore_catastale = prezzo_acquisto / rivalutazione_catastale
        self.spese_condominio_proprietario = - (self.valore_catastale * perc_spese_condominio_proprietario)
        self.ristrutturazione = - self.valore_catastale / anni_ristrutturazione

        if acquisto_da_privato:
            imposta_registro = 0.02 * self.valore_catastale
            imposta_ipotecaria = 50
            imposta_catastale = 50
            visure_e_altri_oneri = 50
            self.imposte = imposta_registro + imposta_ipotecaria + imposta_catastale + visure_e_altri_oneri
        else:
            iva = 0.04 * prezzo_acquisto
            imposta_registro = 200
            imposta_ipotecaria = 200
            imposta_catastale = 200
            self.imposte = iva + imposta_registro + imposta_ipotecaria + imposta_catastale

        self.spese_acquisto = -(max(1000, self.imposte) + spese_notarili) / anni_cambio_casa

        self.investimenti = prezzo_acquisto * avg_invest_y_return
        self.interessi_mutuo = -(prezzo_acquisto * interessi_mutuo)

        self.totale = self.spese_condominio_proprietario + self.ristrutturazione + self.spese_acquisto + self.investimenti + self.interessi_mutuo

# %%
proprietario = Proprietario(
                            prezzo_acquisto,
                            rivalutazione_catastale,
                            perc_spese_condominio_proprietario,
                            acquisto_da_privato,
                            spese_notarili,
                            anni_cambio_casa,
                            anni_ristrutturazione)

# %%
proprietario.totale

# %%
perc_affitto_mensile_su_prezzo_vendita = dati_zona["%_affitto_su_vendita"]
avg_invest_y_return = 0.05
detrazione_affitto = 0

# %%
class PrendereInAffitto():
    def __init__(
                    self,
                    perc_affitto_mensile_su_prezzo_vendita,
                    prezzo_vendita_casa_omologa,
                    avg_invest_y_return,
                    detrazione_affitto
                ):
        
        self.affitto = (prezzo_vendita_casa_omologa * perc_affitto_mensile_su_prezzo_vendita)*-12
        self.rendita_investimenti = prezzo_vendita_casa_omologa * avg_invest_y_return
        self.detrazione_affitto = detrazione_affitto

        self.totale = self.affitto + self.rendita_investimenti + self.detrazione_affitto

# %%
inquilino = PrendereInAffitto(
    perc_affitto_mensile_su_prezzo_vendita,
    prezzo_acquisto,
    avg_invest_y_return,
    detrazione_affitto
)

# %%
inquilino.totale