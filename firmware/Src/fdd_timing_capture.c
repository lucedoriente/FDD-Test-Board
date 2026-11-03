/**
 * @file    fdd_timing_capture.c
 * @brief   Floppy Drive High-Precision Spindle Tachometer Implementation
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 */

#include "fdd_timing_capture.h"
#include "bsp_fdd_gpio.h"

#define RPM_WINDOW_SIZE         16U
#define SPINDLE_TIMEOUT_US      1000000UL   /**< 1 second without index pulse = stopped */

static fdd_tachometer_data_t s_tacho;
static uint32_t s_last_rising_us = 0;
static uint32_t s_period_history[RPM_WINDOW_SIZE];
static uint8_t  s_history_index = 0;
static uint8_t  s_history_count = 0;
static uint32_t s_last_pulse_tick_ms = 0;

extern uint32_t hal_get_tick_ms(void);

void fdd_timing_capture_init(void) {
    s_tacho.current_rpm         = 0.0f;
    s_tacho.average_rpm         = 0.0f;
    s_tacho.min_rpm             = 9999.0f;
    s_tacho.max_rpm             = 0.0f;
    s_tacho.current_period_us   = 0;
    s_tacho.pulse_width_us      = 0;
    s_tacho.wow_flutter_percent = 0.0f;
    s_tacho.total_index_pulses  = 0;
    s_tacho.spindle_spinning    = false;
    s_tacho.speed_in_spec       = false;

    s_last_rising_us = 0;
    s_history_index  = 0;
    s_history_count  = 0;
    s_last_pulse_tick_ms = 0;
}

void fdd_timing_on_index_edge(uint32_t timer_timestamp_us, bool rising) {
    if (rising) {
        /* Rising Edge = Start of Index Pulse */
        bsp_led_index(true);

        if (s_last_rising_us != 0) {
            uint32_t period_us;
            if (timer_timestamp_us >= s_last_rising_us) {
                period_us = timer_timestamp_us - s_last_rising_us;
            } else {
                /* Timer counter rollover (32-bit arithmetic handles this naturally) */
                period_us = (0xFFFFFFFFUL - s_last_rising_us) + timer_timestamp_us + 1;
            }

            /* Basic sanity check: Floppy period is between 100 ms (600 RPM) and 500 ms (120 RPM) */
            if (period_us > 100000UL && period_us < 600000UL) {
                s_tacho.current_period_us = period_us;
                s_tacho.current_rpm = 60000000.0f / (float)period_us;
                s_tacho.total_index_pulses++;
                s_tacho.spindle_spinning = true;

                /* Store into ring buffer for statistics */
                s_period_history[s_history_index] = period_us;
                s_history_index = (s_history_index + 1) % RPM_WINDOW_SIZE;
                if (s_history_count < RPM_WINDOW_SIZE) {
                    s_history_count++;
                }

                /* Calculate Window Statistics */
                uint32_t sum = 0;
                uint32_t min_p = 0xFFFFFFFFUL;
                uint32_t max_p = 0;

                for (uint8_t i = 0; i < s_history_count; i++) {
                    uint32_t p = s_period_history[i];
                    sum += p;
                    if (p < min_p) min_p = p;
                    if (p > max_p) max_p = p;
                }

                uint32_t mean_p = sum / s_history_count;
                s_tacho.average_rpm = 60000000.0f / (float)mean_p;

                float rpm_from_min_p = 60000000.0f / (float)max_p;
                float rpm_from_max_p = 60000000.0f / (float)min_p;

                if (rpm_from_min_p < s_tacho.min_rpm) s_tacho.min_rpm = rpm_from_min_p;
                if (rpm_from_max_p > s_tacho.max_rpm) s_tacho.max_rpm = rpm_from_max_p;

                /* Wow and Flutter = (Max_Period - Min_Period) / Mean_Period * 100% */
                if (mean_p > 0) {
                    s_tacho.wow_flutter_percent = ((float)(max_p - min_p) / (float)mean_p) * 100.0f;
                }
            }
        }

        s_last_rising_us = timer_timestamp_us;
        s_last_pulse_tick_ms = hal_get_tick_ms();
    } else {
        /* Falling Edge = End of Index Pulse */
        bsp_led_index(false);
        if (s_last_rising_us != 0 && timer_timestamp_us >= s_last_rising_us) {
            s_tacho.pulse_width_us = timer_timestamp_us - s_last_rising_us;
        }
    }
}

void fdd_timing_update(void) {
    uint32_t now_ms = hal_get_tick_ms();

    /* Check Spindle Timeout */
    if (s_tacho.spindle_spinning) {
        if ((now_ms - s_last_pulse_tick_ms) > (SPINDLE_TIMEOUT_US / 1000U)) {
            s_tacho.spindle_spinning = false;
            s_tacho.current_rpm = 0.0f;
            bsp_led_index(false);
        }
    }
}

void fdd_timing_reset_stats(void) {
    s_tacho.min_rpm             = 9999.0f;
    s_tacho.max_rpm             = 0.0f;
    s_tacho.wow_flutter_percent = 0.0f;
    s_tacho.total_index_pulses  = 0;
    s_history_index             = 0;
    s_history_count             = 0;
}

const fdd_tachometer_data_t *fdd_timing_get_data(void) {
    return &s_tacho;
}

bool fdd_timing_evaluate_speed(fdd_spindle_speed_type_t nominal_type, float tolerance_percent) {
    float target_rpm = 300.0f;

    if (nominal_type == SPINDLE_NOMINAL_360_RPM) {
        target_rpm = 360.0f;
    }

    if (!s_tacho.spindle_spinning || s_history_count < 4) {
        s_tacho.speed_in_spec = false;
        return false;
    }

    float delta = s_tacho.average_rpm - target_rpm;
    if (delta < 0.0f) delta = -delta;

    float allowed_delta = target_rpm * (tolerance_percent / 100.0f);
    s_tacho.speed_in_spec = (delta <= allowed_delta);

    return s_tacho.speed_in_spec;
}
