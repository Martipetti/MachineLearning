Link kaggle import in python csv: https://www.kaggle.com/code/dissfya/atp-tennis-daily-pull/notebook

procedimento per stilare presentazione:
- eliminazione di alcune colonne inutili (spiegare perchè nè abbiamo eliminate alcune e tenute altre)
  - mantenuti i dati che possiamo sapere prima della partita
  - alcune colonne non sempre sono compilate e risulta inutile tenerle solo per alcune righe
- rinomina delle colonne (per aggiungere la colonna target)
- sono stati mescolati i dati. Nella sua forma primaria il data contiene nella colonna "winner" (rinominata in "player_1") il vincitore. Mescoliamo i dati tra le due colonne dei giocatori per evitare che il "player_1" sia sempre riconosciuto come il vincitore (le relazione tra questa e le altre colonne vengono mantenute)
- target contiene 0 -> vince giocatore 1,  1 -> vince giocatore 2
