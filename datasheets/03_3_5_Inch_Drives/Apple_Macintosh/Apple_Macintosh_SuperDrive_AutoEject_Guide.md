# Apple Macintosh 3.5" Floppy Drives & SuperDrive Auto-Eject

## 1. Panoramica Meccanica: L'Assenza del Tasto di Espulsione

Una delle caratteristiche piu iconiche dei computer Apple Macintosh classici (Mac 128K, 512K, Plus, SE, Classic, II, LC, Quadra) e l'assenza di un pulsante meccanico frontale di espulsione del floppy disk:
- L'espulsione e **motorizzata**: all'interno del drive e presente un micromotore DC a spazzole accoppiato a una cascata di ingranaggi in plastica e a una cremagliera.
- Quando l'utente trascina l'icona del floppy nel cestino (o preme Eject da tastiera), il sistema operativo attiva il chip SWIM/IWM inviando una sequenza di abilitazione che alimenta il motorino di espulsione per circa 500 ms, spingendo energicamente fuori il disco.

## 2. Il Rischio Durante i Test a Banco (Graffetta di Sicurezza)

> [!WARNING]
> Se si inserisce un dischetto in un drive Apple Macintosh Auto-Eject collegato a un generico banco di collaudo privo del circuito driver di espulsione, **il dischetto rimane agganciato all'interno**.
> Per estrarlo e tassativo utilizzare il metodo della **graffetta metallica raddrizzata**, inserendola con decisione nel forellino di sblocco d'emergenza situato sul frontale a destra dell'asola di inserimento per azionare manualmente la camma di sgancio.

## 3. Modelli di Meccaniche Macintosh

| Modello Apple / Sony | Capacita | Velocita Mandrino | Connettore | Note Meccaniche |
|:---|:---:|:---:|:---:|:---|
| **Sony OA-D34V** | 400 KB SS | **Variabile CLV** (390 - 780 RPM) | 20 pin flat | Monolaterale, velocita governata da chip IWM |
| **Sony MP-F51W** | 800 KB DS | **Variabile CLV** (394 - 788 RPM) | 20 pin flat | Bilaterale, velocita governata da chip IWM |
| **Sony MP-F75W** (SuperDrive / FDHD) | 1.44 MB HD / 800K / 720K | **Dual Speed** (300 RPM per MFM; CLV per GCR) | 20 pin flat | Gestito dal chip SWIM, auto-eject motorizzato |

## 4. Guasti Frequenti dei Meccanismi Auto-Eject

1. **Ingranaggi di Espulsione Sgranati o Induriti**:
   - Il grasso originale bianco al litio invecchiando si trasforma in resina dura, bloccando gli ingranaggi dell'auto-eject. Il motorino sforza e i transistor driver saltano.
   - *Rimedio*: Pulizia con alcool isopropilico e reingrassaggio con grasso sintetico al PTFE.
2. **Transistor Driver di Espulsione Bruciati (Q3 / Q4)**:
   - Sulla scheda Sony del SuperDrive MP-F75W, i transistor di pilotaggio dell'espulsione (equivalenti a Toshiba `2SA1298` PNP) possono bruciarsi a causa del motore bloccato.
3. **Condensatori Elettrolitici in Perdita**:
   - I condensatori SMD a barilotto presenti sulla schedina causano instabilita sull'amplificatore di lettura e sul circuito di tracking Traccia 0.
