import tkinter as tk
from datetime import datetime
from tkinter import scrolledtext, messagebox, filedialog
import os
import json #für Einstellungen export

class Rednerliste:
    def __init__(self, master):
        self.master = master
        self.master.title("Rednerliste")
        self.master.attributes("-topmost", True)
        self.ansicht_standard_voll_links = f"{230}x{root.winfo_screenheight() - 80}+{root.winfo_x() - 8}+{master.winfo_y()}"
        self.ansicht_standard_voll_rechts = f"{230}x{root.winfo_screenheight() - 80}+{root.winfo_screenwidth() - 240}+{master.winfo_y()}"
        self.ansicht_standard_halb_links = f"{230}x{root.winfo_screenheight() // 2}+{root.winfo_x() - 8}+{master.winfo_y()}"
        self.ansicht_standard_halb_rechts = f"{230}x{root.winfo_screenheight() // 2}+{root.winfo_screenwidth() - 240}+{master.winfo_y()}"

        self.ansicht_standard_individuell_links = f"{230}x{self.master.winfo_height()}+{root.winfo_x() - 8}+{master.winfo_y()}"
        self.ansicht_standard_individuell_rechts = f"{230}x{self.master.winfo_height()}+{root.winfo_screenwidth() - 240}+{master.winfo_y()}"


        self.master.geometry(f"{230}x{root.winfo_screenheight() - 80}+{root.winfo_x() - 8}+{master.winfo_y()}")

        #Einstellungen für Settings import
        # beispiel um die Einstellung zu setzen:         self.ansicht_halb_var = tk.BooleanVar(value=self.settings['Button 1/2'])
        self.settings = {
#            'Fenster': True  # anpassen
            'Button 1/2': True,
            'Button !': True,
            'Button Zahnrad': True, #geht noch nicht, wenn false
#            'Rednerauswahl': True, #standard Redner eintragen macht keinen Sinn
            'Schriftgröße': '12',
            'Protokoll zeigen': False,
            'Trenner 1': ' - ',
            'Trenner 2': ' - ',
            'Zeitformat': '%H:%M:%S',
            'checkbox anwesend': True,
            'checkbox eingereiht': False,
            'checkbox gesprochen': True,
            'checkbox verlassen': True,
            'text anwesend': 'anwesend',
            'text eingereiht': 'eingereiht',
            'text gesprochen': 'gesprochen',
            'text verlassen': 'verlassen'
        }
        # Einstellungen laden aus Datei, wenn vorhanden
        self.load_settings()

        self.ansicht_halb_var = tk.BooleanVar(value=self.settings['Button 1/2'])  # 1/2-Button ist ausgeschaltet



        # Ereignisbindung für das Schließen des Fensters
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    # Konfiguriere das Grid, um proportionale Größenveränderungen zu ermöglichen
        master.rowconfigure(0, weight=0)
        master.rowconfigure(1, weight=0)
        master.rowconfigure(3, weight=1)
        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)

        
#Anordnung oben Menü (row=1)

    # Button Standard Ansicht links
        standard_ansicht_links_button = tk.Button(master, text="<-", command=self.standard_ansicht_links)
        standard_ansicht_links_button.grid(row=1, column=0, columnspan=1, padx=10, pady=1, sticky="nw")
        self.tooltip = ToolTip(standard_ansicht_links_button, "Standard Ansicht linksseitig") # tooltip 

    # Button Standard Ansicht rechts
        standard_ansicht_rechts_button = tk.Button(master, text="->", command=self.standard_ansicht_rechts)
        standard_ansicht_rechts_button.grid(row=1, column=0, columnspan=2, padx=(65,0), pady=0, sticky="nw")
        self.tooltip = ToolTip(standard_ansicht_rechts_button, "Standard Ansicht rechtsseitig") # tooltip 

    # Button ! im Vordergrund
        self.ansicht_vordergrund_var = tk.BooleanVar(value=self.settings['Button !'])
        self.ansicht_vordergrund_button = tk.Button(master, text="⚠️", command=self.toggle_ansicht_vordergrund,
                                                  relief=tk.SUNKEN if self.ansicht_vordergrund_var.get() else tk.RAISED)
        self.ansicht_vordergrund_button.grid(row=1, column=0, columnspan=2, padx=(10, 10), pady=1, sticky="n")
        self.tooltip = ToolTip(self.ansicht_vordergrund_button, "zeigt die Rednerliste immer über anderen Programmen")

    # Hilfe
        self.hilfe_button = tk.Button(master, text="❓", command=self.hilfe_anzeigen)
        self.hilfe_button.grid(row=1, column=1, columnspan=1, padx=(0,40), pady=1, sticky="ne")
        self.tooltip = ToolTip(self.hilfe_button, "Hilfe") # tooltip 

    # Button "Einstellungen"
        self.einstellungen_var = tk.BooleanVar(value=self.settings['Button Zahnrad'])
