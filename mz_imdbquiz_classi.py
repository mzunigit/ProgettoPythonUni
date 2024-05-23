import random
import pandas as pd

class Inizio:
    """Introduzione al gioco ed alle opzioni disponibili"""

# Questa sezione funge da menu' principale del gioco, dove l'utente seleziona cosa vuole fare
# Vengono proposti due metodi statici che per ragioni organizzative vengono racchiusi in una classe
# Il gioco si sviluppera' nel modulo "mz_imdbquiz_runenv", dove l'unico codice necessario e' il richiamo a questa classe

    @staticmethod
    def principale(): # Metodo che fa partire il gioco
        statistiche = Statistiche() # Si inizializza un'istanza che accede alla classe Statistiche
        interfaccia = Interfaccia(statistiche) # Si inizializza un'istanza di Interfaccia che a sua volta accede a Statistiche 

        print(f"Ciao! Questo è un quiz per veri nerd del cinema!")
        print(f"Le domande sono basate sulle pellicole Top 2000 per IMDb")
        print(f"Scegli tra le seguenti opzioni:")
        
        opzioni = ["1. Nuova partita", "2. Visualizza statistiche", "3. Esci dal gioco"] # Selezione opzione
        print(f"\n".join(opzioni))

        while True:
            scelta = input("Cosa scegli? ")
            if scelta == "1":
                interfaccia.nuova_partita()
                break
            elif scelta == "2":
                statistiche.mostra_statistiche_gioco()
                break
            elif scelta == "3":
                print(f"Alla prossima!")
                break
            else:
                print(f"Scegli un'opzione valida")
                continue

    @staticmethod
    def domanda_reboot(): # Metodo che nei vari punti del programma permette di tornare all'inizio
        while True:
            print(f"Vuoi tornare all'inizio (Si/No)?")
            risposta = input("")
            if risposta.lower() == "si":
                Inizio.principale()
                break
            elif risposta.lower() == "no":
                print(f"Alla prossima!")
                break
            else:
                print(f"Scegliere un'opzione valida")
                continue

class Interfaccia:
    """Sistema di gioco con domande provenienti dal motore collegato al database"""

# Questa classe propone i vari step parte del gioco i quali interagiscono con le classi MotoreGioco, Inizio e Statistiche

    def __init__(self, statistiche):
        self.statistiche = statistiche # Questa variabile riprende l"istanza di Interfaccia in Inizio
        self.motore_gioco = MotoreGioco() # Si inizializza un"istanza che accede a MotoreGioco
    
    def nuova_partita(self):
        print(f"Prima di iniziare una nuova partita, inserisci il tuo nome")
        self.statistiche.aggiungi_giocatore() # Il nome del giocatore viene aggiunto al dizionario in Statistiche
        self.nome_giocatore = self.statistiche.nome_giocatore
        print(f"Iniziamo!")
        self.quiz()

    def quiz(self):
        titolo_film = random.choice(self.motore_gioco.df["Movie Name"])  # Seleziona un film casuale dal dataset
        domanda = self.motore_gioco.genera_domanda(titolo_film)

        print(domanda["domanda"])
        for i, opzioni in enumerate(domanda["opzioni"]): # Numerazione delle risposte a cui aggiungere 1 per ovviare all'indice 0
            print(f"{i + 1}. {opzioni}")

        while True:
            risposta_utente = input("Risposta: ")
            try:
                risposta_utente = int(risposta_utente) - 1
                if domanda["opzioni"][risposta_utente] == domanda["risposta_vera"]:
                    print(f"Risposta corretta!")
                    self.statistiche.aggiorna_statistiche(self.nome_giocatore, risposta_corretta = True)
                    break
                else:
                    print(f"Risposta errata! La risposta corretta era: {domanda["risposta_vera"]}")
                    self.statistiche.aggiorna_statistiche(self.nome_giocatore, risposta_corretta = False)
                    break
            except (ValueError, IndexError):
                print(f"Scegli un'opzione valida")
                continue

        self.statistiche.mostra_statistiche_giocatore(self.nome_giocatore) # Ad ogni risposta il giocatore vede i suoi punteggi

        while True:
            print(f"Passiamo alla prossima domanda (Si/No)?") # Ad ogni risposta il giocatore sceglie se procedere
            self.risposta = input("")
            if self.risposta.lower() == "si":
                self.quiz()
                break
            elif self.risposta.lower() == "no":
                Inizio.domanda_reboot()
                break
            else:
                print(f"Scegliere un'opzione valida")
                continue

class Statistiche:
    """Registro nomi dei giocatori, punteggi accumulati, domande affrontate, 
    totale risposte corrette e totale risposte errate"""

