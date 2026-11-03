/**
 * @file    cli_console.c
 * @brief   Diagnostic Serial Command Line Interface (CLI) Implementation
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 */

#include "cli_console.h"
#include "bsp_fdd_gpio.h"
#include "fdd_power_monitor.h"
#include "fdd_motion.h"
#include "fdd_timing_capture.h"
#include "fdd_diagnostics.h"
#include "fdd_analog_scope.h"
#include "fdd_burnin.h"
#include "fdd_flux_analyzer.h"

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdarg.h>

#define CLI_BUFFER_SIZE         128U
static char s_rx_buffer[CLI_BUFFER_SIZE];
static uint8_t s_rx_index = 0;

/* Weak output function - can be redirected to USART1 or USB CDC */
__attribute__((weak)) void cli_put_char(char c) {
    (void)c;
}

void cli_console_puts(const char *str) {
    while (*str) {
        cli_put_char(*str++);
    }
}

void cli_console_printf(const char *fmt, ...) {
    char buf[160];
    va_list args;
    va_start(args, fmt);
    vsnprintf(buf, sizeof(buf), fmt, args);
    va_end(args);
    cli_console_puts(buf);
}

static void cmd_help(void) {
    cli_console_puts("\r\n=== Retro-Diag FDD Master Tester CLI Commands ===\r\n");
    cli_console_puts("  diag [model]           - Esegui Collaudo Automatico (es: diag tandon, diag teac55, diag sa800, diag amstrad, diag)\r\n");
    cli_console_puts("  models                 - Elenca i modelli di drive supportati nel database OEM con link ai manuali\r\n");
    cli_console_puts("  status                 - Print full system telemetry & sensors\r\n");
    cli_console_puts("  pwr <rail> <on|off>    - Control rail (24v, 12v, 5v, all)\r\n");
    cli_console_puts("  motor <on|off>         - Spindle motor control\r\n");
    cli_console_puts("  select <0|1> <on|off>  - Floppy Drive Select line\r\n");
    cli_console_puts("  side <0|1>             - Head side select\r\n");
    cli_console_puts("  home                   - Auto-seek to Track 00\r\n");
    cli_console_puts("  seek <cyl>             - Seek to cylinder (0..79)\r\n");
    cli_console_puts("  step <in|out> [count]  - Single or multi-step\r\n");
    cli_console_puts("  rate <ms>              - Set step rate (2, 3, 6, 8, 12, 20, 30 ms)\r\n");
    cli_console_puts("  align <center_cyl>     - Run Dysan/Teaco alignment cycle\r\n");
    cli_console_puts("  rpm                    - Read tachometer speed & flutter\r\n");
    cli_console_puts("  clear                  - Clear overcurrent trip flags\r\n");
    cli_console_puts("  scope [side]           - Cat's Eye Alignment Scope metrics (TP1/TP2 Vpp, symmetry, azimuth)\r\n");
    cli_console_puts("  burnin <start|stop|stat> [cycles] - Endurance Torture Test engine\r\n");
    cli_console_puts("  flux [side] [track]    - MFM Flux transition interval capture & histogram\r\n");
    cli_console_puts("  json                   - Output compact JSON real-time telemetry frame\r\n");
    cli_console_puts("  beep                   - Sound buzzer test tone\r\n");
    cli_console_puts("=================================================\r\n");
}

static void cmd_models(void) {
    cli_console_puts("\r\n=== DATABASE PROFILI DRIVE & SERVICE MANUALS DISPONIBILI ===\r\n");
    for (int i = 1; i < DRIVE_MODEL_COUNT; i++) {
        const fdd_model_spec_t *m = fdd_diagnostics_get_model_spec((fdd_drive_model_t)i);
        cli_console_printf("[%2d] %-36s | %5.0f RPM | %2d Trk | Step: %2d ms\r\n",
                           i, m->display_name, m->nominal_rpm, m->max_cylinders, m->recommended_step_rate);
        cli_console_printf("     Manuale OEM: %s\r\n", m->oem_manual_url);
    }
    cli_console_puts("============================================================\r\n");
    cli_console_puts("Uso: 'diag <nome_modello>' o 'diag <numero>' (es: 'diag tandon' o 'diag 4')\r\n\r\n");
}