#        self.einstellungen_var.set(True)
        self.einstellungen_button = tk.Button(master, text="⚙️", command=self.toggle_einstellungen,
                                                  relief=tk.SUNKEN if self.einstellungen_var.get() else tk.RAISED)
        self.einstellungen_button.grid(row=1, column=1, columnspan=1, padx=(0,10), pady=1, sticky="ne")
        self.tooltip = ToolTip(self.einstellungen_button, "ein: Einstellungen \naus: Basis Ansicht")


    # Button 1/2 halbe Bildschirmhöhe
        self.ansicht_halb_button = tk.Button(master, text="½", command=self.toggle_bildschirmhoehe,
                                                  relief=tk.SUNKEN if self.ansicht_halb_var.get() else tk.RAISED)
        self.ansicht_halb_button.grid(row=1, column=0, columnspan=1, padx=(40,0), pady=1, sticky="nw")
        self.tooltip = ToolTip(self.ansicht_halb_button, "Bildschirmhöhe im einfachen Modus \n ein: halb \n aus: voll")

    # Button Einstellungen speichern
        self.save_button = tk.Button(root, text='💾', command=self.save_settings)
        self.save_button.grid(row=1, column=1, columnspan=1, padx=(0,70), pady=1, sticky="ne")
        self.tooltip = ToolTip(self.save_button, "Speichert die Einstellungen in settings.txt\nund lädt diese bei Programmstart.\nFunktioniert bisher nicht!!!")
        self.save_button.grid_forget() #versteckt den Button

#Kernansicht (Row=2 bis row=6)
  
    #Rednerauswahl
        self.rednerauswahl_label = tk.Label(master, text="Rednerauswahl")
        self.rednerauswahl_label.grid(row=2, column=0, padx=10, pady=5, sticky="wn")

        self.rednerauswahl_listbox = tk.Listbox(master, selectbackground='lightblue', height=15, width=15)
        self.rednerauswahl_listbox.grid(row=3, column=0, padx=10, pady=0, sticky="wens")
        self.rednerauswahl_listbox.bind('<Double-Button-1>', self.redner_auswahl)
        self.rednerauswahl_listbox.bind('<Delete>', self.redner_loeschen)
        self.tooltip = ToolTip(self.rednerauswahl_label, "Doppelklick setzt auf Rednerliste") # tooltip 
        self.rednerauswahl_listbox.configure(font=('Helvetica', 12)) #korrigiert ungleiche Breite von Rednerliste und Reihenfolge bei Programmstart

    #Reihenfolge
        self.reihenfolge_label = tk.Label(master, text="Reihenfolge")
        self.reihenfolge_label.grid(row=2, column=1, padx=10, pady=5, sticky="wn")

        self.reihenfolge_listbox = tk.Listbox(master, selectbackground='lightblue', height=15, width=15)
        self.reihenfolge_listbox.grid(row=3, column=1, padx=10, pady=0, sticky="wens")
        self.reihenfolge_listbox.bind('<Double-Button-1>', self.reihenfolge_auswahl)

        self.reihenfolge_listbox.bind('<ButtonPress-1>', self.start_drag)
        self.reihenfolge_listbox.bind('<B1-Motion>', self.on_drag)
        self.reihenfolge_listbox.bind('<ButtonRelease-1>', self.stop_drag)
        self.tooltip = ToolTip(self.reihenfolge_label, "Doppelklick entfernt von Rednerliste") # tooltip 
        self.reihenfolge_listbox.configure(font=('Helvetica', 12)) #korrigiert ungleiche Breite von Rednerliste und Reihenfolge bei Programmstart

    #Protokoll

        self.protokoll_text = scrolledtext.ScrolledText(master, height=5, width=25)
        self.protokoll_text.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="wens")
#        if self.protokoll_zeigen_var.get():  
#            self.protokoll_text.grid() #blendet Protokoll Textbox ein
#        else:
#            self.protokoll_text.grid_remove()
        
        initial_date_entry = datetime.now().strftime("%Y-%m-%d")
        self.protokoll_text.insert(tk.END, initial_date_entry + " Protokoll erstellt\n")
        
    #neue Redner    
        self.redner_erstellen_text = scrolledtext.ScrolledText(master, height=3, width=15)
        self.redner_erstellen_text.grid(row=7, column=0, padx=10, pady=5, sticky="wens")
        
        self.redner_erstellen_text.bind("<Return>", lambda event: self.redner_erstellen()) #auf Return Redner erstellen

        self.redner_label = tk.Label(master, text="neue Redner")
        self.redner_label.grid(row=7, column=1, columnspan=1, padx=10, pady=5, sticky="nw")


        self.redner_erstellen_button = tk.Button(master, text="erstellen", command=self.redner_erstellen)
        self.redner_erstellen_button.grid(row=7, column=1, columnspan=1, padx=10, pady=5, sticky="sw")
        self.tooltip = ToolTip(self.redner_erstellen_button, "legt die neuen Redner aus der 'neue Redner' Box an\noder Eingabe Taste") # tooltip 

        self.loeschen_button = tk.Button(master, text="löschen", command=self.redner_loeschen)
        self.loeschen_button.grid(row=7, column=1, columnspan=1, padx=10, pady=5, sticky="se")
        self.tooltip = ToolTip(self.loeschen_button, "löscht den ausgewählten Redner in der Rednerauswahl\noder Entfernen Taste") # tooltip 



