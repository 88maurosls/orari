import streamlit as st
import pandas as pd

class StreamlistSharing:
    def __init__(self):
        self.data = pd.DataFrame(columns=['Nome Dipendente', 'Ore di Lavoro'])

    def aggiungi_dipendente(self, nome, ore):
        self.data = self.data.append({'Nome Dipendente': nome, 'Ore di Lavoro': ore}, ignore_index=True)

    def mostra_streamlist(self):
        st.write(self.data)

    def totale_dipendenti(self):
        return len(self.data)

    def totale_ore_lavoro(self):
        return self.data['Ore di Lavoro'].sum()

# Creazione dell'oggetto StreamlistSharing
streamlist = StreamlistSharing()

# Interfaccia Streamlit
st.title("Streamlist Sharing")

# Form per aggiungere dipendenti
with st.form(key='aggiungi_dipendente'):
    nome = st.text_input("Nome Dipendente")
    ore = st.number_input("Ore di Lavoro", min_value=0, max_value=100, step=1)
    submit_button = st.form_submit_button(label='Aggiungi Dipendente')

    if submit_button:
        streamlist.aggiungi_dipendente(nome, ore)
        st.success(f"Dipendente {nome} aggiunto con {ore} ore di lavoro")

# Mostra streamlist attuale
st.header("Streamlist Attuale")
streamlist.mostra_streamlist()

# Mostra totale dipendenti e ore di lavoro
st.header("Totali")
st.write(f"Numero totale di dipendenti: {streamlist.totale_dipendenti()}")
st.write(f"Totale ore di lavoro: {streamlist.totale_ore_lavoro()}")
