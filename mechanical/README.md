# FDD Master Tester & Exerciser — Case Console 3D (FreeCAD 1.0/1.1)

Progetto CAD meccanico parametrico per il contenitore da banco a console ergonomica ($10^\circ$) del **Retro-Diag FDD Master Tester & Exerciser**.

---

## 1. Architettura a Campana (Base Tray + Upper Hood)

Il contenitore adotta l'architettura industriale a **Vassoio di Fondo + Calotta Superiore a Campana**:
* **Vassoio di Fondo (`Base_Tray`)**: accoglie la scheda madre e l'alimentatore Mean Well, consentendo il montaggio, il cablaggio e il collaudo a banco aperto a 360°.
* **Calotta Superiore (`Upper_Console_Hood`)**: monoblocco a cuneo ergonomico che scende dall'alto a campana, con scassi a pettine a "U" rovesciata che calzano sopra i connettori a filo scheda. Si fissa con 5 viti M3 svasate dal fondo.

---

## 2. File di Progetto e Produzione Generati

Tutti i file sono archiviati nella directory `mechanical/`:

| File | Formato | Destinazione / Utilizzo |
| :--- | :---: | :--- |
| **`FDD_Tester_Case_Assembly.FCStd`** | FreeCAD 1.0/1.1 | Progetto CAD parametrico nativo modificabile con FreeCAD |
| **`FDD_Tester_Case_Full_Assembly.step`** | STEP AP214 | Assieme solido 3D completo per verifica di accoppiamento |
| **`FDD_Tester_Base_Tray.step`** | STEP AP214 | Vassoio di fondo per lavorazione CNC / Stampa 3D |
| **`FDD_Tester_Base_Tray.stl`** | Mesh STL | Vassoio di fondo ad alta risoluzione pronto per upload JLCPCB |
| **`FDD_Tester_Upper_Hood.step`** | STEP AP214 | Calotta a campana per lavorazione CNC / Stampa 3D |
| **`FDD_Tester_Upper_Hood.stl`** | Mesh STL | Calotta a campana ad alta risoluzione pronta per upload JLCPCB |
| **`generate_case.py`** | Python | Script generatore parametrico per FreeCAD (`python.exe generate_case.py`) |

---

## 3. Specifiche Meccaniche e Dimensionali

* **Larghezza Totale ($X$)**: $320.00\text{ mm}$
* **Profondità Totale ($Y$)**: $185.00\text{ mm}$
* **Altezza Posteriore ($Z_{max}$)**: $70.00\text{ mm}$
* **Altezza Anteriore ($Z_{min}$)**: $40.00\text{ mm}$
* **Inclinazione Piano Superiore**: $\approx 9.21^\circ \div 10^\circ$
* **Spessore Parete e Base**: $3.00\text{ mm}$ uniforme
* **Labbro di Accoppiamento Base (*Upward Lip*)**: altezza $4.0\text{ mm}$, spessore $1.5\text{ mm}$, tolleranza $0.25\text{ mm}$

---

## 4. Supporto Scheda Madre a 6 Punti (Zero Flessione)

La scheda madre `FDD-Test-Board` ($200.0 \times 140.0\text{ mm}$) è supportata da 6 torrette M3 alte $8.0\text{ mm}$ con inserto in ottone termo-innestato M3:

| Foro | Posizione PCB $(X_{pcb}, Y_{pcb})$ | Posizione Case $(X, Y)$ | Ruolo Meccanico |
| :---: | :---: | :---: | :--- |
| **H1** | $(5.0, 5.0)\text{ mm}$ | $(121.0, 9.0)\text{ mm}$ | Angolo Posteriore Sinistro |
| **H2** | $(195.0, 5.0)\text{ mm}$ | $(311.0, 9.0)\text{ mm}$ | Angolo Posteriore Destro |
| **H3** | $(195.0, 135.0)\text{ mm}$ | $(311.0, 139.0)\text{ mm}$ | Angolo Anteriore Destro |
| **H4** | $(5.0, 135.0)\text{ mm}$ | $(121.0, 139.0)\text{ mm}$ | Angolo Anteriore Sinistro |
| **H5** | **$(100.0, 135.0)\text{ mm}$** | **$(216.0, 139.0)\text{ mm}$** | **Centro campata frontale (elimina flessione tasti)** |
| **H6** | **$(195.0, 101.0)\text{ mm}$** | **$(311.0, 105.0)\text{ mm}$** | **Fianco destro (supporto inserimento connettori)** |