#Anordnung unten Einstellungen (row=9

    # Schieberegler für Schriftgröße für Listboxen
        self.schriftgroesse_var = tk.IntVar(value=self.settings['Schriftgröße'])  # Initialwert der Schriftgröße
        self.schriftgroesse_slider = tk.Scale(master, from_=12, to=40, orient=tk.HORIZONTAL, label="Schriftgröße der Redner", variable=self.schriftgroesse_var, command=self.update_schriftgroesse)
        self.schriftgroesse_slider.grid(row=9, column=0, columnspan=2, padx=10, pady=5, sticky="wens")
        self.tooltip = ToolTip(self.schriftgroesse_slider, "verändert die Schriftgröße in Rednerauswahl und Reihenfolge") # tooltip 

    # Protokoll Einstellungen (row=11 bis row=16)        
 
        #Protokoll zeigen
        self.protokoll_zeigen_var = tk.BooleanVar(value=self.settings['Protokoll zeigen'])
        self.protokoll_zeigen_checkbox = tk.Checkbutton(master, text="zeige Protokoll", variable=self.protokoll_zeigen_var, command=self.toggle_protokoll_zeigen) # unsicher ob command geht
        self.protokoll_zeigen_checkbox.grid(row=11, column=0, columnspan=2, padx=5, pady=5)
        self.tooltip = ToolTip(self.protokoll_zeigen_checkbox, "Zeigt das Protokoll im Basis Modus an,\nund dessen Einstellungen in den Einstellungen") # tooltip 

        #Trenner
        self.trenner_zeit_label = tk.Label(master, text="Zeit")
        self.trenner_zeit_label.grid(row=12, column=0, columnspan=1, padx=(20,0), pady=5, sticky="w")
        self.trenner_redner_label = tk.Label(master, text="Redner")
        self.trenner_redner_label.grid(row=12, column=0, columnspan=2, padx=0, pady=5)
        self.trenner_status_label = tk.Label(master, text="Status")
        self.trenner_status_label.grid(row=12, column=1, columnspan=1, padx=(0,20), pady=5, sticky="e")

        self.trenner_1_var = tk.Entry(master, width=2)
        self.trenner_1_var.grid(row=12, column=0, padx=(20,0), pady=5)
        self.trenner_1_var.insert(0, self.settings['Trenner 1'])
        self.tooltip = ToolTip(self.trenner_1_var, "Im Protokoll Zeichen zwischen Zeit und Redner") # tooltip 

        self.trenner_2_var = tk.Entry(master, width=2)
        self.trenner_2_var.grid(row=12, column=1, padx=(0,30), pady=5)
        self.trenner_2_var.insert(0, self.settings['Trenner 2'])
        self.tooltip = ToolTip(self.trenner_2_var, "Im Protokoll Zeichen zwischen Redner und Status") # tooltip 


    # Datumsformat einstellen - links

        # Textbox für die Eingabe des Zeitformats
        self.zeit_format_label = tk.Label(master, text="Zeitformat:")
        self.zeit_format_label.grid(row=13, column=0, padx=10, pady=5, sticky="w")

        self.zeit_format_var = tk.Entry(master, width=15)
        self.zeit_format_var.insert(0, self.settings['Zeitformat'])
        self.zeit_format_var.grid(row=14, column=0, padx=10, pady=5, sticky="we")
        self.tooltip = ToolTip(self.zeit_format_var, "setzt das Zeitformat für die Protokolleinträge\n%H:%M:%S") # tooltip 


        # Textbox für die Ausgabe des formatierten Datums
        self.zeit_text_label = tk.Label(master, text="Beispiel:")
        self.zeit_text_label.grid(row=15, column=0, padx=10, pady=5, sticky="w")

        self.zeit_text_var = tk.Text(master, height=1, width=15)
        self.zeit_text_var.grid(row=16, column=0, padx=10, pady=5, sticky="we")
        self.tooltip = ToolTip(self.zeit_text_var, "zeigt ein Beispiel für das Zeitformat für die Protokolleinträge") # tooltip 

        # Ereignisbindung für die Aktualisierung der Ausgabe-Textbox
        self.zeit_format_var.bind("<KeyRelease>", self.update_zeit_text)
        self.zeit_format_var.bind("<ButtonRelease-1>", self.update_zeit_text)
        self.update_zeit_text()
        
    #Checkboxen rechts
        self.protokoll_checkbox_anwesend = tk.BooleanVar(value=self.settings['checkbox anwesend'])
        self.protokoll_checkbox_eingereiht = tk.BooleanVar(value=self.settings['checkbox eingereiht'])
        self.protokoll_checkbox_gesprochen = tk.BooleanVar(value=self.settings['checkbox gesprochen'])
        self.protokoll_checkbox_verlassen = tk.BooleanVar(value=self.settings['checkbox verlassen'])

        self.anwesend_checkbox_var = tk.Checkbutton(master, variable=self.protokoll_checkbox_anwesend)
        self.anwesend_checkbox_var.grid(row=13, column=1, padx=(0), pady=5, sticky="w")
        self.tooltip = ToolTip(self.anwesend_checkbox_var, "Trägt neu erstellte (anwesende) Redner im Protokoll ein") # tooltip 

        self.anwesend_text_var = tk.Entry(master, width=10)
        self.anwesend_text_var.grid(row=13, column=1, padx=(30,0), pady=5, sticky="we")
        self.anwesend_text_var.insert(0, self.settings['text anwesend'])
        self.tooltip = ToolTip(self.anwesend_text_var, "das Wort 'anwesend' kann geändert werden") # tooltip 

        
        self.eingereiht_checkbox_var = tk.Checkbutton(master, variable=self.protokoll_checkbox_eingereiht)
        self.eingereiht_checkbox_var.grid(row=14, column=1, padx=(0), pady=5, sticky="w")
        self.tooltip = ToolTip(self.eingereiht_checkbox_var, "Trägt in Reihenfolge eingereihte Redner im Protokoll ein") # tooltip 

        self.eingereiht_text_var = tk.Entry(master, width=10)
        self.eingereiht_text_var.grid(row=14, column=1, padx=(30,0), pady=5, sticky="we")
        self.eingereiht_text_var.insert(0, self.settings['text eingereiht'])
        self.tooltip = ToolTip(self.eingereiht_text_var, "das Wort 'eingereiht' kann geändert werden") # tooltip 


        self.gesprochen_checkbox_var = tk.Checkbutton(master, variable=self.protokoll_checkbox_gesprochen)
        self.gesprochen_checkbox_var.grid(row=15, column=1, padx=(0), pady=5, sticky="w")
        self.tooltip = ToolTip(self.gesprochen_checkbox_var, "Trägt von Reihenfolge entfernte (gesprochene) Redner im Protokoll ein.") # tooltip 

        self.gesprochen_text_var = tk.Entry(master, width=10)
        self.gesprochen_text_var.grid(row=15, column=1, padx=(30,0), pady=5, sticky="we")
        self.gesprochen_text_var.insert(0, self.settings['text gesprochen'])
        self.tooltip = ToolTip(self.gesprochen_text_var, "das Wort 'gesprochen' kann geändert werden") # tooltip 


        self.geloescht_checkbox_var = tk.Checkbutton(master, variable=self.protokoll_checkbox_verlassen)
        self.geloescht_checkbox_var.grid(row=16, column=1, padx=(0), pady=5, sticky="w")
        self.tooltip = ToolTip(self.geloescht_checkbox_var, "Trägt aus Reihenfolge gelöschte (verlassene) Redner im Protokoll ein") # tooltip 

        self.geloescht_text_var = tk.Entry(master, width=10)
        self.geloescht_text_var.grid(row=16, column=1, padx=(30,0), pady=5, sticky="we")
        self.geloescht_text_var.insert(0, self.settings['text verlassen'])
        self.tooltip = ToolTip(self.geloescht_text_var, "das Wort 'gelöscht' kann geändert werden") # tooltip 

    
    #Funktionen
    
        # Funktion zum Ein- und Ausblenden der EinstellungsWidgets
        self.einstellungen_widgets = [
            self.redner_erstellen_text,
            self.protokoll_zeigen_checkbox,
            self.ansicht_vordergrund_button,   # ggf. mit # am Zeilenanfang ausblenden
#            self.save_button, # ggf. mit # am Zeilenanfang ausblenden
            self.hilfe_button, # ggf. mit # am Zeilenanfang ausblenden
            self.redner_label,
            self.redner_erstellen_button,
            self.loeschen_button,
            self.schriftgroesse_slider,
        ]

        # Funktion zum Ein- und Ausblenden der Protokoll Einstellungen Widgets
        self.protokoll_zeigen_widgets = [
            self.anwesend_checkbox_var,
            self.eingereiht_checkbox_var,
            self.gesprochen_checkbox_var,
            self.geloescht_checkbox_var,
            self.anwesend_text_var,
            self.eingereiht_text_var,
            self.gesprochen_text_var,
            self.geloescht_text_var,
            self.trenner_zeit_label,
            self.trenner_redner_label,
            self.trenner_status_label,
            self.trenner_1_var,
            self.trenner_2_var,
            self.zeit_format_var,
            self.zeit_format_label,
            self.zeit_text_var,
            self.zeit_text_label
        ]

        # Funktion um Protokoll Einstellungen zu zeigen
        if self.protokoll_zeigen_var.get() and not self.einstellungen_var.get():  
            for widget in self.protokoll_zeigen_widgets:
                widget.grid()
            self.protokoll_zeigen_widgets.grid()
            self.protokoll_text.grid()
        else:
            for widget in self.protokoll_zeigen_widgets:
                widget.grid_remove()
            self.protokoll_text.grid_remove()
       
       # Funktion um Einstellungen rot oder hellgrau anzuzeigen
        if self.einstellungen_var.get():  # Einstellungen aktiviert
            self.einstellungen_button.config(background="#FFAAAA")
        else:                         # Einstellungen deaktiviert
            self.einstellungen_button.config(background="lightgrey")
       