static void cmd_status(void) {
    const fdd_power_telemetry_t *pwr = fdd_power_get_telemetry();
    const fdd_motion_state_t    *mot = fdd_motion_get_state();
    const fdd_tachometer_data_t *rpm = fdd_timing_get_data();

    cli_console_puts("\r\n--- SYSTEM TELEMETRY ---\r\n");
    cli_console_printf("Power Rails:\r\n");
    cli_console_printf("  +24V: [%s]  Cur: %4.0f mA  (Peak: %4.0f mA, Lim: %4.0f mA) Trip: %s\r\n",
                       pwr->rail_enabled[PWR_RAIL_24V] ? "ON " : "OFF",
                       pwr->current_ma[PWR_RAIL_24V], pwr->peak_current_ma[PWR_RAIL_24V],
                       pwr->limit_ma[PWR_RAIL_24V], pwr->fault_tripped[PWR_RAIL_24V] ? "YES" : "NO");

    cli_console_printf("  +12V: [%s]  Cur: %4.0f mA  (Peak: %4.0f mA, Lim: %4.0f mA) Trip: %s\r\n",
                       pwr->rail_enabled[PWR_RAIL_12V] ? "ON " : "OFF",
                       pwr->current_ma[PWR_RAIL_12V], pwr->peak_current_ma[PWR_RAIL_12V],
                       pwr->limit_ma[PWR_RAIL_12V], pwr->fault_tripped[PWR_RAIL_12V] ? "YES" : "NO");

    cli_console_printf("  +5V : [%s]  Cur: %4.0f mA  (Peak: %4.0f mA, Lim: %4.0f mA) Trip: %s\r\n",
                       pwr->rail_enabled[PWR_RAIL_5V] ? "ON " : "OFF",
                       pwr->current_ma[PWR_RAIL_5V], pwr->peak_current_ma[PWR_RAIL_5V],
                       pwr->limit_ma[PWR_RAIL_5V], pwr->fault_tripped[PWR_RAIL_5V] ? "YES" : "NO");

    cli_console_puts("Sensors:\r\n");
    cli_console_printf("  TRACK00: %s | WP: %s | DISK_CHG: %s | INDEX_RAW: %s\r\n",
                       bsp_fdd_is_track00() ? "ACTIVE (T0)" : "NO",
                       bsp_fdd_is_write_protected() ? "PROTECTED" : "UNPROTECTED",
                       bsp_fdd_is_disk_changed() ? "CHANGED" : "CLOSED",
                       bsp_fdd_get_index_raw() ? "HIGH" : "LOW");

    cli_console_puts("Motion:\r\n");
    cli_console_printf("  Cylinder: %d / %d | Rate: %d ms | Homed: %s\r\n",
                       mot->current_cylinder, mot->max_cylinders - 1,
                       mot->step_rate_ms, mot->is_homed ? "YES" : "NO");

    cli_console_puts("Tachometer:\r\n");
    cli_console_printf("  RPM: %5.1f (Avg: %5.1f) | Wow/Flutter: %3.2f%% | Pulses: %u\r\n",
                       rpm->current_rpm, rpm->average_rpm,
                       rpm->wow_flutter_percent, rpm->total_index_pulses);
    cli_console_puts("------------------------\r\n");
}

