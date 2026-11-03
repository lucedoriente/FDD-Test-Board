/**
 * @file    fdd_diagnostics.c
 * @brief   Automated Floppy Drive Diagnostic Suite & Expert Repair Advisor Implementation
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 */

#include "fdd_diagnostics.h"
#include "bsp_fdd_gpio.h"
#include "cli_console.h"

#include <stdio.h>
#include <string.h>

extern void HAL_Delay(uint32_t Delay);
extern uint32_t hal_get_tick_ms(void);

/* ========================================================================== */
/* 1. OEM Drive Model Specifications Database                                 */
/* ========================================================================== */

static const fdd_model_spec_t s_model_specs[DRIVE_MODEL_COUNT] = {
    {
        .model_id = DRIVE_MODEL_AUTO_DETECT,
        .display_name = "Auto-Probe Rilevazione Automatica",
        .size_str = "Auto",
        .nominal_rpm = 300.0f,
        .rpm_tolerance_pct = 1.0f,
        .max_cylinders = 80,
        .recommended_step_rate = STEP_RATE_3MS,
        .motion_mode = MOTION_MODE_STANDARD_BUS,
        .requires_24v = false,
        .has_track0_sensor = true,
        .oem_manual_url = "https://archive.org/details/floppy_drive_manuals"
    },
    {
        .model_id = DRIVE_MODEL_GENERIC_350_HD,
        .display_name = "3.5\" HD Standard PC (Direct Drive BLDC)",
        .size_str = "3.5\"",
        .nominal_rpm = 300.0f,
        .rpm_tolerance_pct = 1.0f,
        .max_cylinders = 80,
        .recommended_step_rate = STEP_RATE_3MS,
        .motion_mode = MOTION_MODE_STANDARD_BUS,
        .requires_24v = false,
        .has_track0_sensor = true,
        .oem_manual_url = "https://retrocmp.de/fdd/general_35.htm"
    },
    {
        .model_id = DRIVE_MODEL_SONY_MPF920,
        .display_name = "Sony MPF-920 (3.5\" 1.44MB BLDC)",
        .size_str = "3.5\"",
        .nominal_rpm = 300.0f,
        .rpm_tolerance_pct = 1.0f,
        .max_cylinders = 80,
        .recommended_step_rate = STEP_RATE_3MS,
        .motion_mode = MOTION_MODE_STANDARD_BUS,
        .requires_24v = false,
        .has_track0_sensor = true,
        .oem_manual_url = "https://archive.org/details/manualzilla-id-6974254"
    },
    {
        .model_id = DRIVE_MODEL_TEAC_FD235HF,
        .display_name = "TEAC FD-235HF (3.5\" 1.44MB / 720KB)",
        .size_str = "3.5\"",
        .nominal_rpm = 300.0f,
        .rpm_tolerance_pct = 1.0f,
        .max_cylinders = 80,
        .recommended_step_rate = STEP_RATE_3MS,
        .motion_mode = MOTION_MODE_STANDARD_BUS,
        .requires_24v = false,
        .has_track0_sensor = true,
        .oem_manual_url = "https://hxc2001.com/download/floppy_drive_documentation/datasheets/TEAC_FD-235HF.pdf"
    },
    {
        .model_id = DRIVE_MODEL_CHINON_FB354,
        .display_name = "Chinon FB-354 (Amiga 3.5\" DD 880KB)",
        .size_str = "3.5\"",
        .nominal_rpm = 300.0f,
        .rpm_tolerance_pct = 1.0f,
        .max_cylinders = 80,
        .recommended_step_rate = STEP_RATE_3MS,
        .motion_mode = MOTION_MODE_STANDARD_BUS,
        .requires_24v = false,
        .has_track0_sensor = true,
        .oem_manual_url = "https://retro-commodore.eu/amiga-hardware/"
    },
    {
        .model_id = DRIVE_MODEL_CHINON_FB357A,
        .display_name = "Chinon FB-357A/FZ-357A (Amiga 3.5\" HD 1.76MB)",
        .size_str = "3.5\"",
        .nominal_rpm = 300.0f,
        .rpm_tolerance_pct = 1.0f,
        .max_cylinders = 80,
        .recommended_step_rate = STEP_RATE_3MS,
        .motion_mode = MOTION_MODE_STANDARD_BUS,
        .requires_24v = false,
        .has_track0_sensor = true,
        .oem_manual_url = "https://retro-commodore.eu/amiga-hardware/"
    },
    {
        .model_id = DRIVE_MODEL_TANDON_TM100_2A,
        .display_name = "Tandon TM100-2A (5.25\" 360KB PC/XT)",
        .size_str = "5.25\"",
        .nominal_rpm = 300.0f,
        .rpm_tolerance_pct = 1.5f,
        .max_cylinders = 40,
        .recommended_step_rate = STEP_RATE_6MS,
        .motion_mode = MOTION_MODE_STANDARD_BUS,
        .requires_24v = false,
        .has_track0_sensor = true,
        .oem_manual_url = "https://archive.org/details/TM1001TM100248TPIOperatingAndServiceManual1983"
    },
    {
        .model_id = DRIVE_MODEL_TEAC_FD55GFR,
        .display_name = "TEAC FD-55GFR (5.25\" 1.2MB/360KB Dual-Speed)",
        .size_str = "5.25\"",
        .nominal_rpm = 360.0f,
        .rpm_tolerance_pct = 1.0f,
        .max_cylinders = 80,
        .recommended_step_rate = STEP_RATE_3MS,
        .motion_mode = MOTION_MODE_STANDARD_BUS,
        .requires_24v = false,
        .has_track0_sensor = true,
        .oem_manual_url = "http://deramp.com/downloads/floppy_drives/teac/TEAC%20FD-55GFR.pdf"
    },
    {
        .model_id = DRIVE_MODEL_SHUGART_SA400,
        .display_name = "Shugart SA400 Minifloppy (35 Track Vintage)",
        .size_str = "5.25\"",
        .nominal_rpm = 300.0f,
        .rpm_tolerance_pct = 2.0f,
        .max_cylinders = 35,
        .recommended_step_rate = STEP_RATE_20MS,
        .motion_mode = MOTION_MODE_STANDARD_BUS,
        .requires_24v = false,
        .has_track0_sensor = true,
        .oem_manual_url = "http://deramp.com/downloads/floppy_drives/shugart/SA400%20Service%20Manual.pdf"
    },
    {
        .model_id = DRIVE_MODEL_SHUGART_SA800,
        .display_name = "Shugart SA800/801 8\" Single-Sided (AC Motor)",
        .size_str = "8\"",
        .nominal_rpm = 360.0f,
        .rpm_tolerance_pct = 1.0f,
        .max_cylinders = 77,
        .recommended_step_rate = STEP_RATE_8MS,
        .motion_mode = MOTION_MODE_STANDARD_BUS,
        .requires_24v = true,
        .has_track0_sensor = true,
        .oem_manual_url = "http://www.bitsavers.org/pdf/shugart/SA8xx/39025-1_SA800_801_Service_Manual_Mar82.pdf"
    },
    {
        .model_id = DRIVE_MODEL_SHUGART_SA850,
        .display_name = "Shugart SA850/851 8\" Double-Sided (AC Motor)",
        .size_str = "8\"",
        .nominal_rpm = 360.0f,
        .rpm_tolerance_pct = 1.0f,
        .max_cylinders = 77,
        .recommended_step_rate = STEP_RATE_8MS,
        .motion_mode = MOTION_MODE_STANDARD_BUS,
        .requires_24v = true,
        .has_track0_sensor = true,
        .oem_manual_url = "https://bitsavers.org/pdf/shugart/SA8xx/39018-0_SA850_851_Service_Manual_Dec80.pdf"
    },
    {
        .model_id = DRIVE_MODEL_AMSTRAD_EME156,
        .display_name = "Matsushita EME-156 (Amstrad 3\" Compact Floppy)",
        .size_str = "3\"",
        .nominal_rpm = 300.0f,
        .rpm_tolerance_pct = 1.5f,
        .max_cylinders = 40,
        .recommended_step_rate = STEP_RATE_12MS,
        .motion_mode = MOTION_MODE_STANDARD_BUS,
        .requires_24v = false,
        .has_track0_sensor = true,
        .oem_manual_url = "https://archive.org/details/amstrad-cpc-6128-service-manual"
    },
    {
        .model_id = DRIVE_MODEL_APPLE_DISK_II,
        .display_name = "Apple II Disk II (Shugart SA390 4-Fasi)",
        .size_str = "5.25\"",
        .nominal_rpm = 300.0f,
        .rpm_tolerance_pct = 1.5f,
        .max_cylinders = 35,
        .recommended_step_rate = STEP_RATE_20MS,
        .motion_mode = MOTION_MODE_4PHASE_HALF,
        .requires_24v = false,
        .has_track0_sensor = false,
        .oem_manual_url = "https://archive.org/details/apple-ii-disk-ii-manual"
    },
    {
        .model_id = DRIVE_MODEL_COMMODORE_1541,
        .display_name = "Commodore 1541 Mechanics (ALPS/Newtronics 4-Fasi)",
        .size_str = "5.25\"",
        .nominal_rpm = 300.0f,
        .rpm_tolerance_pct = 1.5f,
        .max_cylinders = 40,
        .recommended_step_rate = STEP_RATE_20MS,
        .motion_mode = MOTION_MODE_4PHASE_FULL,
        .requires_24v = false,
        .has_track0_sensor = false,
        .oem_manual_url = "https://www.zimmers.net/anonftp/pub/cbm/schematics/drives/new/1541/1540-1541_Disk_Drive_Service_Manual_314002-01_(1985_Nov).pdf"
    },
    {
        .model_id = DRIVE_MODEL_ATARI_ST_EPSON,
        .display_name = "Atari ST (Epson SMD-380 / Chinon 720K/1.44M)",
        .size_str = "3.5\"",
        .nominal_rpm = 300.0f,
        .rpm_tolerance_pct = 1.0f,
        .max_cylinders = 80,
        .recommended_step_rate = STEP_RATE_3MS,
        .motion_mode = MOTION_MODE_STANDARD_BUS,
        .requires_24v = false,
        .has_track0_sensor = true,
        .oem_manual_url = "https://dev-docs.org/"
    },
    {
        .model_id = DRIVE_MODEL_JAPAN_3MODE,
        .display_name = "Japanese 3-Mode (TEAC FD-235HG PC-98 1.2MB)",
        .size_str = "3.5\"",
        .nominal_rpm = 360.0f,
        .rpm_tolerance_pct = 1.0f,
        .max_cylinders = 80,
        .recommended_step_rate = STEP_RATE_3MS,
        .motion_mode = MOTION_MODE_STANDARD_BUS,
        .requires_24v = false,
        .has_track0_sensor = true,
        .oem_manual_url = "https://hxc2001.com/download/floppy_drive_documentation/datasheets/TEAC_FD-235HG.pdf"
    },
    {
        .model_id = DRIVE_MODEL_APPLE_MAC_SUPERDRIVE,
        .display_name = "Apple Mac SuperDrive (Sony MP-F75W Auto-Eject)",
        .size_str = "3.5\"",
        .nominal_rpm = 300.0f,
        .rpm_tolerance_pct = 1.5f,
        .max_cylinders = 80,
        .recommended_step_rate = STEP_RATE_3MS,
        .motion_mode = MOTION_MODE_STANDARD_BUS,
        .requires_24v = false,
        .has_track0_sensor = true,
        .oem_manual_url = "https://bitsavers.org/pdf/apple/disk/sony/Apple_3.5_Drive_Schematic.pdf"
    }
};