# Funktionen   
# Schalter-Buttons
    def toggle_ansicht_vordergrund(self):
        self.ansicht_vordergrund_var.set(not self.ansicht_vordergrund_var.get())  # Umschalten des Zustands des Schalter-Buttons
        self.ansicht_vordergrund_button.config(relief=tk.SUNKEN if self.ansicht_vordergrund_var.get() else tk.RAISED)  # Ändere das Relief des Buttons basierend auf dem aktualisierten Zustand

        self.master.attributes("-topmost", self.ansicht_vordergrund_var.get())

    def toggle_bildschirmhoehe(self):
        self.ansicht_halb_var.set(not self.ansicht_halb_var.get())  # Umschalten des Zustands des Schalter-Buttons
        self.ansicht_halb_button.config(relief=tk.SUNKEN if self.ansicht_halb_var.get() else tk.RAISED)  # Ändere das Relief des Buttons basierend auf dem aktualisierten Zustand

        # Überprüfe den Zustand des Schalter-Buttons
        if not self.einstellungen_var.get():
            if self.ansicht_halb_var.get():
                # Ändere die Bildschirmhöhe auf die Hälfte des ursprünglichen Werts
                self.master.geometry(f"{self.master.winfo_width()}x{self.master.winfo_screenheight() // 2}+{self.master.winfo_x()}+{self.master.winfo_y()}")
            else:
                # Verwende die ursprüngliche Bildschirmhöhe
                self.master.geometry(f"{self.master.winfo_width()}x{self.master.winfo_screenheight() - 80}+{self.master.winfo_x()}+{self.master.winfo_y()}")
        else:
            # Wenn Einstellungen aktiviert ist, ignoriere die Änderung der Bildschirmhöhe
            pass

    def standard_ansicht_links(self):
        self.master.state('normal') #wenn zoomed/maximiert, muss erst das Fenster wiederhergestellt werden.
        self.master.geometry(f"{230}x{self.master.winfo_height()}+{-8}+{0}")
    
    def standard_ansicht_rechts(self):
        self.master.state('normal')  #wenn zoomed/maximiert, muss erst das Fenster wiederhergestellt werden.
        self.master.geometry(f"{230}x{self.master.winfo_height()}+{root.winfo_screenwidth() - 240}+{0}")
        
    def toggle_einstellungen(self):
        self.einstellungen_var.set(not self.einstellungen_var.get())  # Umschalten des Zustands des Schalter-Buttons
        self.einstellungen_button.config(relief=tk.SUNKEN if self.einstellungen_var.get() else tk.RAISED)

        #Farbe rot
        if self.einstellungen_var.get():  # Einstellungen aktiviert
            self.einstellungen_button.config(background="#FFAAAA")
        else:                         # Einstellungen deaktiviert
            self.einstellungen_button.config(background="lightgrey")
        
        #Bildschirmhöhe
        if self.einstellungen_var.get():  # Einstellungen aktiviert
            self.screen_height = root.winfo_screenheight() - 80
        else:                         # Einstellungen deaktiviert
            if self.ansicht_halb_var.get():
                self.screen_height = root.winfo_screenheight() // 2
            else:
                self.screen_height = root.winfo_screenheight() - 80
        self.master.geometry(f"{self.master.winfo_width()}x{self.screen_height}+{self.master.winfo_x()}+{self.master.winfo_y()}") #aktualiesiert fenstermaße mit neuer screenhigh

        # Elemente zeigen
        if self.einstellungen_var.get():  # Einstellungen aktiviert
            if self.protokoll_zeigen_var.get(): #Protokoll zeigen aktiviert
                for widget in self.einstellungen_widgets:  #Einstellungen
                    widget.grid()
                for widget in self.protokoll_zeigen_widgets: #Protokoll Einstellungen
                    widget.grid()
                self.protokoll_text.grid()#Protokoll Text
            else:                               #Protokoll zeigen deaktiviert
                for widget in self.einstellungen_widgets:  #Einstellungen
                    widget.grid()
                for widget in self.protokoll_zeigen_widgets: #Protokoll Einstellungen
                    widget.grid_remove()
                self.protokoll_text.grid_remove()#Protokoll Text
        else:                            # Einstellungen deaktiviert
            if self.protokoll_zeigen_var.get(): #Protokoll zeigen aktiviert
                for widget in self.einstellungen_widgets:  #Einstellungen
                    widget.grid_remove()
                for widget in self.protokoll_zeigen_widgets: #Protokoll Einstellungen
                    widget.grid_remove()
                self.protokoll_text.grid()#Protokoll Text
            else:                               #Protokoll zeigen deaktiviert
                for widget in self.einstellungen_widgets:  #Einstellungen
                    widget.grid_remove()
                for widget in self.protokoll_zeigen_widgets: #Protokoll Einstellungen
                    widget.grid_remove()
                self.protokoll_text.grid_remove()#Protokoll Text

    def toggle_protokoll_zeigen(self):   #fertig, checkbox funktioniert wie vorgesehen.
        if self.protokoll_zeigen_var.get():  
            for widget in self.protokoll_zeigen_widgets:
                widget.grid()
            self.protokoll_text.grid() #blendet Protokoll Textbox ein
        else: # Einstellungen deaktiviert
            for widget in self.protokoll_zeigen_widgets:  
                widget.grid_remove()
            self.protokoll_text.grid_remove() #blendet Protokoll Textbox aus




