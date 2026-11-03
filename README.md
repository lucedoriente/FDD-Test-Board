# Retro-Diag FDD Master Tester & Exerciser

**Autore / Hardware Designer**: Alessio Iodice (<alessio67@gmail.com>)  
**Serie Hardware**: Retro-Diag Diagnostic Instruments  
**Revisione Hardware**: `1.0` (`2026-11-02` — Validazione KiCad 9.0)  
**Licenza**: CC BY-NC-SA 4.0  

---

## 1. Panoramica del Progetto

Il **Retro-Diag FDD Master Tester & Exerciser** è uno strumento da banco universale ad alte prestazioni per il collaudo, la riparazione, la taratura meccanica e l'allineamento delle testine di qualsiasi unità floppy disk prodotta tra il 1971 e la fine degli anni '90.

L'hardware è progettato con standard di laboratorio:
* **Copertura Totale dei Formati**:
  - **Drive 8 Pollici**: Shugart SA800/801, SA850/851, Siemens FDD100-8D, Memorex 651, PerSci, sistemi S-100/CP/M (soft-sector e hard-sector a 32 fori).
  - **Drive 5.25 Pollici**: Standard Shugart SA400/450 (35 tracce), PC/XT/AT (40 e 80 tracce: 160K, 180K, 320K, 360K, 720K Quad, 1.2M High Density a 360 RPM).
  - **Drive 3.5 Pollici**: 720 KB (Double Density), 1.44 MB (High Density), 2.88 MB (Extended Density a 1 Mbps e registrazione perpendicolare), varianti Apple/Amiga/Apricot.
  - **Drive 3 Pollici "Compact Floppy"**: Amstrad CPC 664/6128, Amstrad PCW 8256/8512, Sinclair ZX Spectrum +3, Tatung Einstein.
  - **Drive Apple II e Meccaniche Nude**: Apple II Disk II (20 pin) e connettore diretto a 4 fasi per motori stepper a magnete permanente (Commodore 1541).

---

## 2. Architettura Meccanica ed Ergonomia

Per garantire massima comodità di montaggio, dissipazione termica passiva e cablaggio ordinato, la scheda adotta le seguenti specifiche:
* **Dimensioni PCB**: **$200.0 \times 140.0\text{ mm}$** (PCB a 4 strati ad alta immunità ai disturbi, stackup JLCPCB JLC04161H-7628 con piani GND e Power dedicati).
* **Bordo Posteriore (Connettori a 90° angolari per cavi standard)**:
  - `J_FDD50`: Maschio IDC 50 pin a 90° (cavo piatto standard drive 8").
  - `J_FDD34`: Maschio IDC 34 pin a 90° polarizzato (cavo piatto standard 5.25" e 3.5").
  - `J_FDD26`: Maschio IDC 26 pin a 90° (cavo piatto 3" Amstrad/Spectrum e HP).
  - `J_APPLE20`: Maschio IDC 20 pin a 90° (cavo nastro Apple II Disk II).
  - `J_PWR_525`: Connettore Molex 4 pin maschio a 90° (+12V, GND, GND, +5V).
  - `J_PWR_350`: Connettore Berg floppy 4 pin maschio a 90° (+5V, GND, GND, +12V).
  - `J_PWR_800`: Morsettiera Phoenix passo 5.08 mm a 90° (+24V, +5V, GND, -12V/-5V).
  - `J_IN_24V`: Ingresso morsettiera a 90° dai 24V del modulo Mean Well interno.
* **Bordo Sinistro (Interfaccia PC)**:
  - Presa **USB Type-C** montata a filo con chip di protezione ESD `USBLC6-2SC6` per telemetria, dump dei dati e aggiornamento firmware.
* **Pannello Superiore / Frontale (Interfaccia Utente & Strumentazione)**:
  - Display grafico IPS a colori da **2.8" / 3.2"** (320 × 240 pixel, controller SPI ST7789V).
  - **Daughterboard Pannello Frontale (`FDD_UI_Panel`)**: Modulo dedicato da pannello ($120.0 \times 38.0\text{ mm}$, 2 layer) collegato alla scheda principale mediante cavo a nastro IDC polarizzato 14 poli (2×7 pitch 2.54 mm):
    - Encoder rotativo industriale Bourns PEC12R con pulsante integrato (`SELECT / PUSH`).
    - 3 Pulsanti tattili da pannello (`RUN`, `BACK`, `RESET`).
    - 5 Indicatori LED di stato ad alta visibilità (`READY`, `BUSY`, `FAULT`, `INDEX`, `READ`).
  - Basetta con **Punti di Test (Test Points)** con anelli di terra per sonde oscilloscopio 10x:
    `TP_GND`, `TP_INDEX`, `TP_READ_DATA`, `TP_TRACK0`, `TP_STEP`, `TP_DIR`, `TP_WRITE_GATE`.

---

## 3. Sezione di Alimentazione e Sicurezza Attiva (Zero-Smoke)

* **Alimentatore Integrato nel Case**: Modulo industriale **Mean Well IRM-60-24ST** o **EPS-65-24** (ingresso universale 90–264 VAC con vaschetta posteriore IEC C14 con fusibile e interruttore).
* **Rail di Potenza e Protezioni E-Fuse**:
  1. **+24V DC (fino a 2.5A)**: Diretto per motori ed elettromagnete di carico testina dei drive da 8".
  2. **+12V DC (fino a 2.5A)**: Convertitore Buck sincrono ad altissima efficienza (Texas Instruments `TPS54302`).
  3. **+5V DC (fino a 3.0A)**: Convertitore Buck sincrono ad altissima efficienza (Texas Instruments `TPS54302`).
  4. **-12V / -5V (fino a 50mA)**: Micro pompa di carica invertente (`TPS63700` o `LMC7660`) per bias comparatori vintage 8".
* **Misura Corrente e Trip di Protezione**:
  - Ogni rail (+24V, +12V, +5V) è dotato di shunt di precisione e amplificatore current-sense **INA180A1**.
  - Spegnimento istantaneo in $< 5\text{ }\mu\text{s}$ in caso di cortocircuito o motore bloccato, con allarme grafico a video.

---

## 4. Modalità Operative Firmware

1. **Wizard Guidato per Principianti**:
   - Riconoscimento assistito, schemi grafici a video di collegamento pin 1.
   - Test automatico a 5 passi: Check cortocircuiti $\to$ Sensori disco/WP $\to$ Misura precisa RPM ($\pm 0.1\text{ RPM}$) $\to$ Seek su tutte le tracce $\to$ Esito finale in italiano.
2. **Allineamento Testine (Analog Alignment Mode)**:
   - Cicli automatici tra Traccia 00, Traccia Centrale (16, 38 o 40) e Traccia Interna (39, 76, 79) per taratura lobo cat-eye e azimut con disco Dysan/Accurite.
3. **Generatore Pattern Read/Write & Flux**:
   - Generazione di pattern MFM/FM alle frequenze standard: 125 kHz, 250 kHz, 500 kHz e **1 MHz (ED 2.88MB)**.
   - Verifica di risposta del canale di preamplificazione e lettura del drive.
