# Atari ST Floppy Drive Technical Specification & Jumper Guide

## 1. Architettura Bus Floppy Atari ST (520ST, 1040ST, Mega ST, Falcon)

A differenza dell'Amiga che usa un'interfaccia personalizzata con segnale `/READY` su Pin 34, l'**Atari ST** adotta un bus molto piu' vicino allo standard Shugart/PC:
- **Connettore**: Flat standard a 34 pin (e connettore DIN a 14 pin sul retro per il drive esterno `B:`).
- **Controller FDC**: Western Digital **WD1772** (sui modelli ST/STE) o **AJAX** (sui modelli con supporto 1.44MB HD come Mega STE, TT030 e Falcon).
- **Velocita Mandrino**: **300.0 RPM** ($\pm 1\%$).
- **Step Rate**: 3 ms (supportato nativamente da TOS, impostabile a 2 ms, 3 ms o 6 ms).
- **Formati Tracce**: 80 cilindri, 2 lati, 9 settori per traccia (720 KB) o 18 settori (1.44 MB HD).

## 2. Pinout e Differenze con lo Standard PC

| Pin | Funzione Atari ST | Note Tecniche |
|:---:|:---|:---|
| **Pin 8** | /INDEX | Impulso ottico per giro (200 ms @ 300 RPM) |
| **Pin 10** | /DRIVE SELECT 0 | Seleziona l'unita interna `A:` |
| **Pin 12** | /DRIVE SELECT 1 | Seleziona l'unita esterna `B:` (sul connettore DIN posteriore) |
| **Pin 16** | /MOTOR ON | Pilotato direttamente dal chip PSG Yamaha YM2149 (Port A bit 2) |
| **Pin 18** | /DIRECTION | Direzione di step (0V = interno) |
| **Pin 20** | /STEP | Impulso di passo per il carrello |
| **Pin 22** | /WRITE DATA | Dati codificati MFM dal WD1772 |
| **Pin 24** | /WRITE GATE | Abilitazione scrittura |
| **Pin 26** | /TRACK 00 | Rilevamento ottico Traccia 0 |
| **Pin 28** | /WRITE PROTECT | Protezione scrittura (YM2149) |
| **Pin 30** | /READ DATA | Dati MFM letti dal disco |
| **Pin 32** | /SIDE 1 SELECT | Selezione testina superiore (YM2149) |
| **Pin 34** | NC / /DISK CHANGE | Nei primi 520ST/1040ST non era connesso alla scheda madre; nei TOS recenti legge il cambio disco. |

## 3. Modelli di Meccaniche OEM e Guasti Tipici

1. **Epson SMD-380 (DD 720 KB)**:
   - Meccanica a montaggio orizzontale/verticale.
   - *Jumper*: Selezionato sempre su **DS0** (Drive 0).
   - *Guasto frequente*: Condensatori di disaccoppiamento motore in perdita e vite senza fine secca.
2. **Chinon F-054 / FB-354 (versione Atari)**:
   - Configurato con jumper su DS0 (anziche DS1 del PC).
3. **Sony MPF-110 / MPF-920 / Teac FD-235HF**:
   - Per essere montati su Atari ST necessitano solo di essere ponticellati su **DS0**.