static void cmd_json(void) {
    const fdd_power_telemetry_t *pwr = fdd_power_get_telemetry();
    const fdd_motion_state_t    *mot = fdd_motion_get_state();
    const fdd_tachometer_data_t *rpm = fdd_timing_get_data();

    cli_console_printf("{\"telemetry\":{"
                       "\"pwr\":{\"5v\":{\"on\":%d,\"ma\":%.1f,\"lim\":%.0f,\"trip\":%d},"
                       "\"12v\":{\"on\":%d,\"ma\":%.1f,\"lim\":%.0f,\"trip\":%d},"
                       "\"24v\":{\"on\":%d,\"ma\":%.1f,\"lim\":%.0f,\"trip\":%d}},"
                       "\"motion\":{\"cyl\":%d,\"max\":%d,\"rate\":%d,\"homed\":%d},"
                       "\"tach\":{\"rpm\":%.1f,\"avg\":%.1f,\"flutter\":%.2f,\"pulses\":%u},"
                       "\"sensors\":{\"trk0\":%d,\"wp\":%d,\"chg\":%d,\"index\":%d}"
                       "}}\r\n",
                       pwr->rail_enabled[PWR_RAIL_5V] ? 1 : 0, pwr->current_ma[PWR_RAIL_5V], pwr->limit_ma[PWR_RAIL_5V], pwr->fault_tripped[PWR_RAIL_5V] ? 1 : 0,
                       pwr->rail_enabled[PWR_RAIL_12V] ? 1 : 0, pwr->current_ma[PWR_RAIL_12V], pwr->limit_ma[PWR_RAIL_12V], pwr->fault_tripped[PWR_RAIL_12V] ? 1 : 0,
                       pwr->rail_enabled[PWR_RAIL_24V] ? 1 : 0, pwr->current_ma[PWR_RAIL_24V], pwr->limit_ma[PWR_RAIL_24V], pwr->fault_tripped[PWR_RAIL_24V] ? 1 : 0,
                       mot->current_cylinder, mot->max_cylinders, mot->step_rate_ms, mot->is_homed ? 1 : 0,
                       rpm->current_rpm, rpm->average_rpm, rpm->wow_flutter_percent, rpm->total_index_pulses,
                       bsp_fdd_is_track00() ? 1 : 0,
                       bsp_fdd_is_write_protected() ? 1 : 0,
                       bsp_fdd_is_disk_changed() ? 1 : 0,
                       bsp_fdd_get_index_raw() ? 1 : 0);
}

static void cmd_scope(uint8_t side) {
    cli_console_printf("Sampling Cat's Eye Scope (Side %d)...\r\n", side);
    const fdd_cat_eye_metrics_t *m = fdd_analog_scope_sample(side);
    if (!m) {
        cli_console_puts("ERROR: Failed to sample scope ADC channels!\r\n");
        return;
    }
    cli_console_printf("  TP1 Vpp: %4.1f mV | TP2 Vpp: %4.1f mV\r\n", m->vpp_tp1_mv, m->vpp_tp2_mv);
    cli_console_printf("  Symmetry: %5.1f%% | Azimuth Offset: %+.2f deg\r\n", m->symmetry_percent, m->azimuth_degrees);
    cli_console_printf("  Calibrated Flag: %s\r\n", m->is_calibrated ? "YES" : "NO");
    cli_console_printf("{\"scope\":{\"side\":%d,\"tp1_mv\":%.1f,\"tp2_mv\":%.1f,\"sym_pct\":%.1f,\"azimuth\":%.2f}}\r\n",
                       side, m->vpp_tp1_mv, m->vpp_tp2_mv, m->symmetry_percent, m->azimuth_degrees);
}

static void cmd_burnin(const char *action, uint32_t cycles) {
    if (!action || strcmp(action, "stat") == 0 || strcmp(action, "status") == 0) {
        const fdd_burnin_status_t *st = fdd_burnin_get_status();
        cli_console_puts("\r\n--- BURN-IN TORTURE TEST STATUS ---\r\n");
        cli_console_printf("  State: %s | Cycles: %u / %u (%.1f%%)\r\n",
                           st->is_running ? "RUNNING" : "STOPPED",
                           st->completed_cycles, st->target_cycles,
                           st->target_cycles ? ((float)st->completed_cycles / st->target_cycles * 100.0f) : 0.0f);
        cli_console_printf("  Current Drift: %+.1f%% (Initial: %.1f mA, Cur: %.1f mA)\r\n",
                           st->thermal_current_drift_pct, st->initial_motor_current_ma, st->current_motor_current_ma);
        cli_console_printf("  Homing Losses: %u | Step Errors: %u\r\n",
                           st->homing_loss_count, st->total_step_errors);
        cli_console_puts("-----------------------------------\r\n");
    } else if (strcmp(action, "start") == 0) {
        uint32_t target = (cycles > 0) ? cycles : 500;
        fdd_burnin_config_t cfg = {
            .target_cycles = target,
            .start_track = 0,
            .end_track = 79,
            .step_rate = STEP_RATE_3MS,
            .invert_pattern = true
        };
        fdd_burnin_start(&cfg);
        cli_console_printf("Endurance Burn-in STARTED (Target: %u cycles, Tracks 0..79)\r\n", target);
    } else if (strcmp(action, "stop") == 0) {
        fdd_burnin_stop();
        cli_console_puts("Endurance Burn-in STOPPED.\r\n");
    }
}