#Textfelder    
    def update_zeit_text(self, event=None):
        try:
            input_format = self.zeit_format_var.get()
            current_time = datetime.now().strftime(input_format)
            self.zeit_text_var.delete(1.0, tk.END)
            self.zeit_text_var.insert(tk.END, current_time)
            return current_time  # Rückgabe des aktuellen Datumsformats
        except ValueError:
            self.zeit_text_var.delete(1.0, tk.END)
            self.zeit_text_var.insert(tk.END, "Ungültiges Datumsformat")


            

    def hilfe_anzeigen(self):
        hilfe_text = ("Rednerliste schafft Überblick, wer wann an der Reihe ist zu Reden. Das geht so:\n\n"
                      "Kopiere alle deine Redner untereinander in die 'Neue Redner' Box und klicke 'Redner erstellen' oder Enter.\n" 
                      "Wechsle in die Basis Ansicht, indem du den Einstellungen Knopf deaktivierst.\n"
                      "Doppelklicke auf den nächsten Redner in der Rednerauswahl. Verschiebe ggf. die Reihenfolge mit der Maus in der Reihenfolge.\n"
                      "Doppelklicke auf den Redner in der Reihenfolge, der fertig gesprochen hat.\n"
                      "Wenn du ein Protokoll benötigst, aktiviere dies in den Einstellungen ganz unten.\n"
                      "\n"
                      "Programmiert von Dr. Burkhard Strauß mit viel Hilfe initial von ChatGPT und notepad++.\n"
                      "Findest du das Programm gut, spende an KLUG oder Github. \n"
                      "\n"
                      "kopiere folgende Namen zum testen:\n"
                      "\n"
                      "Albert\n"
                      "Burkhard\n"
                      "Cleopatra\n"
                      "Denise\n"
                      "Emil\n"
                      "\n"
                      "Zeitformat:\n"
                      "%Y-%m-%d %H:%M:%S\n"
                      "Jahr-Monat-Tag Stunden:Minuten:Sekunden\n"
                      "")
        hilfe_fenster = tk.Toplevel(self.master)
        hilfe_fenster.attributes("-topmost", True)  # Bring das Hilfefenster in den Vordergrund
        hilfe_fenster.title("Hilfe")

        hilfe_textbox = scrolledtext.ScrolledText(hilfe_fenster, width=50, wrap=tk.WORD, font=("Helvetica", 12), height=30)
        
        hilfe_textbox.insert(tk.END, hilfe_text)
        hilfe_textbox.config(state=tk.DISABLED)  # Verhindert die Bearbeitung des Textes
        hilfe_textbox.pack()

        

        
    def redner_auswahl(self, event):
        current_time = self.update_zeit_text()
        index = self.rednerauswahl_listbox.curselection()
        if index:
            redner = self.rednerauswahl_listbox.get(index)
            self.rednerauswahl_listbox.delete(index)
            if redner not in self.reihenfolge_listbox.get(0, tk.END):
                self.reihenfolge_listbox.insert(tk.END, redner)
                if self.protokoll_checkbox_eingereiht.get():
                    self.protokoll_text.insert(tk.END, f"{current_time}{self.trenner_1_var.get()}{redner}{self.trenner_2_var.get()}{self.eingereiht_text_var.get()}\n")

    def reihenfolge_auswahl(self, event):
        current_time = self.update_zeit_text()
        index = self.reihenfolge_listbox.curselection()
        if index:
            redner = self.reihenfolge_listbox.get(index)
            self.reihenfolge_listbox.delete(index)
            if redner not in self.rednerauswahl_listbox.get(0, tk.END):
                self.rednerauswahl_listbox.insert(tk.END, redner)
                self.sortiere_rednerauswahl()
                if self.protokoll_checkbox_gesprochen.get():
                    self.protokoll_text.insert(tk.END, f"{current_time}{self.trenner_1_var.get()}{redner}{self.trenner_2_var.get()}{self.gesprochen_text_var.get()}\n")

    def redner_erstellen(self):
        current_time = self.update_zeit_text()
        eingabe_text = self.redner_erstellen_text.get("1.0", tk.END)
        redner_liste_var = eingabe_text.split("\n")
        for redner in redner_liste_var:
            if redner:
                if redner not in self.rednerauswahl_listbox.get(0, tk.END) and redner not in self.reihenfolge_listbox.get(0, tk.END):
                    self.rednerauswahl_listbox.insert(tk.END, redner)
                    self.sortiere_rednerauswahl()
                    if self.protokoll_checkbox_anwesend.get():
                        self.protokoll_text.insert(tk.END, f"{current_time}{self.trenner_1_var.get()}{redner}{self.trenner_2_var.get()}{self.anwesend_text_var.get()}\n")
        self.redner_erstellen_text.delete("1.0", tk.END)



    def redner_loeschen(self, event=None):
        current_time = self.update_zeit_text()
        index = self.rednerauswahl_listbox.curselection()
        if index:
            redner = self.rednerauswahl_listbox.get(index)
            self.rednerauswahl_listbox.delete(index)
            if self.protokoll_checkbox_verlassen.get():
               self.protokoll_text.insert(tk.END, f"{current_time}{self.trenner_1_var.get()}{redner}{self.trenner_2_var.get()}{self.geloescht_text_var.get()}\n")

    def start_drag(self, event):
        index = self.reihenfolge_listbox.nearest(event.y)
        self.drag_data = {'index': index, 'text': self.reihenfolge_listbox.get(index)}
        self.reihenfolge_listbox._configure('DND', background='lightblue')
        self.reihenfolge_listbox.tag_add('DND', index)

    def on_drag(self, event):
        y = event.y
        index_above = self.reihenfolge_listbox.nearest(y)
        index_dragged = self.drag_data['index']
        if index_above != index_dragged:
            self.reihenfolge_listbox.delete(index_dragged)
            self.reihenfolge_listbox.insert(index_above, self.drag_data['text'])
            self.drag_data['index'] = index_above

    def stop_drag(self, event):
        self.reihenfolge_listbox._configure('DND', background='white')
        self.reihenfolge_listbox.tag_remove('DND', 0, tk.END)




    def update_schriftgroesse(self, event=None):
        # Aktualisiere die Schriftgröße der Listboxen basierend auf dem Wert des Schiebereglers
        new_font_size = self.schriftgroesse_var.get()
        self.rednerauswahl_listbox.configure(font=('Helvetica', new_font_size))
        self.reihenfolge_listbox.configure(font=('Helvetica', new_font_size))

            
    def sortiere_rednerauswahl(self):
        redner_liste_var = sorted(self.rednerauswahl_listbox.get(0, tk.END))
        self.rednerauswahl_listbox.delete(0, tk.END)
        for redner in redner_liste_var:
            self.rednerauswahl_listbox.insert(tk.END, redner)
            