const fdd_model_spec_t *fdd_diagnostics_get_model_spec(fdd_drive_model_t model) {
    if (model < DRIVE_MODEL_COUNT) {
        return &s_model_specs[model];
    }
    return &s_model_specs[DRIVE_MODEL_GENERIC_350_HD];
}

/* ========================================================================== */
/* 2. Auto-Probe Heuristics Engine                                            */
/* ========================================================================== */

fdd_drive_model_t fdd_diagnostics_auto_probe(void) {
    /* 1. Preliminary check: are we using the Apple II 20-pin connector? */
    /* If J13 is populated or Apple phases used, choose Apple */

    /* 2. Power on 5V and 12V and monitor currents */
    fdd_power_enable_rail(PWR_RAIL_5V, true);
    HAL_Delay(100);
    fdd_power_enable_rail(PWR_RAIL_12V, true);
    HAL_Delay(150);

    const fdd_power_telemetry_t *pwr = fdd_power_get_telemetry();
    float current_12v = pwr->current_ma[PWR_RAIL_12V];

    /* Turn on motor to measure RPM */
    bsp_fdd_set_drive_select(0, true);
    bsp_fdd_set_motor(true);
    HAL_Delay(800);

    fdd_timing_reset_stats();
    uint32_t start = hal_get_tick_ms();
    while ((hal_get_tick_ms() - start) < 1500U) {
        fdd_timing_update();
        HAL_Delay(10);
    }

    const fdd_tachometer_data_t *tacho = fdd_timing_get_data();

    bsp_fdd_set_motor(false);
    bsp_fdd_set_drive_select(0, false);

    /* Heuristic classification */
    if (tacho->spindle_spinning) {
        if (tacho->average_rpm > 340.0f) {
            /* 360 RPM: 5.25" High Density or 8" */
            if (current_12v > 200.0f) {
                return DRIVE_MODEL_TEAC_FD55GFR;
            }
        } else {
            /* 300 RPM */
            if (current_12v < 80.0f) {
                /* 12V practically unused -> 3.5" Modern PC BLDC */
                return DRIVE_MODEL_GENERIC_350_HD;
            } else {
                /* 12V heavily used -> 5.25" DD (Tandon TM100) or Amstrad 3" */
                return DRIVE_MODEL_TANDON_TM100_2A;
            }
        }
    }

    /* Fallback default if motor stopped or inconclusive */
    return DRIVE_MODEL_GENERIC_350_HD;
}

