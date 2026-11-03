# Commodore Amiga Floppy Drive Technical Specification & Modification Guide

## 1. Amiga Floppy Interface vs Standard PC Interface (34-pin Ribbon)

L'interfaccia a 34 pin dell'Amiga (usata nei modelli A500, A600, A1200, A2000, A3000, A4000) deriva dal bus Shugart SA400 originale e presenta differenze **critiche e non negoziabili** rispetto allo standard IBM PC:

| Pin | Segnale PC (IBM AT) | Segnale Amiga (Paula) | Descrizione Tecnica Amiga |
|:---:|:---|:---|:---|
| **Pin 2** | NC / HD High Density | **/DISKCHANGE** | Va a livello BASSO quando il disco viene estratto; resettato da un fronte di step con disco inserito |
| **Pin 8** | /INDEX | **/INDEX** | Impulso ottico per giro (300 RPM standard -> 200 ms periodo) |
| **Pin 10** | /DRIVE SELECT 0 | **/DRIVE SELECT 0** | Abilitazione primo drive (`DF0:` interno) |
| **Pin 12** | /DRIVE SELECT 1 | **/DRIVE SELECT 1** | Abilitazione secondo drive interno (es. A2000) |
| **Pin 14** | /DRIVE SELECT 2 | NC / Not Used | |
| **Pin 16** | /MOTOR ON | **/MOTOR ON** | Attivazione motore mandrino (0V = Attivo) |
| **Pin 18** | /DIRECTION | **/DIRECTION** | Direzione scorrimento testine (0V = Verso l'interno/centro) |
| **Pin 20** | /STEP | **/STEP** | Impulso di avanzamento traccia (passo min 3 ms) |
| **Pin 22** | /WRITE DATA | **/WRITE DATA** | Impulsi MFM codificati da Paula |
| **Pin 24** | /WRITE GATE | **/WRITE GATE** | Abilitazione corrente di scrittura testina |
| **Pin 26** | /TRACK 00 | **/TRACK 00** | Rilevamento ottico posizione su Traccia 00 |
| **Pin 28** | /WRITE PROTECT | **/WRITE PROTECT** | 0V = Disco protetto da scrittura (foro aperto) |
| **Pin 30** | /READ DATA | **/READ DATA** | Flusso bit grezzi MFM da inviare a Paula |
| **Pin 32** | /SIDE 1 SELECT | **/SIDE 1 SELECT** | 0V = Testina Superiore (Testina 1), 5V = Testina 0 |
| **Pin 34** | **/DISKCHANGE** (AT) | **/READY (RDY)** | **DIFFERENZA CRUCIALE**: Paula esige `READY` a livello BASSO quando il mandrino e' a 300 RPM e il disco e' presente! Se si collega un drive PC non modificato, il Pin 34 emette Disk Change e l'Amiga non riconosce il drive. |

---

## 2. Modelli di Meccaniche Amiga Ufficiali OEM

### A. Chinon FB-354 (DD 880 KB - Standard Amiga 500 / 2000)
- **Specifiche**: 80 tracce, 2 lati, 300 RPM, 3 ms step rate, connettore 34-pin standard con Pin 34 = `/READY`.
- **Configurazione Jumper posteriore (6-pin block)**:
  - Ponticello su **DS0** (seleziona Drive 0).
  - Ponticello **RDY** / **MM** (Motor Mode / Ready attivo su Pin 34).
- **Guasti Tipici**:
  1. *Condensatori SMD che perdono (Leaking Caps)*: C1 (22µF 16V), C2 (1µF 50V), C3 (100µF 6.3V). L'elettrolita acido corrode le piste sottostanti, causando il blocco del motore BLDC o assenza di segnale Read Data.
  2. *Microswitch di presenza disco e write-protect ossidati*: Mancata commutazione di `/DISKCHANGE` o `/READY`.

### B. Chinon FB-357A / FZ-357A (HD 1.76 MB - Amiga 3000 / 4000)
- **Specifiche**: Meccanica High Density a doppia velocità.
- **Funzionamento Unico**: Per mantenere il flusso dati compatibile con la banda del chip Paula (senza richiedere clock raddoppiato), quando viene inserito un floppy HD la velocità del mandrino viene **dimezzata automaticamente a 150 RPM**!
  - Dischi DD (880 KB): rotazione a **300 RPM**.
  - Dischi HD (1.76 MB): rotazione a **150 RPM**.

---

## 3. Guida alla Conversione di Drive PC per Amiga (Ready Mod)

Per usare un drive PC economico su Amiga sono richieste due modifiche hardware sul drive:
1. **Configurazione DS0**: Spostare il jumper o la resistenza a zero-ohm da `DS1` (standard PC) a `DS0`.
2. **Generazione Segnale READY su Pin 34**:
   - *Metodo Hardware con ponticello*: Su drive come TEAC FD-235HF o Sony MPF-920, individuare la piazzola `RY` o `RDY` e ponticellarla sul Pin 34, tagliando la traccia che collega Pin 34 a `DC` (Disk Change).
   - *Metodo Emulazione*: Se il drive non supporta nativamente RDY, si usa un circuito flip-flop (74LS74 o transistor) che abbassa il Pin 34 solo quando `/MOTOR_ON` e' attivo e viene rilevato l'impulso `/INDEX`.

---

## 4. Connettore Esterno DB-23 Floppy Amiga (Porta DF1:)

Sul retro dei computer Amiga e' presente una porta DB-23 femmina per connettere drive esterni.
- La porta veicola tutte le linee del bus Shugart piu':
  - Linee di alimentazione (+5V max 1A, +12V max 0.5A).
  - Segnale `/MTRX` condiviso: ogni drive esterno ha un flip-flop 74LS74 a registro a scorrimento che aggancia il comando motore all'invio del segnale Drive Select.