# Beim Schließen die Auswahlbuttons:
    def on_closing(self):
        # Öffne ein Popup-Fenster mit den gewünschten Buttons
        confirm_close_window = tk.Toplevel(self.master)
        confirm_close_window.title("Bestätigung")
        self.master.attributes("-topmost", False) #Schließen Fenster ist im Vordergrund

        label = tk.Label(confirm_close_window, text="Beenden und Protokoll")
        label.pack(pady=10)

        save_button = tk.Button(confirm_close_window, text="speichern", command=self.save_protocol)
        save_button.pack(pady=5)

        copy_button = tk.Button(confirm_close_window, text="kopieren", command=self.copy_protocol)
        copy_button.pack(pady=5)

        close_without_saving_button = tk.Button(confirm_close_window, text="nicht speichern", command=self.close_without_saving)
        close_without_saving_button.pack(pady=5)


    def save_protocol(self):
        initial_dir = os.path.expanduser("~/Downloads")  # Ausgangsverzeichnis ist der Downloads-Ordner

        current_time = datetime.now().strftime("%Y-%m-%d %H-%M")
        protocol_filename = f"Protokoll {current_time}.txt"

        # Dialog zum Auswählen des Speicherorts anzeigen
        file_path = filedialog.asksaveasfilename(
            initialdir=initial_dir,
            initialfile=protocol_filename,  # Vorbelegter Dateiname
            defaultextension=".txt",
            filetypes=[("Textdateien", "*.txt"), ("Alle Dateien", "*.*")],
            title="Protokoll speichern"
        )

        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(self.protokoll_text.get("1.0", tk.END))

                messagebox.showinfo("Erfolg", f"Protokoll wurde in '{file_path}' gespeichert.")

                # Ordner öffnen
                folder_path = os.path.dirname(file_path)
                os.system(f"start {folder_path}")  # Für Windows
                # Alternativ für Linux/Mac: os.system(f"open {folder_path}")

            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Speichern des Protokolls: {e}")

            self.master.destroy()
            
            
    def copy_protocol(self):
        # Kopiere das Protokoll in die Zwischenablage
        self.master.clipboard_clear()
        self.master.clipboard_append(self.protokoll_text.get("1.0", tk.END))
        self.master.update()

        messagebox.showinfo("Erfolg", "Protokoll wurde in die Zwischenablage kopiert.")
        self.master.destroy()
        
    def close_without_saving(self):
        # Schließe das Programm ohne Protokoll zu speichern
        self.master.destroy()
            
