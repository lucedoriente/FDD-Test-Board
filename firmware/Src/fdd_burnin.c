/**
 * @file    fdd_burnin.c
 * @brief   Endurance Burn-In & Long-Term Stress Testing Engine Implementation
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 */

#include "fdd_burnin.h"
#include "fdd_motion.h"
#include "fdd_power_monitor.h"
#include "bsp_fdd_gpio.h"
#include "hal_display.h"
#include <string.h>

static fdd_burnin_config_t s_cfg;
static fdd_burnin_status_t s_status;
static uint32_t s_start_time_ms = 0;
static uint8_t  s_burnin_substep = 0;

void fdd_burnin_start(const fdd_burnin_config_t *cfg) {
    if (cfg) {
        memcpy(&s_cfg, cfg, sizeof(s_cfg));
    } else {
        /* Defaults: 500 cycles on 80 tracks, 3ms step rate */
        s_cfg.target_cycles = 500;
        s_cfg.start_track = 0;
        s_cfg.end_track = 79;
        s_cfg.step_rate = STEP_RATE_3MS;
        s_cfg.homing_check_interval = 25;
        s_cfg.max_allowed_current_ma = 450.0f;
    }

    memset(&s_status, 0, sizeof(s_status));
    s_status.is_running = true;
    s_burnin_substep = 0;
    s_start_time_ms = hal_get_tick_ms();

    /* Arm motor and configure motion */
    bsp_fdd_set_drive_select(0, true);
    bsp_fdd_set_motor(true);
    fdd_motion_init(s_cfg.end_track + 1, s_cfg.step_rate);
    fdd_motion_home();

    /* Sample cold baseline current on +12V */
    hal_delay_ms(150);
    const fdd_power_metrics_t *pwr = fdd_power_get_metrics();
    s_status.baseline_12v_current_ma = pwr->current_12v_ma;
    if (s_status.baseline_12v_current_ma < 50.0f) {
        s_status.baseline_12v_current_ma = 180.0f; /* Nominal default */
    }
}

bool fdd_burnin_update(void) {
    if (!s_status.is_running) return false;

    uint32_t now = hal_get_tick_ms();
    s_status.elapsed_seconds = (now - s_start_time_ms) / 1000U;

    /* 1. Thermal & Friction Current Monitoring */
    const fdd_power_metrics_t *pwr = fdd_power_get_metrics();
    s_status.current_12v_current_ma = pwr->current_12v_ma;

    if (s_status.baseline_12v_current_ma > 10.0f) {
        s_status.current_drift_percent = ((s_status.current_12v_current_ma - s_status.baseline_12v_current_ma) /
                                          s_status.baseline_12v_current_ma) * 100.0f;
    }

    /* Abort if motor bearing friction causes thermal overload */
    if (s_status.current_12v_current_ma > s_cfg.max_allowed_current_ma && s_status.current_drift_percent > 35.0f) {
        s_status.aborted_due_to_friction = true;
        fdd_burnin_stop();
        return false;
    }

    /* Check manual emergency abort button */
    if (bsp_btn_back_pressed()) {
        s_status.aborted_due_to_user = true;
        fdd_burnin_stop();
        return false;
    }

    /* 2. Motion Cycle Execution (State Machine) */
    if (s_burnin_substep == 0) {
        /* Seek inward to end track */
        fdd_motion_seek(s_cfg.end_track);
        s_burnin_substep = 1;
    } else {
        /* Seek outward to start track */
        fdd_motion_seek(s_cfg.start_track);
        s_burnin_substep = 0;
        s_status.completed_cycles++;

        /* 3. Periodic Track 00 Homing & Step Loss Audit */
        if ((s_status.completed_cycles % s_cfg.homing_check_interval) == 0) {
            if (!bsp_fdd_is_track00()) {
                /* Step loss detected! */
                s_status.total_step_loss_events++;
                fdd_motion_home(); /* Recover */
            }
        }

        /* Check if target cycles reached */
        if (s_status.completed_cycles >= s_cfg.target_cycles) {
            fdd_burnin_stop();
            return false;
        }
    }

    return true;
}

void fdd_burnin_stop(void) {
    s_status.is_running = false;
    fdd_motion_seek(0);
    bsp_fdd_set_motor(false);
    bsp_fdd_set_drive_select(0, false);
}

const fdd_burnin_status_t *fdd_burnin_get_status(void) {
    return &s_status;
}