/* ========================================================================== */
/* 3. Model-Specific Expert Repair Advisor                                    */
/* ========================================================================== */

const char *fdd_diagnostics_get_repair_guide(fdd_drive_model_t model, fdd_fault_code_t code) {
    switch (code) {
        case FAULT_SHORT_CIRCUIT_24V:
            return ">> RIPARAZIONE (+24V Short Circuit):\r\n"
                   "  - Sui drive 8\" (Shugart SA800/SA850): controllare l'avvolgimento del solenoide Head Load.\r\n"
                   "    La resistenza nominale e' circa 25-35 Ohm. Se < 5 Ohm, la bobina e' fusa in corto.\r\n"
                   "  - Verificare il diodo flyback di protezione (1N4004) in parallelo al solenoide.\r\n";

        case FAULT_SHORT_CIRCUIT_12V:
        case FAULT_SHORT_CIRCUIT_5V:
            if (model == DRIVE_MODEL_TANDON_TM100_2A || model == DRIVE_MODEL_SHUGART_SA400) {
                return ">> RIPARAZIONE TANDON / SHUGART 5.25\" (Cortocircuito):\r\n"
                       "  - Causa comunissima: condensatori di disaccoppiamento al tantalio a goccia C1, C2, C15 in cortocircuito.\r\n"
                       "  - Tagliare un terminale del tantalio sospetto o dissaldarlo e sostituire con elettrolitico radiale 10uF 25V o ceramico.\r\n";
            } else if (model == DRIVE_MODEL_SONY_MPF920 || model == DRIVE_MODEL_TEAC_FD235HF) {
                return ">> RIPARAZIONE SONY / TEAC 3.5\" (Cortocircuito):\r\n"
                       "  - Controllare i piccoli condensatori elettrolitici SMD cilindrici in alluminio sulla schedina motore.\r\n"
                       "  - Se hanno rilasciato acido, rimuoverli, lavare le piste con alcool isopropilico e sostituire.\r\n";
            }
            return ">> RIPARAZIONE (Cortocircuito Alimentazione):\r\n"
                   "  - Rilevato corto netto verso GND. Ispezionare la linea con multimetro per isolare il chip o il tantalio guasto.\r\n";

        case FAULT_SPINDLE_STALL_NO_ROTATION:
            if (model == DRIVE_MODEL_CHINON_FB354 || model == DRIVE_MODEL_CHINON_FB357A) {
                return ">> RIPARAZIONE CHINON FB-354 / AMIGA (Mandrino Fermo o Instabile):\r\n"
                       "  - GUASTO NOTORIO AMIGA: Condensatori elettrolitici SMD a barilotto in perdita (leaking caps)!\r\n"
                       "  - 1. Ispezionare la schedina logica/motore: cercare aloni lucidi, ossido verde o odore di pesce/ammoniaca.\r\n"
                       "  - 2. Dissaldare immediatamente C1 (22uF 16V), C2 (1uF 50V), C3 (100uF 6.3V) e condensatori sul circuito motore.\r\n"
                       "  - 3. Lavare a fondo il PCB con alcool isopropilico e spazzolino per rimuovere l'elettrolita conduttivo acido.\r\n"
                       "  - 4. Ricostruire le piste corrose/interrotte sotto i pad prima di montare i condensatori nuovi (consigliati al tantalio o polimero solido).\r\n";
            } else if (model == DRIVE_MODEL_AMSTRAD_EME156) {
                return ">> RIPARAZIONE AMSTRAD EME-156 (Mandrino Fermo):\r\n"
                       "  - GUASTO NOTORIO: La cinghia di trazione originale si liquefa in una sostanza gommosa nera appiccicosa ('black goo').\r\n"
                       "  - 1. Rimuovere il coperchio metallico inferiore svitando le 3 viti a croce.\r\n"
                       "  - 2. Rimuovere con cura i residui di pece dal volano e dalla puleggia motore usando cotton fioc e alcool isopropilico o acetone.\r\n"
                       "  - 3. Installare una nuova cinghia quadrata calibrata (dimensioni: diametro 71mm, sezione 1.2mm x 1.2mm).\r\n";
            } else if (model == DRIVE_MODEL_TANDON_TM100_2A) {
                return ">> RIPARAZIONE TANDON TM100-2A (Mandrino Fermo):\r\n"
                       "  - 1. Ruotare a mano il cono centrale: se bloccato, il cono di bloccaggio e' disallineato o la bronzina e' secca.\r\n"
                       "  - 2. Verificare se la cinghia piatta in gomma da 4 mm e' spezzata o caduta dalla puleggia motore.\r\n"
                       "  - 3. Controllare il fusibile a lamella o la resistenza zavorra sul modulo servo motore posteriore.\r\n";
            } else if (model == DRIVE_MODEL_SHUGART_SA800 || model == DRIVE_MODEL_SHUGART_SA850) {
                return ">> RIPARAZIONE SHUGART 8\" (Mandrino Fermo):\r\n"
                       "  - I drive 8\" SA800 usano un MOTORE AC 115V/230V indipendente: assicurarsi che la vaschetta AC sia alimentata!\r\n"
                       "  - Verificare che il condensatore di avviamento/sfasamento del motore AC (solitamente 1.5uF - 3.5uF 350VAC) non sia aperto.\r\n"
                       "  - Controllare la cinghia piatta larga in gomma che collega il motore al volano inferiore.\r\n";
            } else {
                return ">> RIPARAZIONE 3.5\" BLDC (Mandrino Fermo):\r\n"
                       "  - Meccanica Direct-Drive Brushless: NESSUNA CINGHIA presente!\r\n"
                       "  - Verificare che il rotore magnetico non sfreghi contro il circuito stampato (rimuovere corpi estranei).\r\n"
                       "  - Ispezionare le saldature dei sensori di Hall e del chip driver trifase (es. BA6209, LB1641, M51995).\r\n";
            }

        case FAULT_SPINDLE_SPEED_TOO_SLOW:
        case FAULT_SPINDLE_SPEED_TOO_FAST:
            if (model == DRIVE_MODEL_SHUGART_SA800 || model == DRIVE_MODEL_SHUGART_SA850) {
                return ">> REGOLAZIONE VELOCITA SHUGART 8\" (Puleggia AC Frequenza Rete):\r\n"
                       "  - ATTENZIONE: Questo drive NON HA trimmer di velocita! I giri dipendono dai 50Hz o 60Hz della rete elettrica.\r\n"
                       "  - Se il drive gira a 300 RPM su rete a 50Hz: monta la puleggia USA a 60 Hz! E' necessario sostituire la puleggia motore con la variante europea a 50 Hz (P/N Shugart 50358, diametro maggiorato).\r\n";
            } else if (model == DRIVE_MODEL_TANDON_TM100_2A) {
                return ">> TARATURA VELOCITA TANDON TM100-2A:\r\n"
                       "  - 1. Individuare la schedina del servo motore montata sul telaio posteriore.\r\n"
                       "  - 2. Individuare il potenziometro a trimmer 'R4' (regolazione velocita mandrino).\r\n"
                       "  - 3. Con cacciavite ceramico o isolato, ruotare delicatamente R4 osservando il tachimetro a schermo fino a stabilizzare 300.0 ± 0.5 RPM.\r\n";
            } else if (model == DRIVE_MODEL_TEAC_FD55GFR) {
                return ">> TARATURA VELOCITA TEAC FD-55GFR:\r\n"
                       "  - Modello Dual-Speed: deve girare a 360 RPM per dischi HD (1.2MB) e a 300 RPM per dischi DD (360KB).\r\n"
                       "  - Se la velocita e' errata, controllare il ponticello 'I / II' e il trimmer di taratura sul PCB del motore.\r\n";
            } else if (model == DRIVE_MODEL_JAPAN_3MODE) {
                return ">> CONTROLLO VELOCITA 3-MODE (Target 360 RPM per PC-98):\r\n"
                       "  - Se il drive gira a 300 RPM anziche 360 RPM, il ponticello hardware di modo o il Pin 2 non e' commutato in modalita 1.6MB!\r\n"
                       "  - Controllare il ponticello '3M' / 'MODE' sul retro del drive TEAC FD-235HG o forzare a livello logico opportuno il Pin 2.\r\n";
            } else {
                return ">> TARATURA VELOCITA 3.5\" DIRECT DRIVE:\r\n"
                       "  - La velocita e' agganciata a un oscillatore a quarzo: non dovrebbe richiedere alcuna taratura manuale.\r\n"
                       "  - Se la velocita devia, i condensatori di filtraggio sull'anello PLL della schedina motore hanno perso capacita: sostituirli.\r\n";
            }

        case FAULT_SPINDLE_HIGH_WOW_FLUTTER:
            if (model == DRIVE_MODEL_SHUGART_SA800 || model == DRIVE_MODEL_TANDON_TM100_2A || model == DRIVE_MODEL_AMSTRAD_EME156) {
                return ">> RIDUZIONE WOW & FLUTTER (Drive con Cinghia):\r\n"
                       "  - 1. Sgrassare con alcool isopropilico puro la puleggia motore in ottone e la gola del volano da polvere e residui gommosi.\r\n"
                       "  - 2. La cinghia ha preso una deformazione permanente ('ovalizzazione' per inattivita prolungata): sostituire con cinghia nuova.\r\n"
                       "  - 3. Applicare mezza goccia di olio fine (tipo Singer) sull'alberino centrale della bronzina Oilite (NON sporcare il mandrino!).\r\n";
            } else {
                return ">> RIDUZIONE WOW & FLUTTER (Direct Drive 3.5\"):\r\n"
                       "  - Pulire il perno centrale e il cuscinetto reggispinta da polvere metallica o accumuli di sporco.\r\n"
                       "  - Verificare la planarita del rotore magnetico.\r\n";
            }

        case FAULT_TRACK00_SENSOR_STUCK_OR_BLIND:
            if (model == DRIVE_MODEL_APPLE_DISK_II || model == DRIVE_MODEL_COMMODORE_1541) {
                return ">> NOTA ARCHITETTURA (Nessun Sensore Traccia 00):\r\n"
                       "  - Questa meccanica NON MONTA fisicamente il sensore di Traccia 00! Il calcolo avviene per battuta meccanica.\r\n"
                       "  - Il test e' informativo: verificare che il fermo meccanico di finecorsa non sia allentato o piegato.\r\n";
            } else {
                return ">> RIPARAZIONE SENSORE TRACCIA 00:\r\n"
                       "  - 1. Pulire con un cotton fioc e alcool isopropilico la forcella ottica del sensore Traccia 00.\r\n"
                       "  - 2. Controllare che la bandella o linguetta metallica del carrello entri perfettamente al centro della fenditura ottica a finecorsa.\r\n"
                       "  - 3. Allentare leggermente la vite del sensore sul telaio e regolarne la posizione assiale fino ad agganciare il segnale prima del finecorsa.\r\n";
            }

        case FAULT_STEPPER_MECHANICAL_FRICTION:
            if (model == DRIVE_MODEL_SHUGART_SA400) {
                return ">> LUBRIFICAZIONE SHUGART SA400 (Camma a Spirale):\r\n"
                       "  - L'SA400 adotta una camma elicoidale a spirale (vite Archimedea) su cui poggia un perno a sfera.\r\n"
                       "  - Rimuovere il vecchio grasso secco dalla spirale e applicare un velo di grasso al silicone o PTFE.\r\n";
            } else {
                return ">> PULIZIA & LUBRIFICAZIONE GUIDE SCORRIMENTO:\r\n"
                       "  - 1. Rimuovere il vecchio grasso secco indurito dalle due guide cilindriche in acciaio con un panno imbevuto di alcool isopropilico.\r\n"
                       "  - 2. Pulire accuratamente le gole della vite senza fine dello stepper con uno spazzolino morbido.\r\n"
                       "  - 3. Applicare un velo sottilissimo di grasso sintetico al PTFE (Teflon) o olio sintetico ad alta scorrevolezza.\r\n"
                       "  - 4. Far scorrere a mano delicatamente il carrello per distribuire il film lubrificante prima di ritestare.\r\n";
            }

        case FAULT_STEPPER_STEP_LOSS:
            if (model == DRIVE_MODEL_TANDON_TM100_2A || model == DRIVE_MODEL_SHUGART_SA850) {
                return ">> RIPARAZIONE BANDELLA METALLICA STEPPER:\r\n"
                       "  - Rilevata perdita di passi o gioco assiale: verificare la vite di bloccaggio della bandella in acciaio flessibile sulla puleggia dello stepper.\r\n"
                       "  - Se la bandella e' allentata o piegata, non avra trazione corretta: registrarne la tensione o sostituire la bandella.\r\n";
            } else {
                return ">> RIPARAZIONE VITE SENZA FINE STEPPER:\r\n"
                       "  - Controllare la molla di precarico antibacklash posta sulla chiocciola del carrello testine.\r\n"
                       "  - Se la molletta e' rotta o saltata, il carrello avra gioco avanti/indietro tra i passi.\r\n";
            }

        case FAULT_PIN34_NOT_READY:
            return ">> ANOMALIA SEGNALE READY PIN 34 (Incompatibilita Bus Amiga):\r\n"
                   "  - Il chip Paula di Commodore Amiga richiede obbligatoriamente il segnale READY attivo basso sul Pin 34 quando il motore e' a regime!\r\n"
                   "  - 1. Se si tratta di un drive PC adattato ad Amiga: il drive sta ancora emettendo DISK_CHANGE sul Pin 34 anziche READY. Configurare il ponticello RDY/DC o effettuare la modifica 'ready mod'.\r\n"
                   "  - 2. Su drive Amiga nativo (Chinon FB-354): il microswitch meccanico di rilevamento presenza disco sul frontale e' sporco, ossidato o bloccato.\r\n"
                   "  - 3. Spruzzare disossidante secco contatti nel microswitch e verificarne la continuita.\r\n";

        case FAULT_AMIGA_LEAKY_CAPS:
            return ">> CRITICITA AMIGA: CONDENSATORI SMD IN PERDITA:\r\n"
                   "  - Nei drive Chinon per Amiga, i condensatori SMD elettrolitici rilasciano elettrolita corrosivo.\r\n"
                   "  - Effettuare il recap completo e controllare le piste sotto la CPU di controllo motore.\r\n";

        case FAULT_MAC_AUTO_EJECT_CAUTION:
            return ">> AVVISO MECCANICA APPLE MACINTOSH AUTO-EJECT:\r\n"
                   "  - ATTENZIONE: Questo drive NON possiede un pulsante meccanico frontale di espulsione!\r\n"
                   "  - 1. Per rimuovere il disco di collaudo a fine test, utilizzare una GRAFFETTA METALLICA nel forellino a destra.\r\n"
                   "  - 2. Se l'espulsione motorizzata fallisce sul Mac, pulire i vecchi residui di grasso resinoso dagli ingranaggi dell'auto-eject.\r\n"
                   "  - 3. Verificare i transistor SMD driver Q3 e Q4 (equivalenti a 2SA1298) sulla scheda del drive.\r\n";

        case FAULT_ATARI_DS0_MISCONFIG:
            return ">> CONFIGURAZIONE DRIVE ATARI ST (Selezione DS0):\r\n"
                   "  - L'Atari ST indirizza l'unita interna A: esclusivamente tramite la linea DS0 (Pin 10).\r\n"
                   "  - Se il drive non risponde ai comandi o il LED resta spento, verificare che il jumper sia saldato su DS0 e non su DS1 (default PC).\r\n";

        default:
            return "Nessuna anomalia riscontrata su questo componente.";
    }
}

