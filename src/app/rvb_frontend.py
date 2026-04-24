import streamlit as st

class FormRvb():
    def __init__(self):
        self.user_inputs = {}            
        st.title("Parametri per calcolo Mutuo e Affitto") 
        with st.form("Parametri per Calcolo Mutuo e Affitto"):
            self.user_inputs["purchase_price"] = st.slider("Prezzo di acquisto", step = 10000, min_value = 50000, max_value = 1000000, value = 200000)
            self.user_inputs["sqm"] = st.number_input("Metri quadrati", min_value = 20, max_value = 300, step = 10, value = 100)
            self.user_inputs["condo_owner_fees_coeff"] = st.number_input(
                "Frazione percentuale del valore catastale in spese condomin_valueiali",
                value = 0.005,
                min_value = 0.0,
                max_value = 0.01,
                help = "Se il valore catastale è 100'000€ e 500€ sono le spese annuali di condomin_valueio a carico del proprietario, allora il valore è 0.005")
            self.user_inputs["notary_fees"] = st.number_input("Spese notarili", min_value = 0, max_value = 5000, step = 200, value = 1000)
            self.user_inputs["payback_years"] = st.number_input("Numero di anni di mutuo o di rientro da spese di acquisto", min_value = 1, max_value = 30, step = 5, value = 20)
            self.user_inputs["years_occurring_renovation"] = st.number_input("Numero di anni tra una ristrutturazione all'altra, ovvero quando l'immobile avrà perso il 30%% del suo valore", min_value = 10, max_value = 50, step = 10, value = 40, help = "Si è stimato che un immobile perda il 30 %% del suo valore ogni 40 anni.")
            self.user_inputs["mortgage_interest_rate"] = st.number_input("Tasso di interesse del mutuo. Assume valore 0 se l'acquisto è avvenuto in contanti", min_value = 0.0, max_value = 0.1, step = 0.001, value = 0.002)
            self.user_inputs["avg_invest_return"] = st.number_input("Tasso di ritorno del miglior investimento alternativo. Di default è il rendimento netto annuo del MSCI World. Assume valure 0 se non si investe.", min_value = 0.0, max_value = 0.2, step = 0.01, value = 0.05)
            self.user_inputs["buying_from_individual"] = st.radio("Vuoi acquistare da società o da un privato?", options = ['Azienda', 'Privato'], index = 1)
            submit = st.form_submit_button("Invia")
        self.submitted = submit