static void cmd_flux(uint8_t side, uint8_t trk) {
    cli_console_printf("Capturing MFM flux transition intervals (Side %d, Trk %d)...\r\n", side, trk);
    const fdd_flux_analysis_t *fa = fdd_flux_analyzer_capture_revolution(side, trk);
    if (!fa) {
        cli_console_puts("ERROR: Flux capture failed!\r\n");
        return;
    }
    const char *dens = "UNKNOWN";
    if (fa->detected_density == FLUX_DENSITY_DD_250K) dens = "DD 250kbps (720KB/360KB)";
    else if (fa->detected_density == FLUX_DENSITY_DD_300K) dens = "DD 300kbps (1.2MB 300rpm)";
    else if (fa->detected_density == FLUX_DENSITY_HD_500K) dens = "HD 500kbps (1.44MB/1.2MB)";
    else if (fa->detected_density == FLUX_DENSITY_ED_1000K) dens = "ED 1000kbps (2.88MB)";

    cli_console_printf("  Density: %s\r\n", dens);
    cli_console_printf("  Total Transitions: %u | Bitcell: %.1f ns\r\n",
                       fa->total_flux_transitions, fa->nominal_bitcell_ns);
    cli_console_printf("  Interval Range: %.1f .. %.1f ns | Dropouts: %u\r\n",
                       fa->min_interval_ns, fa->max_interval_ns, fa->dropouts);

    cli_console_puts("  Histogram (0..8us in 0.5us steps):\r\n  [");
    for (int i = 0; i < 32; i++) {
        cli_console_printf("%u%s", fa->histogram[i], (i == 31) ? "" : ",");
    }
    cli_console_puts("]\r\n");
}

