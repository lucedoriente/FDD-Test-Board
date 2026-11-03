/**
 * @file    fdd_motion.c
 * @brief   Floppy Disk Stepper Motion & Seek Engine Implementation
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 */

#include "fdd_motion.h"
#include "bsp_fdd_gpio.h"

extern void HAL_Delay(uint32_t Delay);

static fdd_motion_state_t s_state;

/* Direct 4-phase Stepper Phase Sequence Tables */
static const uint8_t s_full_step_table[4] = {
    0x03,   /* PH0 + PH1 active */
    0x06,   /* PH1 + PH2 active */
    0x0C,   /* PH2 + PH3 active */
    0x09    /* PH3 + PH0 active */
};

static const uint8_t s_half_step_table[8] = {
    0x01,   /* PH0 */
    0x03,   /* PH0 + PH1 */
    0x02,   /* PH1 */
    0x06,   /* PH1 + PH2 */
    0x04,   /* PH2 */
    0x0C,   /* PH2 + PH3 */
    0x08,   /* PH3 */
    0x09    /* PH3 + PH0 */
};

static const uint8_t s_wave_step_table[4] = {
    0x01,   /* PH0 */
    0x02,   /* PH1 */
    0x04,   /* PH2 */
    0x08    /* PH3 */
};

static void apply_4phase_output(uint8_t mask) {
    /* Write to PE0..PE3 via BSRR */
    uint32_t set_mask = (mask & 0x0F);
    uint32_t clr_mask = ((~mask) & 0x0F);
    APPLE_STEPPER_PORT->BSRR = (clr_mask << 16U) | set_mask;
}

void fdd_motion_init(uint8_t max_cylinders, fdd_step_rate_t default_rate) {
    s_state.current_cylinder    = 0;
    s_state.max_cylinders       = (max_cylinders > 0) ? max_cylinders : 80;
    s_state.step_rate_ms        = default_rate;
    s_state.step_pulse_width_us = 6;      /* 6 us standard pulse */
    s_state.head_settle_time_ms = 15;     /* 15 ms settling time */
    s_state.mode                = MOTION_MODE_STANDARD_BUS;
    s_state.is_homed            = false;
    s_state.is_moving           = false;
    s_state.phase_index_4phase  = 0;

    apply_4phase_output(0x00);
}

void fdd_motion_set_step_rate(fdd_step_rate_t rate_ms) {
    s_state.step_rate_ms = rate_ms;
}

void fdd_motion_set_mode(fdd_motion_mode_t mode) {
    s_state.mode = mode;
    if (mode == MOTION_MODE_STANDARD_BUS) {
        apply_4phase_output(0x00);
    }
}

void fdd_motion_set_max_cylinders(uint8_t max_cyl) {
    s_state.max_cylinders = max_cyl;
}

bool fdd_motion_step(bool inward) {
    bsp_led_busy(true);

    if (s_state.mode == MOTION_MODE_STANDARD_BUS) {
        /*
         * Standard Shugart / PC Bus Stepping Protocol
         * 1. Set DIR line
         * 2. Wait Direction Setup Time (minimum 1 us)
         * 3. Pulse STEP line LOW
         * 4. Wait Step Rate interval
         */
        bsp_fdd_set_direction(inward);
        HAL_Delay(1); /* 1 ms setup delay ensures margins on all vintage electronics */

        bsp_fdd_pulse_step(s_state.step_pulse_width_us);

        if (s_state.step_rate_ms > 1) {
            HAL_Delay(s_state.step_rate_ms - 1);
        }

        if (inward) {
            if (s_state.current_cylinder < (s_state.max_cylinders - 1)) {
                s_state.current_cylinder++;
            }
        } else {
            if (s_state.current_cylinder > 0) {
                s_state.current_cylinder--;
            }
            /* Verify Track 0 sensor */
            if (bsp_fdd_is_track00()) {
                s_state.current_cylinder = 0;
                s_state.is_homed = true;
            }
        }
    } else {
        /* Direct 4-phase Stepper Driving */
        if (s_state.mode == MOTION_MODE_4PHASE_FULL) {
            if (inward) {
                s_state.phase_index_4phase = (s_state.phase_index_4phase + 1) & 0x03;
            } else {
                s_state.phase_index_4phase = (s_state.phase_index_4phase + 3) & 0x03;
            }
            apply_4phase_output(s_full_step_table[s_state.phase_index_4phase]);
        } else if (s_state.mode == MOTION_MODE_4PHASE_HALF) {
            if (inward) {
                s_state.phase_index_4phase = (s_state.phase_index_4phase + 1) & 0x07;
            } else {
                s_state.phase_index_4phase = (s_state.phase_index_4phase + 7) & 0x07;
            }
            apply_4phase_output(s_half_step_table[s_state.phase_index_4phase]);
        } else if (s_state.mode == MOTION_MODE_4PHASE_WAVE) {
            if (inward) {
                s_state.phase_index_4phase = (s_state.phase_index_4phase + 1) & 0x03;
            } else {
                s_state.phase_index_4phase = (s_state.phase_index_4phase + 3) & 0x03;
            }
            apply_4phase_output(s_wave_step_table[s_state.phase_index_4phase]);
        }

        HAL_Delay(s_state.step_rate_ms);

        if (inward) {
            if (s_state.current_cylinder < (s_state.max_cylinders - 1)) {
                s_state.current_cylinder++;
            }
        } else {
            if (s_state.current_cylinder > 0) {
                s_state.current_cylinder--;
            }
        }
    }

    bsp_led_busy(false);
    return true;
}