# Einstellungen speichern und laden
    def save_settings(self):
        # Aktuelle Einstellungen aktualisieren
        self.settings['Button 1/2'] = self.ansicht_halb_var.get()
        self.settings['Button !'] = self.ansicht_vordergrund_var.get()
        self.settings['Button Zahnrad'] = self.einstellungen_var.get()
#        self.settings['Rednerauswahl'] = self.redner_liste_var.get()
        self.settings['Schriftgröße'] = self.schriftgroesse_var.get()
        self.settings['Protokoll zeigen'] = self.protokoll_zeigen_var.get()
        self.settings['Trenner 1'] = self.trenner_1_var.get()
        self.settings['Trenner 2'] = self.trenner_2_var.get()
        self.settings['Zeitformat'] = self.zeit_format_var.get()
        self.settings['checkbox anwesend'] = self.anwesend_checkbox_var.get()
        self.settings['checkbox eingereiht'] = self.eingereiht_text_var.get()
        self.settings['checkbox gesprochen'] = self.gesprochen_checkbox_var.get()
        self.settings['checkbox verlassen'] = self.geloescht_checkbox_var.get()
        self.settings['text anwesend'] = self.anwesend_text_var.get()
        self.settings['text eingereiht'] = self.eingereiht_checkbox_var.get()
        self.settings['text gesprochen'] = self.gesprochen_text_var.get()
        self.settings['text verlassen'] = self.geloescht_text_var.get()