# Questa classe si occupera' di raccogliere i punteggi dei giocatori ed avere metodi da usare in altre classi

    statistiche_gioco = {"Nome Giocatore": [],
                         "Punteggio": [],
                         "Domande_totali": [],
                         "Risposte_corrette": [],
                         "Risposte_errate": []} # Si crea un dizionario che raccogliera' le statistiche dei giocatori

    def __init__(self):
        self.nome_giocatore = None # La variabile inizializza un nome nullo, che verra' sostituito dal giocatore

    def aggiungi_giocatore(self):
        self.nome_giocatore = input("Nome: ") # Metodo per aggiungere un nuovo giocatore
        if self.nome_giocatore not in Statistiche.statistiche_gioco["Nome Giocatore"]:
            Statistiche.statistiche_gioco["Nome Giocatore"].append(self.nome_giocatore)
            Statistiche.statistiche_gioco["Punteggio"].append(0)
            Statistiche.statistiche_gioco["Domande_totali"].append(0)
            Statistiche.statistiche_gioco["Risposte_corrette"].append(0)
            Statistiche.statistiche_gioco["Risposte_errate"].append(0)
            print(f"Giocatore {self.nome_giocatore} aggiunto con successo")
        else:
            print(f"Giocatore già esistente")

    def mostra_statistiche_gioco(self):
        if not Statistiche.statistiche_gioco["Nome Giocatore"]: # Metodo per mostrare le statistiche complessive
            print(f"Non ci sono statistiche")
        else:
            print(Statistiche.statistiche_gioco)
        Inizio.domanda_reboot()

    def mostra_statistiche_giocatore(self, nome_giocatore):
        if nome_giocatore in Statistiche.statistiche_gioco["Nome Giocatore"]: # Metodo per mostrare le statistiche del giocatore
            indice = Statistiche.statistiche_gioco["Nome Giocatore"].index(nome_giocatore)
            risultati_giocatore = {"Nome Giocatore": Statistiche.statistiche_gioco["Nome Giocatore"][indice],
                                   "Punteggio": Statistiche.statistiche_gioco["Punteggio"][indice],
                                   "Domande_totali": Statistiche.statistiche_gioco["Domande_totali"][indice],
                                   "Risposte_corrette": Statistiche.statistiche_gioco["Risposte_corrette"][indice],
                                   "Risposte_errate": Statistiche.statistiche_gioco["Risposte_errate"][indice]}
            print(f"Statistiche attuali per {nome_giocatore}: {risultati_giocatore}")
        else:
            print(f"Giocatore non presente nelle statistiche")

    def aggiorna_statistiche(self, nome_giocatore, risposta_corretta):
        if nome_giocatore in Statistiche.statistiche_gioco["Nome Giocatore"]: # Metodo per aggiornare le statistiche
            indice = Statistiche.statistiche_gioco["Nome Giocatore"].index(nome_giocatore)
            Statistiche.statistiche_gioco["Domande_totali"][indice] += 1
            if risposta_corretta:
                Statistiche.statistiche_gioco["Punteggio"][indice] += 1
                Statistiche.statistiche_gioco["Risposte_corrette"][indice] += 1
            else:
                Statistiche.statistiche_gioco["Risposte_errate"][indice] += 1
        else:
            print(f"Giocatore non trovato nelle statistiche")

class MotoreGioco:
    """Connessione al dataset IMDb. Segue randomizzazione domande che verranno restituite in Interfaccia"""

# Questa classe racchiude il motore pensante del gioco, il quale estrae informazioni dal dataset IMDb e le randomizza per le domande
    
    def __init__(self):
        file_path = "imdb_top_2000_movies.csv"
        print(f"Tentativo di caricamento file in: {file_path}")
        try:
            self.df = pd.read_csv(file_path, encoding="utf-8")
            print(f"File caricato con successo")
        except FileNotFoundError as errore:
            print(f"Errore: {errore}")
            raise
        except UnicodeDecodeError as errore:
            print(f"Errore di decodifica: {errore}")
            raise

    def recupera_info_film(self, titolo_film):
        film = self.df[self.df["Movie Name"] == titolo_film].iloc[0]
        info_film = {"titolo": film["Movie Name"],
                     "anno_uscita": film["Release Year"],
                     "durata": film["Duration"],
                     "genere": film["Genre"],
                     "regista": film["Director"],
                     "attori": film["Cast"],
                     "incassi": film["Gross"]}
        return info_film

    def genera_domanda(self, titolo_film):
        info = self.recupera_info_film(titolo_film) # Si generano dizionari con le possibilita' di domanda
        domande = [{"domanda": f"Qual è l'anno di uscita del film {info["titolo"]}?",
                    "risposta_vera": info["anno_uscita"],
                    "opzioni": self.genera_opzioni(info["anno_uscita"], "anno_uscita")}, # Si prendono gli argomenti per genera_opzioni
                   {"domanda": f"Qual è la durata, in minuti, del film {info["titolo"]}?",
                    "risposta_vera": info["durata"],
                    "opzioni": self.genera_opzioni(info["durata"], "durata")},
                   {"domanda": f"Qual è il genere del film {info["titolo"]}?",
                    "risposta_vera": info["genere"],
                    "opzioni": self.genera_opzioni(info["genere"], "genere")},
                   {"domanda": f"Chi è il regista del film {info["titolo"]}?",
                   "risposta_vera": info["regista"],
                   "opzioni": self.genera_opzioni(info["regista"], "regista")},
                   {"domanda": f"Qual è uno degli attori principali del film {info["titolo"]}?",
                    "risposta_vera": info["attori"],
                    "opzioni": self.genera_opzioni(info["attori"], "attori")},
                   {"domanda": f"Qual è l'incasso mondiale del film {info["titolo"]}?",
                    "risposta_vera": info["incassi"],
                    "opzioni": self.genera_opzioni(info["incassi"], "incassi")}]
        return random.choice(domande)

    def genera_opzioni(self, risposta_vera, categoria):
        opzioni = [risposta_vera] # Si genera una lista iniziale che contiene solo la risposta vera
        while len(opzioni) < 4: # Si generano 3 risposte false
            risposta_falsa = self.recupera_domande_false(categoria)
            if risposta_falsa not in opzioni:
                opzioni.append(risposta_falsa)  # Per evitare duplicati nelle risposte false
        random.shuffle(opzioni)
        return opzioni

    def recupera_domande_false(self, categoria):
        if categoria == "anno_uscita":
            return random.choice(self.df["Release Year"])
        elif categoria == "durata":
            return random.choice(self.df["Duration"])
        elif categoria == "genere":
            return random.choice(self.df["Genre"])
        elif categoria == "regista":
            return random.choice(self.df["Director"])
        elif categoria == "attori":
            return random.choice(self.df["Cast"])
        elif categoria == "incassi":
            return random.choice(self.df["Gross"])