/* ========================================================================== */
/* 4. Automated Diagnostic Runner                                             */
/* ========================================================================== */

static fdd_diagnostic_report_t s_report;

static void add_subtest_record(const char *name, test_result_t res, float measured,
                               float nominal, float tol, const char *unit,
                               fdd_fault_code_t code, const char *summary) {
    if (s_report.subtest_count < MAX_DIAG_SUBTESTS) {
        fdd_subtest_record_t *rec = &s_report.subtests[s_report.subtest_count++];
        rec->test_name = name;
        rec->result = res;
        rec->measured_val = measured;
        rec->nominal_val = nominal;
        rec->tolerance_val = tol;
        rec->unit_str = unit;
        rec->fault_code = code;
        strncpy(rec->summary, summary, sizeof(rec->summary) - 1);
        rec->summary[sizeof(rec->summary) - 1] = '\0';

        if (res == TEST_RESULT_FAIL) {
            s_report.fault_count++;
            s_report.overall_status = TEST_RESULT_FAIL;
        } else if (res == TEST_RESULT_WARN) {
            s_report.warn_count++;
            if (s_report.overall_status != TEST_RESULT_FAIL) {
                s_report.overall_status = TEST_RESULT_WARN;
            }
        }
    }
}

void fdd_diagnostics_init(void) {
    memset(&s_report, 0, sizeof(s_report));
    s_report.overall_status = TEST_RESULT_PASS;
}

