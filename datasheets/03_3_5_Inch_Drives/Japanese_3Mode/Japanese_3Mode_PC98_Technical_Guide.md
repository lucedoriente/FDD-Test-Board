# Japanese 3-Mode Floppy Drives (NEC PC-98 / PC-88 / MSX)

## 1. Il Concetto di "3-Mode" Floppy (Giappone)

Nel mercato informatico giapponese (dominato dai sistemi **NEC PC-9801, PC-8801, Sharp X68000, Fujitsu FM Towns**), lo standard floppy per dischi da 3.5" non utilizzava solo i formati occidentali IBM (720 KB e 1.44 MB a 300 RPM), ma adottava primariamente un formato speciale ad alta densità:
- **Formato 1.2 MB Giapponese (PC-98)**:
  - Velocita del mandrino: **360.0 RPM** (anziché i consueti 300 RPM dei drive da 3.5").
  - Frequenza di trasferimento dati: **500 kbit/s**.
  - Formattazione: 80 cilindri, 2 lati, **8 settori da 1024 byte per traccia** (o 15 settori da 512 byte = 1.2 MB).
  - Questo consentiva la compatibilità binaria diretta con i dischetti da 5.25" ad alta densità usati sui PC/AT e sui PC-98 desktop.

## 2. Le Tre Modalita Operative dei Drive "3-Mode"

| Modalita | Capacita Non Formattata | Velocita Mandrino | Transfer Rate | Settori / Traccia | Standard Tipico |
|:---|:---:|:---:|:---:|:---:|:---|
| **1 MB (2DD)** | 1.0 MB (720 KB form.) | **300 RPM** | 250 kbit/s | 9 settori da 512B | Standard PC/MSX |
| **1.6 MB (2HD Japan)** | 1.6 MB (1.2 MB form.) | **360 RPM** | 500 kbit/s | 8 settori da 1024B | **NEC PC-9801 / X68000** |
| **2 MB (2HD IBM)** | 2.0 MB (1.44 MB form.) | **300 RPM** | 500 kbit/s | 18 settori da 512B | Standard IBM PC/AT |

## 3. Modelli Emblematici e Controllo Hardware

- **TEAC FD-235HG** (e varianti HG-C8xx / HG-A8xx):
  - Il drive rileva la finestra HD tramite sensore ottico/meccanico.
  - La commutazione a 360 RPM puo avvenire via hardware (commutazione automatica a 360 RPM su dischi HD se configurato jumper `3M`), oppure tramite livello logico sul **Pin 2** del connettore 34 pin (`HD/MODE SELECT`).
- **Epson SMD-1000 / SMD-1040 / Chinon FZ-357**:
  - Doppia bobina tachimetrica interna con PLL bifrequenza (300/360 RPM).

## 4. Test sul Retro-Diag FDD Tester

Il nostro timer `TIM4` e la logica di diagnosi riconoscono automaticamente entrambe le frequenze nominali:
- Se il drive e' testato in modalita standard 3.5", il target e' $300\text{ RPM}$.
- Se il drive e' selezionato come **3-Mode (PC-98 1.2MB)**, il target e' **$360.0\text{ RPM}$**, identico a quello dei drive da 5.25" HD!
