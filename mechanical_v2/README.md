# Retro-Diag FDD Master Tester & Exerciser — Modular Enclosure V2

## Architettura e Filosofia di Progetto (Release V2)
Il case V2 è un'evoluzione modulare ad alta sicurezza dello strumento da banco, progettata per separare fisicamente e galvanicamente la sezione a tensione di rete (230V AC) dalla sezione a bassissima tensione di sicurezza (24V DC / 5V / 3.3V Logic).

### Componenti dell'Assieme:
1. **Modulo Alimentatore (Sinistra — $95.0\text{ mm}$)**:
   - Alloggia l'alimentatore Mean Well serie LRS (LRS-50-24 o LRS-75-24).
   - Presa IEC C14 con portafusibile e interruttore sul pannello posteriore.
   - Feritoie di aspirazione sul fondo, feritoie laterali di ingresso aria fresca e griglia di sfogo termico a convezione sul tetto.
   - Chiusura a 4 viti con proprio coperchio indipendente: **il vano 230V resta sempre sigillato anche durante la manutenzione o i test a banco aperto della scheda madre**.

2. **Piastra di Schermatura EMC / Galvanica (Centro — $1.5\text{ mm}$ Alluminio)**:
   - Lamina metallica sagomata a cuneo interposta tra i due contenitori.
   - Blocca l'irradiazione elettromagnetica ad alta frequenza dello switching verso i circuiti sensibili di lettura floppy.
   - Collegata al conduttore di Terra (PE) per equipotenzialità.
   - Funge da spina dorsale strutturale rigida (*shear web*) quando i due moduli vengono serrati insieme.

3. **Modulo Strumento / Console Logica (Destra — $235.0\text{ mm}$)**:
   - Alloggia la scheda madre `FDD-Test-Board` ($200 \times 140\text{ mm}$) su 7 torrette con prefori $\varnothing 2.50\text{ mm}$ (incluso il supporto intermedio posteriore anti-flessione `H7`).
   - Tetto ergonomico inclinato a cuneo (~9.2°) con **Display Touchscreen 7.0" Sunton ESP32-8048S070C perfettamente centrato** sul modulo ($26.5\text{ mm}$ di cornice laterale per lato).
   - Daughterboard comandi `FDD_UI_Panel` ($120 \times 38\text{ mm}$) centrata sotto il display (encoder rotativo, 3 pulsanti, 5 LED di stato).
   - Scassi a "U" aperti sul fondo per connettori posteriori (USB-C, Molex 5.25", Berg 3.5", IDC-34, IDC-50) e laterali destri (IDC-26, IDC-20, Phoenix 24V, Header 6-pin).

4. **Interfaccia di Accoppiamento**:
   - **Scasso Cavi Condiviso**: asola $30 \times 16\text{ mm}$ a quota $Y \in [80, 110\text{ mm}], Z \in [3, 19\text{ mm}]$ allineata attraverso parete PSU, piastra schermo e parete logica.
   - **Traliccio di Unione a 5 Bulloni M4**: 5 fori calibrati con tasche esagonali per dadi M4 sulla parete interna dello strumento.

---

## Elenco File di Fabbricazione (`mechanical_v2/`)
| File | Descrizione | Dimensioni ($X \times Y \times Z$) | Materiale Consigliato |
| :--- | :--- | :--- | :--- |
| `00_Modular_V2_Full_Assembly.step` | Assieme 3D completo di tutti i 5 componenti | $331.5 \times 185.0 \times 70.0\text{ mm}$ | Visualizzazione CAD |
| `01_PSU_Base_Tray.step` / `.stl` | Vassoio base vano alimentatore | $95.0 \times 185.0 \times 38.0\text{ mm}$ | Resina SLA (9600 White o Black) / PA12 |
| `02_PSU_Upper_Hood.step` / `.stl` | Calotta superiore vano alimentatore | $95.0 \times 185.0 \times 70.0\text{ mm}$ | Resina SLA (9600 White o Black) / PA12 |
| `03_EMC_Shield_Plate_1.5mm.step` | Piastra centrale di schermatura | $1.5 \times 185.0 \times 70.0\text{ mm}$ | Alluminio 1.5mm (Taglio Laser / Waterjet) |
| `04_Logic_Base_Tray.step` / `.stl` | Vassoio base vano strumento | $235.0 \times 185.0 \times 38.0\text{ mm}$ | Resina SLA (9600 White o Black) / PA12 |
| `05_Logic_Upper_Hood.step` / `.stl` | Calotta superiore vano strumento | $235.0 \times 185.0 \times 70.0\text{ mm}$ | Resina SLA (9600 White o Black) / PA12 |
| `FDD_Tester_Modular_V2.FCStd` | Progetto sorgente nativo FreeCAD 1.0/1.1 | — | CAD Modificabile |

---

## Ferramenta Necessaria (BOM Fasteners)
- **Chiusura Calotte dal Fondo**: 8 viti a testa svasata M3 $\times 16\text{ mm}$ (4 per PSU + 4 per Logica).
- **Unione Modulo PSU $\leftrightarrow$ Modulo Logica**: 5 viti M4 $\times 16\text{ mm}$ a testa cilindrica/bombata con 5 dadi M4 e rondelle.
- **Fissaggio Scheda Madre FDD-Test-Board**: 7 viti M3 $\times 6\text{ mm}$ autofilettanti per plastica.
- **Fissaggio Alimentatore Mean Well LRS**: 4 viti M3 $\times 6\text{ mm}$ autofilettanti per plastica.
- **Fissaggio Presa IEC C14**: 2 viti M3 $\times 10\text{ mm}$ con dadi.