const fdd_diagnostic_report_t *fdd_diagnostics_run_full(
    fdd_drive_model_t model,
    void (*progress_cb)(uint8_t percent, const char *stage),
    bool (*abort_cb)(void)
) {
    uint32_t start_time = hal_get_tick_ms();
    fdd_diagnostics_init();

    if (model == DRIVE_MODEL_AUTO_DETECT) {
        if (progress_cb) progress_cb(2, "Esecuzione Auto-Probe Hardware...");
        model = fdd_diagnostics_auto_probe();
    }

    s_report.selected_model = model;
    s_report.spec = fdd_diagnostics_get_model_spec(model);

    /* ---------------------------------------------------------------------- */
    /* STAGE 1: POWER CHECK & SHORT CIRCUIT TELEMETRY (0% -> 15%)             */
    /* ---------------------------------------------------------------------- */
    if (progress_cb) progress_cb(5, "Verifica Alimentazione & Assorbimenti...");
    bsp_led_busy(true);

    fdd_power_enable_rail(PWR_RAIL_5V, true);
    HAL_Delay(100);
    fdd_power_enable_rail(PWR_RAIL_12V, true);
    if (s_report.spec->requires_24v) {
        HAL_Delay(50);
        fdd_power_enable_rail(PWR_RAIL_24V, true);
    }
    HAL_Delay(200);

    const fdd_power_telemetry_t *pwr = fdd_power_get_telemetry();

    if (pwr->fault_tripped[PWR_RAIL_5V]) {
        add_subtest_record("Alimentazione +5V", TEST_RESULT_FAIL, pwr->peak_current_ma[PWR_RAIL_5V],
                           500.0f, 2500.0f, "mA", FAULT_SHORT_CIRCUIT_5V,
                           "Cortocircuito o sovraccarico sul rail +5V (E-Fuse intervenuto)");
    } else if (pwr->fault_tripped[PWR_RAIL_12V]) {
        add_subtest_record("Alimentazione +12V", TEST_RESULT_FAIL, pwr->peak_current_ma[PWR_RAIL_12V],
                           800.0f, 1800.0f, "mA", FAULT_SHORT_CIRCUIT_12V,
                           "Cortocircuito o sovraccarico sul rail +12V (E-Fuse intervenuto)");
    } else if (s_report.spec->requires_24v && pwr->fault_tripped[PWR_RAIL_24V]) {
        add_subtest_record("Alimentazione +24V", TEST_RESULT_FAIL, pwr->peak_current_ma[PWR_RAIL_24V],
                           1000.0f, 2200.0f, "mA", FAULT_SHORT_CIRCUIT_24V,
                           "Cortocircuito solenoide o motore sul rail +24V");
    } else {
        add_subtest_record("Alimentazione Logica", TEST_RESULT_PASS, pwr->current_ma[PWR_RAIL_5V],
                           500.0f, 1500.0f, "mA", FAULT_NONE,
                           "Assorbimento a vuoto nei limiti nominali");
    }

    if (s_report.overall_status == TEST_RESULT_FAIL || (abort_cb && abort_cb())) {
        bsp_pwr_all_off();
        bsp_led_busy(false);
        s_report.test_duration_ms = hal_get_tick_ms() - start_time;
        return &s_report;
    }

    /* ---------------------------------------------------------------------- */
    /* STAGE 2: SPINDLE ROTATION & TACHOMETER BENCHMARK (15% -> 45%)          */
    /* ---------------------------------------------------------------------- */
    if (progress_cb) progress_cb(20, "Misura Velocita Mandrino & Jitter...");

    bsp_fdd_set_drive_select(0, true);
    bsp_fdd_set_motor(true);

    HAL_Delay(s_report.spec->requires_24v ? 1200 : 700);

    fdd_timing_reset_stats();
    uint32_t sample_start = hal_get_tick_ms();
    while ((hal_get_tick_ms() - sample_start) < 2500U) {
        fdd_timing_update();
        HAL_Delay(10);
        if (abort_cb && abort_cb()) break;
    }

    const fdd_tachometer_data_t *tacho = fdd_timing_get_data();

    if (!tacho->spindle_spinning || tacho->total_index_pulses == 0) {
        add_subtest_record("Rotazione Mandrino (RPM)", TEST_RESULT_FAIL, 0.0f,
                           s_report.spec->nominal_rpm, 3.0f, "RPM", FAULT_SPINDLE_STALL_NO_ROTATION,
                           "Nessun impulso di rotazione rilevato (Mandrino fermo o sensore guasto)");
    } else {
        float delta = tacho->average_rpm - s_report.spec->nominal_rpm;
        float err_pct = (delta / s_report.spec->nominal_rpm) * 100.0f;
        float abs_err = (err_pct < 0) ? -err_pct : err_pct;

        if (abs_err > (s_report.spec->rpm_tolerance_pct * 2.5f)) {
            fdd_fault_code_t fcode = (tacho->average_rpm < s_report.spec->nominal_rpm) ?
                                     FAULT_SPINDLE_SPEED_TOO_SLOW : FAULT_SPINDLE_SPEED_TOO_FAST;
            add_subtest_record("Velocita Mandrino (RPM)", TEST_RESULT_FAIL, tacho->average_rpm,
                               s_report.spec->nominal_rpm, s_report.spec->rpm_tolerance_pct, "RPM", fcode,
                               "Velocita fuori tolleranza rispetto alle specifiche di fabbrica");
        } else if (abs_err > s_report.spec->rpm_tolerance_pct) {
            add_subtest_record("Velocita Mandrino (RPM)", TEST_RESULT_WARN, tacho->average_rpm,
                               s_report.spec->nominal_rpm, s_report.spec->rpm_tolerance_pct, "RPM", FAULT_NONE,
                               "Velocita leggermente scostata dalla taratura ideale");
        } else {
            add_subtest_record("Velocita Mandrino (RPM)", TEST_RESULT_PASS, tacho->average_rpm,
                               s_report.spec->nominal_rpm, s_report.spec->rpm_tolerance_pct, "RPM", FAULT_NONE,
                               "Velocita angolare perfettamente conforme alle specifiche");
        }

        if (tacho->wow_flutter_percent > 1.20f) {
            add_subtest_record("Wow & Flutter (Stabilita)", TEST_RESULT_FAIL, tacho->wow_flutter_percent,
                               0.50f, 0.80f, "%", FAULT_SPINDLE_HIGH_WOW_FLUTTER,
                               "Elevata instabilita di rotazione (Cinghia deformata o puleggia sporca)");
        } else if (tacho->wow_flutter_percent > 0.80f) {
            add_subtest_record("Wow & Flutter (Stabilita)", TEST_RESULT_WARN, tacho->wow_flutter_percent,
                               0.50f, 0.80f, "%", FAULT_NONE,
                               "Fluttuazione velocita al limite di soglia");
        } else {
            add_subtest_record("Wow & Flutter (Stabilita)", TEST_RESULT_PASS, tacho->wow_flutter_percent,
                               0.50f, 0.80f, "%", FAULT_NONE,
                               "Rotazione estremamente fluida e costante");
        }
    }

    /* ---------------------------------------------------------------------- */
    /* STAGE 3: SENSORS FUNCTIONALITY TEST (45% -> 60%)                       */
    /* ---------------------------------------------------------------------- */
    if (progress_cb) progress_cb(50, "Controllo Sensori Ottici & Meccanici...");

    fdd_motion_init(s_report.spec->max_cylinders, s_report.spec->recommended_step_rate);
    fdd_motion_set_mode(s_report.spec->motion_mode);

    if (s_report.spec->has_track0_sensor) {
        bool home_ok = fdd_motion_home();
        if (!home_ok) {
            add_subtest_record("Sensore Traccia 00", TEST_RESULT_FAIL, 0.0f, 1.0f, 0.0f, "",
                               FAULT_TRACK00_SENSOR_STUCK_OR_BLIND,
                               "Sensore Traccia 00 non rilevato o carrello disallineato");
        } else {
            fdd_motion_step(true);
            HAL_Delay(20);
            bool track0_cleared = !bsp_fdd_is_track00();
            fdd_motion_step(false);
            HAL_Delay(20);
            bool track0_reasserted = bsp_fdd_is_track00();

            if (track0_cleared && track0_reasserted) {
                add_subtest_record("Sensore Traccia 00", TEST_RESULT_PASS, 1.0f, 1.0f, 0.0f, "",
                                   FAULT_NONE, "Rilevamento e transizione Traccia 0 perfetti");
            } else {
                add_subtest_record("Sensore Traccia 00", TEST_RESULT_FAIL, 0.0f, 1.0f, 0.0f, "",
                                   FAULT_TRACK00_SENSOR_STUCK_OR_BLIND,
                                   "Segnale Traccia 00 bloccato fisso o isteresi ottica anomala");
            }
        }
    }

    bool wp_state = bsp_fdd_is_write_protected();
    add_subtest_record("Sensore Write Protect", TEST_RESULT_PASS, wp_state ? 1.0f : 0.0f,
                       0.0f, 0.0f, "", FAULT_NONE,
                       wp_state ? "Stato rilevato: Disco Protetto da Scrittura" : "Stato rilevato: Disco Scrivibile");

    if (s_report.spec->model_id == DRIVE_MODEL_CHINON_FB354 || s_report.spec->model_id == DRIVE_MODEL_CHINON_FB357A) {
        /* On Amiga, with motor ON and disk spinning, Pin 34 MUST be READY (0V on bus -> STM32 HIGH via 74HC14) */
        bool ready_pin = bsp_fdd_is_disk_changed();
        if (ready_pin) {
            add_subtest_record("Bus Amiga Pin 34 (READY)", TEST_RESULT_PASS, 1.0f, 1.0f, 0.0f, "",
                               FAULT_NONE, "Segnale READY valido (compatibile Amiga Paula)");
        } else {
            add_subtest_record("Bus Amiga Pin 34 (READY)", TEST_RESULT_FAIL, 0.0f, 1.0f, 0.0f, "",
                               FAULT_PIN34_NOT_READY, "Pin 34 NON asserito a livello basso (Manca READY per Amiga)");
        }
    }

    /* ---------------------------------------------------------------------- */
    /* STAGE 4: STEPPING FRICTION & SPEED BENCHMARK (60% -> 80%)               */
    /* ---------------------------------------------------------------------- */
    if (progress_cb) progress_cb(70, "Benchmark Scorrimento Guide & Stepper...");

    fdd_motion_set_step_rate(s_report.spec->recommended_step_rate);
    fdd_motion_seek(20);
    fdd_motion_seek(0);

    if (s_report.spec->has_track0_sensor && !bsp_fdd_is_track00()) {
        fdd_motion_set_step_rate(STEP_RATE_20MS);
        fdd_motion_home();
        fdd_motion_seek(20);
        fdd_motion_seek(0);

        if (bsp_fdd_is_track00()) {
            add_subtest_record("Scorrimento Carrello", TEST_RESULT_WARN, 20.0f, (float)s_report.spec->recommended_step_rate, 5.0f, "ms",
                               FAULT_STEPPER_MECHANICAL_FRICTION,
                               "Attrito meccanico elevato: richiede passo lento (Guide da pulire/lubrificare)");
        } else {
            add_subtest_record("Scorrimento Carrello", TEST_RESULT_FAIL, 0.0f, 1.0f, 0.0f, "",
                               FAULT_STEPPER_MECHANICAL_FRICTION,
                               "Carrello bloccato o forte resistenza meccanica sullo stepper");
        }
    } else {
        add_subtest_record("Scorrimento Carrello", TEST_RESULT_PASS, (float)s_report.spec->recommended_step_rate,
                           (float)s_report.spec->recommended_step_rate, 0.0f, "ms",
                           FAULT_NONE, "Scorrimento fluido al rate di fabbrica raccomandato");
    }

    /* ---------------------------------------------------------------------- */
    /* STAGE 5: MECHANICAL REPEATABILITY & STEP-LOSS CHECK (80% -> 100%)       */
    /* ---------------------------------------------------------------------- */
    if (progress_cb) progress_cb(90, "Verifica Ripetibilita & Gioco Meccanico...");

    if (s_report.spec->has_track0_sensor) {
        fdd_motion_home();
        uint8_t target_span = (s_report.spec->max_cylinders > 40) ? 40 : 25;
        fdd_motion_seek(target_span);
        HAL_Delay(50);
        fdd_motion_seek(0);
        HAL_Delay(30);

        if (bsp_fdd_is_track00()) {
            add_subtest_record("Precisione Ripetibilita", TEST_RESULT_PASS, 0.0f, 0.0f, 0.0f, "passi",
                               FAULT_NONE, "Ritorno a Traccia 0 senza alcuna perdita di passi");
        } else {
            add_subtest_record("Precisione Ripetibilita", TEST_RESULT_FAIL, 1.0f, 0.0f, 0.0f, "passi",
                               FAULT_STEPPER_STEP_LOSS,
                               "Rilevata perdita di passi (Gioco della vite elicoidale o bandella lasca)");
        }
    }

    bsp_fdd_set_motor(false);
    bsp_fdd_set_drive_select(0, false);
    bsp_led_busy(false);

    if (s_report.overall_status == TEST_RESULT_PASS) {
        bsp_led_ready(true);
        bsp_buzzer_beep(2500, 150);
    } else {
        bsp_led_fault(true);
        bsp_buzzer_beep(1000, 400);
    }

    if (progress_cb) progress_cb(100, "Collaudo Completato!");
    s_report.test_duration_ms = hal_get_tick_ms() - start_time;
    return &s_report;
}