static void parse_and_execute(char *cmd) {
    char *token = strtok(cmd, " \r\n");
    if (!token) return;

    if (strcmp(token, "help") == 0) {
        cmd_help();
    } else if (strcmp(token, "models") == 0) {
        cmd_models();
    } else if (strcmp(token, "diag") == 0 || strcmp(token, "test") == 0) {
        char *type_str = strtok(NULL, " ");
        fdd_drive_model_t dtype = DRIVE_MODEL_AUTO_DETECT;
        if (type_str) {
            int num = atoi(type_str);
            if (num >= 1 && num < DRIVE_MODEL_COUNT) {
                dtype = (fdd_drive_model_t)num;
            } else if (strstr(type_str, "tandon") || strstr(type_str, "tm100")) {
                dtype = DRIVE_MODEL_TANDON_TM100_2A;
            } else if (strstr(type_str, "teac55") || strstr(type_str, "55g")) {
                dtype = DRIVE_MODEL_TEAC_FD55GFR;
            } else if (strstr(type_str, "teac235") || strstr(type_str, "fd235")) {
                dtype = DRIVE_MODEL_TEAC_FD235HF;
            } else if (strstr(type_str, "sony") || strstr(type_str, "mpf")) {
                dtype = DRIVE_MODEL_SONY_MPF920;
            } else if (strstr(type_str, "sa800") || strstr(type_str, "800")) {
                dtype = DRIVE_MODEL_SHUGART_SA800;
            } else if (strstr(type_str, "sa850") || strstr(type_str, "850")) {
                dtype = DRIVE_MODEL_SHUGART_SA850;
            } else if (strstr(type_str, "sa400") || strstr(type_str, "400")) {
                dtype = DRIVE_MODEL_SHUGART_SA400;
            } else if (strstr(type_str, "amiga") || strstr(type_str, "fb354") || strstr(type_str, "chinon")) {
                dtype = DRIVE_MODEL_CHINON_FB354;
            } else if (strstr(type_str, "fb357") || strstr(type_str, "amiga-hd")) {
                dtype = DRIVE_MODEL_CHINON_FB357A;
            } else if (strstr(type_str, "atari") || strstr(type_str, "smd380")) {
                dtype = DRIVE_MODEL_ATARI_ST_EPSON;
            } else if (strstr(type_str, "3mode") || strstr(type_str, "pc98") || strstr(type_str, "235hg")) {
                dtype = DRIVE_MODEL_JAPAN_3MODE;
            } else if (strstr(type_str, "superdrive") || strstr(type_str, "mac") || strstr(type_str, "f75w")) {
                dtype = DRIVE_MODEL_APPLE_MAC_SUPERDRIVE;
            } else if (strstr(type_str, "amstrad") || strstr(type_str, "eme")) {
                dtype = DRIVE_MODEL_AMSTRAD_EME156;
            } else if (strstr(type_str, "apple") || strstr(type_str, "disk2")) {
                dtype = DRIVE_MODEL_APPLE_DISK_II;
            } else if (strstr(type_str, "1541") || strstr(type_str, "cbm")) {
                dtype = DRIVE_MODEL_COMMODORE_1541;
            } else if (strstr(type_str, "350") || strstr(type_str, "1.44")) {
                dtype = DRIVE_MODEL_GENERIC_350_HD;
            }
        }
        cli_console_puts("Avvio Collaudo Automatico Multi-Punto in corso...\r\n");
        const fdd_diagnostic_report_t *rep = fdd_diagnostics_run_full(dtype, NULL, bsp_btn_back_pressed);
        fdd_diagnostics_print_report(rep);
    } else if (strcmp(token, "status") == 0) {
        cmd_status();
    } else if (strcmp(token, "pwr") == 0) {
        char *rail_str = strtok(NULL, " ");
        char *state_str = strtok(NULL, " ");
        if (rail_str && state_str) {
            bool on = (strcmp(state_str, "on") == 0);
            if (strcmp(rail_str, "all") == 0) {
                fdd_power_enable_all(on);
                cli_console_printf("All rails set to %s\r\n", on ? "ON" : "OFF");
            } else if (strcmp(rail_str, "24v") == 0) {
                fdd_power_enable_rail(PWR_RAIL_24V, on);
                cli_console_printf("+24V rail set to %s\r\n", on ? "ON" : "OFF");
            } else if (strcmp(rail_str, "12v") == 0) {
                fdd_power_enable_rail(PWR_RAIL_12V, on);
                cli_console_printf("+12V rail set to %s\r\n", on ? "ON" : "OFF");
            } else if (strcmp(rail_str, "5v") == 0) {
                fdd_power_enable_rail(PWR_RAIL_5V, on);
                cli_console_printf("+5V rail set to %s\r\n", on ? "ON" : "OFF");
            }
        }
    } else if (strcmp(token, "motor") == 0) {
        char *state_str = strtok(NULL, " ");
        if (state_str) {
            bool on = (strcmp(state_str, "on") == 0);
            bsp_fdd_set_motor(on);
            cli_console_printf("Spindle motor set to %s\r\n", on ? "ON" : "OFF");
        }
    } else if (strcmp(token, "select") == 0) {
        char *num_str = strtok(NULL, " ");
        char *state_str = strtok(NULL, " ");
        if (num_str && state_str) {
            uint8_t dnum = (uint8_t)atoi(num_str);
            bool on = (strcmp(state_str, "on") == 0);
            bsp_fdd_set_drive_select(dnum, on);
            cli_console_printf("Drive Select %d set to %s\r\n", dnum, on ? "ON" : "OFF");
        }
    } else if (strcmp(token, "side") == 0) {
        char *side_str = strtok(NULL, " ");
        if (side_str) {
            uint8_t side = (uint8_t)atoi(side_str);
            bsp_fdd_set_side(side);
            cli_console_printf("Head Side set to %d\r\n", side);
        }
    } else if (strcmp(token, "home") == 0) {
        cli_console_puts("Recalibrating to Track 00...\r\n");
        if (fdd_motion_home()) {
            cli_console_puts("Homing successful! At Track 00.\r\n");
        } else {
            cli_console_puts("HOMING ERROR: Track 00 sensor not detected!\r\n");
        }
    } else if (strcmp(token, "seek") == 0) {
        char *cyl_str = strtok(NULL, " ");
        if (cyl_str) {
            uint8_t target = (uint8_t)atoi(cyl_str);
            cli_console_printf("Seeking to Cylinder %d...\r\n", target);
            fdd_motion_seek(target);
            cli_console_printf("Now at Cylinder %d\r\n", fdd_motion_get_state()->current_cylinder);
        }
    } else if (strcmp(token, "step") == 0) {
        char *dir_str = strtok(NULL, " ");
        char *cnt_str = strtok(NULL, " ");
        if (dir_str) {
            bool inward = (strcmp(dir_str, "in") == 0);
            uint8_t count = cnt_str ? (uint8_t)atoi(cnt_str) : 1;
            fdd_motion_step_multiple(inward, count);
            cli_console_printf("Stepped %d times %s. Current cylinder: %d\r\n",
                               count, inward ? "IN" : "OUT", fdd_motion_get_state()->current_cylinder);
        }
    } else if (strcmp(token, "rate") == 0) {
        char *ms_str = strtok(NULL, " ");
        if (ms_str) {
            uint8_t r = (uint8_t)atoi(ms_str);
            fdd_motion_set_step_rate((fdd_step_rate_t)r);
            cli_console_printf("Step rate set to %d ms\r\n", r);
        }
    } else if (strcmp(token, "align") == 0) {
        char *center_str = strtok(NULL, " ");
        uint8_t center = center_str ? (uint8_t)atoi(center_str) : 40;
        cli_console_printf("Starting Alignment Cycle around cylinder %d...\r\n", center);
        fdd_motion_cycle_alignment(center);
        cli_console_puts("Alignment cycle complete.\r\n");
    } else if (strcmp(token, "rpm") == 0) {
        const fdd_tachometer_data_t *rpm = fdd_timing_get_data();
        cli_console_printf("Instant RPM: %5.1f | Avg RPM: %5.1f | Min: %5.1f | Max: %5.1f | Wow/Flutter: %3.2f%%\r\n",
                           rpm->current_rpm, rpm->average_rpm, rpm->min_rpm, rpm->max_rpm, rpm->wow_flutter_percent);
    } else if (strcmp(token, "clear") == 0) {
        fdd_power_clear_faults();
        cli_console_puts("Fault flags cleared.\r\n");
    } else if (strcmp(token, "beep") == 0) {
        bsp_buzzer_beep(1500, 150);
        cli_console_puts("Beep!\r\n");
    } else if (strcmp(token, "json") == 0 || strcmp(token, "telemetry") == 0) {
        cmd_json();
    } else if (strcmp(token, "scope") == 0 || strcmp(token, "analog") == 0) {
        char *side_str = strtok(NULL, " ");
        uint8_t side = side_str ? (uint8_t)atoi(side_str) : 0;
        cmd_scope(side);
    } else if (strcmp(token, "burnin") == 0) {
        char *act_str = strtok(NULL, " ");
        char *cyc_str = strtok(NULL, " ");
        uint32_t cyc = cyc_str ? (uint32_t)atoi(cyc_str) : 500;
        cmd_burnin(act_str, cyc);
    } else if (strcmp(token, "flux") == 0) {
        char *side_str = strtok(NULL, " ");
        char *trk_str = strtok(NULL, " ");
        uint8_t side = side_str ? (uint8_t)atoi(side_str) : 0;
        uint8_t trk = trk_str ? (uint8_t)atoi(trk_str) : fdd_motion_get_state()->current_cylinder;
        cmd_flux(side, trk);
    } else {
        cli_console_printf("Unknown command: '%s'. Type 'help' for command list.\r\n", token);
    }
}