#        self.settings['Fenster'] = self.master.geometry.get()


        # Einstellungen in "settings.txt" speichern
        with open("settings.txt", 'w') as file:
            json.dump(self.settings, file)
        messagebox.showinfo("Erfolg", f"Einstellungen wurden in settings.txt gespeichert.")


    def load_settings(self):
        # Versuchen, Einstellungen aus "settings.txt" zu laden
        try:
            with open("settings.txt", 'r') as file:
                loaded_settings = json.load(file)

            # Aktuelle Einstellungen aktualisieren
            self.settings.update(loaded_settings)
            messagebox.showinfo("Erfolg", f"Einstellungen wurden aus gefundener settings.txt Datei übernommen.")

            # GUI-Elemente mit den geladenen Einstellungen aktualisieren
#            self.checkbox_var.set(self.settings['option1'])
#            self.entry_var.set(self.settings['option2'])

        except FileNotFoundError:
            # Wenn "settings.txt" nicht gefunden wird, einfach weitermachen
            pass

                
# Ermöglicht Tooltips:   
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip_window, text=self.text, justify="left", background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

        self.tooltip_window.attributes("-topmost", True) # Bring das tooltip in den Vordergrund

        
    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

 
if __name__ == "__main__":
    root = tk.Tk()
    app = Rednerliste(root)
    root.mainloop()