void fdd_diagnostics_print_report(const fdd_diagnostic_report_t *rep) {
    cli_console_puts("\r\n======================================================================\r\n");
    cli_console_puts("             RETRO-DIAG FDD MASTER TESTER - REFERTO COLLAUDO           \r\n");
    cli_console_puts("======================================================================\r\n");

    cli_console_printf("Modello Selezionato: %s (%s)\r\n", rep->spec->display_name, rep->spec->size_str);
    cli_console_printf("Target Fabbrica    : %4.1f RPM (±%2.1f%%) | %d Tracce | Step Rate: %d ms\r\n",
                       rep->spec->nominal_rpm, rep->spec->rpm_tolerance_pct,
                       rep->spec->max_cylinders, rep->spec->recommended_step_rate);
    cli_console_printf("Manuale Ufficiale  : %s\r\n", rep->spec->oem_manual_url);
    cli_console_printf("Durata Test        : %4.1f s\r\n", (float)rep->test_duration_ms / 1000.0f);
    cli_console_printf("Esito Complessivo  : [%s]  (Errori: %d | Avvisi: %d)\r\n",
                       (rep->overall_status == TEST_RESULT_PASS) ? "PASS - PERFETTAMENTE OPERATIVO" :
                       (rep->overall_status == TEST_RESULT_WARN) ? "WARN - REVISIONE CONSIGLIATA" :
                                                                  "FAIL - GUASTO BLOCCANTE RILEVATO",
                       rep->fault_count, rep->warn_count);
    cli_console_puts("----------------------------------------------------------------------\r\n");

    for (uint8_t i = 0; i < rep->subtest_count; i++) {
        const fdd_subtest_record_t *r = &rep->subtests[i];
        const char *tag = (r->result == TEST_RESULT_PASS) ? "[ PASS ]" :
                          (r->result == TEST_RESULT_WARN) ? "[ WARN ]" : "[ FAIL ]";

        cli_console_printf("%s %-26s : %s\r\n", tag, r->test_name, r->summary);
        if (r->unit_str && strlen(r->unit_str) > 0) {
            cli_console_printf("         -> Valore Misurato: %5.1f %s (Nominale: %5.1f %s)\r\n",
                               r->measured_val, r->unit_str, r->nominal_val, r->unit_str);
        }
    }

    cli_console_puts("======================================================================\r\n");
    cli_console_puts("               PRESCRIZIONI TECNICHE & GUIDA ALLA RIPARAZIONE         \r\n");
    cli_console_puts("======================================================================\r\n");

    if (rep->fault_count == 0 && rep->warn_count == 0) {
        cli_console_puts(">> NESSUN INTERVENTO RICHIESTO!\r\n");
        cli_console_puts("   Il drive rispetta pienamente tutti i parametri di fabbrica OEM.\r\n");
    } else {
        for (uint8_t i = 0; i < rep->subtest_count; i++) {
            const fdd_subtest_record_t *r = &rep->subtests[i];
            if (r->fault_code != FAULT_NONE) {
                cli_console_printf("\r\n--- ANOMALIA: %s ---\r\n", r->test_name);
                cli_console_puts(fdd_diagnostics_get_repair_guide(rep->selected_model, r->fault_code));
                cli_console_printf("   -> Consulta il Service Manual Ufficiale per gli schemi: %s\r\n", rep->spec->oem_manual_url);
            }
        }
    }

    cli_console_puts("======================================================================\r\n\r\n");
}
