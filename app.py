import pandas as pd

class StreamlistSharing:
    def __init__(self):
        self.data = pd.DataFrame(columns=['Nome Dipendente', 'Ore di Lavoro'])

    def aggiungi_dipendente(self, nome, ore):
        self.data = self.data.append({'Nome Dipendente': nome, 'Ore di Lavoro': ore}, ignore_index=True)

    def mostra_streamlist(self):
        print(self.data)

    def totale_dipendenti(self):
        return len(self.data)

    def totale_ore_lavoro(self):
        return self.data['Ore di Lavoro'].sum()

# Esempio di utilizzo del programma
streamlist = StreamlistSharing()
streamlist.aggiungi_dipendente('Mario Rossi', 40)
streamlist.aggiungi_dipendente('Luigi Bianchi', 35)

print("Streamlist attuale:")
streamlist.mostra_streamlist()

print(f"Numero totale di dipendenti: {streamlist.totale_dipendenti()}")
print(f"Totale ore di lavoro: {streamlist.totale_ore_lavoro()}")