bool fdd_motion_step_multiple(bool inward, uint8_t count) {
    s_state.is_moving = true;
    for (uint8_t i = 0; i < count; i++) {
        fdd_motion_step(inward);
        /* If moving outward and Track 00 sensor triggers, stop */
        if (!inward && bsp_fdd_is_track00()) {
            s_state.current_cylinder = 0;
            s_state.is_homed = true;
            break;
        }
    }
    s_state.is_moving = false;

    /* Head settling time */
    HAL_Delay(s_state.head_settle_time_ms);
    return true;
}

bool fdd_motion_home(void) {
    s_state.is_moving = true;
    bsp_led_busy(true);

    /*
     * Homing Strategy:
     * If already at Track 00, step in 3 tracks then recalibrate out
     */
    if (bsp_fdd_is_track00()) {
        fdd_motion_step_multiple(true, 3);
    }

    /* Maximum outward seek attempts = max_cylinders + 10 margin */
    uint8_t max_attempts = s_state.max_cylinders + 10;
    bool found_track0 = false;

    for (uint8_t i = 0; i < max_attempts; i++) {
        fdd_motion_step(false); /* Step Outward */

        if (bsp_fdd_is_track00()) {
            found_track0 = true;
            s_state.current_cylinder = 0;
            s_state.is_homed = true;
            break;
        }
    }

    /* Settling delay */
    HAL_Delay(s_state.head_settle_time_ms);

    s_state.is_moving = false;
    bsp_led_busy(false);

    if (found_track0) {
        bsp_led_ready(true);
        return true;
    } else {
        bsp_led_fault(true);
        return false;
    }
}

bool fdd_motion_seek(uint8_t target_cylinder) {
    if (target_cylinder >= s_state.max_cylinders) {
        target_cylinder = s_state.max_cylinders - 1;
    }

    if (s_state.current_cylinder == target_cylinder) {
        return true;
    }

    s_state.is_moving = true;

    if (target_cylinder > s_state.current_cylinder) {
        uint8_t steps = target_cylinder - s_state.current_cylinder;
        fdd_motion_step_multiple(true, steps);
    } else {
        uint8_t steps = s_state.current_cylinder - target_cylinder;
        fdd_motion_step_multiple(false, steps);
    }

    s_state.is_moving = false;
    return true;
}

bool fdd_motion_cycle_alignment(uint8_t center_cylinder) {
    /*
     * Vintage Exerciser Alignment Cycle (TEACO / Dysan):
     * Rapid cycling between Track 00, Center Track, and Inner Track
     */
    fdd_motion_home();
    fdd_motion_seek(center_cylinder);
    fdd_motion_seek(s_state.max_cylinders - 1);
    fdd_motion_seek(center_cylinder);
    return true;
}

bool fdd_motion_run_exercise(uint8_t start_cyl, uint8_t end_cyl, uint16_t cycles, bool (*abort_check)(void)) {
    if (end_cyl >= s_state.max_cylinders) {
        end_cyl = s_state.max_cylinders - 1;
    }

    for (uint16_t c = 0; c < cycles; c++) {
        if (abort_check && abort_check()) {
            break;
        }

        fdd_motion_seek(start_cyl);

        if (abort_check && abort_check()) {
            break;
        }

        fdd_motion_seek(end_cyl);
    }

    return true;
}

const fdd_motion_state_t *fdd_motion_get_state(void) {
    return &s_state;
}