void cli_console_init(void) {
    s_rx_index = 0;
    cli_console_puts("\r\n=================================================\r\n");
    cli_console_puts("  Retro-Diag FDD Master Tester Diagnostic Console\r\n");
    cli_console_puts("  Author: Alessio Iodice <alessio67@gmail.com>\r\n");
    cli_console_puts("  Hardware: STM32F407VET6 | KiCad 9 Validated\r\n");
    cli_console_puts("  Type 'help' to display available commands.\r\n");
    cli_console_puts("=================================================\r\n");
    cli_console_puts("FDD-Tester> ");
}

void cli_console_process_char(char c) {
    if (c == '\r' || c == '\n') {
        cli_put_char('\r');
        cli_put_char('\n');
        if (s_rx_index > 0) {
            s_rx_buffer[s_rx_index] = '\0';
            parse_and_execute(s_rx_buffer);
            s_rx_index = 0;
        }
        cli_console_puts("FDD-Tester> ");
    } else if (c == '\b' || c == 0x7F) {
        if (s_rx_index > 0) {
            s_rx_index--;
            cli_console_puts("\b \b");
        }
    } else {
        if (s_rx_index < (CLI_BUFFER_SIZE - 1)) {
            s_rx_buffer[s_rx_index++] = c;
            cli_put_char(c); /* Local echo */
        }
    }
}