---

## 5. Schema di Chiusura a 5 Viti Calotta-Fondo (Zero Interferenze)

Le 5 viti di chiusura si avvitano dal basso (testa svasata piana M3 DIN 7991 a filo base) verso inserti M3 integrati nelle pareti della calotta:

| Vite | Posizione $(X, Y)$ | Posizione nel Case | Perché è sicura |
| :---: | :---: | :--- | :--- |
| **V1** | **$(10.0, 10.0)\text{ mm}$** | Posteriore Sinistra | Prima della vaschetta IEC, a $32\text{ mm}$ dalle feritoie |
| **V2** | **$(91.25, 10.0)\text{ mm}$** | Posteriore Paratia | Nello spazio vuoto tra alimentatore e porta USB-C |
| **V3** | **$(313.0, 101.0)\text{ mm}$** | Fianco Destro | Nello spazio libero di $13\text{ mm}$ tra IDC-20 e J4 Phoenix |
| **V4** | **$(15.0, 175.0)\text{ mm}$** | Frontale Sinistra | Nella zona vuota anteriore vano Mean Well |
| **V5** | **$(305.0, 175.0)\text{ mm}$** | Frontale Destra | Nella zona vuota anteriore vano Mainboard |

---

## 6. Aperture a "U" Rovesciata per Connettori a Filo

### Pannello Posteriore ($Y = 0$)
1. **Vaschetta IEC C14**: Finestra rettangolare chiusa $48 \times 28\text{ mm}$ a quota $X = 24 \div 72\text{ mm}$ con 2 fori viti M3 (interasse $40\text{ mm}$).
2. **J6 (USB Type-C)**: Scasso a U $12.0 \times 18.0\text{ mm}$ a quota $X = 132.5\text{ mm}$.
3. **J2 (Molex 5.25")**: Scasso a U $22.0 \times 23.5\text{ mm}$ a quota $X = 159.0\text{ mm}$.
4. **J3 (mini-Berg 3.5")**: Scasso a U $16.0 \times 21.5\text{ mm}$ a quota $X = 168.0\text{ mm}$.
5. **J11 (IDC-34 90° - Bus Floppy 3.5"/5.25")**: Scasso a U $54.0 \times 24.0\text{ mm}$ a quota $X = 183.5\text{ mm}$.
6. **J10 (IDC-50 90° - Bus Floppy 8" Shugart)**: Scasso a U $74.0 \times 24.0\text{ mm}$ a quota $X = 236.0\text{ mm}$.

### Fianco Destro ($X = 320\text{ mm}$)
1. **J12 (IDC-26 90° - Amstrad 3")**: Scasso a U $43.0 \times 24.0\text{ mm}$ a quota $Y = 26.0\text{ mm}$.
2. **J13 (IDC-20 90° - Apple II)**: Scasso a U $35.0 \times 24.0\text{ mm}$ a quota $Y = 70.0\text{ mm}$.
3. **J4 (Phoenix 4-pin 24V Drive 8")**: Scasso a U $22.0 \times 23.0\text{ mm}$ a quota $Y = 114.0\text{ mm}$.
4. **J14 (Header Stepper 4-fasi)**: Scasso a U $17.0 \times 22.0\text{ mm}$ a quota $Y = 128.0\text{ mm}$.

### Fianco Sinistro ($X = 0$)
* 8 Feritoie orizzontali $35.0 \times 3.5\text{ mm}$ pulite e distanziate (da $Y = 42.0\text{ mm}$ a $Y = 133.0\text{ mm}$), senza alcuna interferenza con le torrette.

---

## 7. Cruscotto Superiore Console (Roof)

* **Display Sunton ESP32-8048S070C (7.0 pollici)**: Finestra attiva frontale $154.0 \times 86.0\text{ mm}$ con incasso a battuta interna $182.0 \times 109.0 \times 1.8\text{ mm}$.
* **Daughterboard Comandi `FDD_UI_Panel` ($120 \times 38\text{ mm}$)**: Fori passanti per alberino encoder $\varnothing 7.5\text{ mm}$, 3 pulsanti $\varnothing 7.0\text{ mm}$ e 5 LED $\varnothing 3.2\text{ mm}$.
