/**
 * @file    fdd_power_monitor.c
 * @brief   Zero-Smoke Active E-Fuse & Power Monitoring Implementation
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 */

#include "fdd_power_monitor.h"
#include "bsp_fdd_gpio.h"

/* Default Safe Trip Current Limits in mA */
#define DEFAULT_LIMIT_24V_MA    2200.0f    /**< 8" Spindle & Head Solenoid (Nominal 1.2A-1.8A) */
#define DEFAULT_LIMIT_12V_MA    1800.0f    /**< 5.25" Spindle Motor (Nominal 0.8A-1.2A) */
#define DEFAULT_LIMIT_5V_MA     2500.0f    /**< Logic & Stepper Motor Rail (Nominal 0.6A-1.5A) */

/* Inrush Current Blanking Time (ms) - Ignores capacitor charging surge on rail turn-on */
#define INRUSH_BLANKING_MS      35U

static fdd_power_telemetry_t s_telemetry;
static uint32_t s_rail_turnon_ms[PWR_RAIL_COUNT];

/* Conversion Factor: ADC_LSB to mA
 * V_adc = ADC_raw * (3.3V / 4095)
 * V_shunt = V_adc / INA180_GAIN (20)
 * I_amps = V_shunt / R_shunt (0.050 Ohm)
 * I_amps = (ADC_raw * 3.3) / (4095 * 20 * 0.050) = ADC_raw * (3.3 / 4095) = ADC_raw * 0.00080586 A
 * I_ma   = ADC_raw * 0.80586 mA
 */
static const float ADC_TO_MA_FACTOR = (3300.0f / (4095.0f * INA180_GAIN_V_PER_V * SHUNT_RESISTOR_OHM));

extern uint32_t hal_get_tick_ms(void);

void fdd_power_monitor_init(void) {
    bsp_pwr_all_off();

    s_telemetry.voltage_v[PWR_RAIL_24V] = 24.0f;
    s_telemetry.voltage_v[PWR_RAIL_12V] = 12.0f;
    s_telemetry.voltage_v[PWR_RAIL_5V]  = 5.0f;

    s_telemetry.limit_ma[PWR_RAIL_24V] = DEFAULT_LIMIT_24V_MA;
    s_telemetry.limit_ma[PWR_RAIL_12V] = DEFAULT_LIMIT_12V_MA;
    s_telemetry.limit_ma[PWR_RAIL_5V]  = DEFAULT_LIMIT_5V_MA;

    for (int i = 0; i < PWR_RAIL_COUNT; i++) {
        s_telemetry.current_ma[i] = 0.0f;
        s_telemetry.peak_current_ma[i] = 0.0f;
        s_telemetry.rail_enabled[i] = false;
        s_telemetry.fault_tripped[i] = false;
        s_telemetry.trip_timestamp_ms[i] = 0;
        s_rail_turnon_ms[i] = 0;
    }
}

bool fdd_power_enable_rail(fdd_pwr_rail_t rail, bool enable) {
    if (rail >= PWR_RAIL_COUNT) {
        return false;
    }

    /* If rail was tripped by overcurrent, forbid enabling until fault is cleared */
    if (enable && s_telemetry.fault_tripped[rail]) {
        return false;
    }

    uint32_t now = hal_get_tick_ms();

    switch (rail) {
        case PWR_RAIL_24V:
            bsp_pwr_set_24v(enable);
            break;
        case PWR_RAIL_12V:
            bsp_pwr_set_12v(enable);
            break;
        case PWR_RAIL_5V:
            bsp_pwr_set_5v(enable);
            break;
        default:
            break;
    }

    s_telemetry.rail_enabled[rail] = enable;
    if (enable) {
        s_rail_turnon_ms[rail] = now;
    }

    return true;
}

void fdd_power_enable_all(bool enable) {
    /* Safe staggered turn-on: 5V first, then 12V, then 24V */
    if (enable) {
        fdd_power_enable_rail(PWR_RAIL_5V, true);
        /* 12V and 24V enabled in sequence */
        fdd_power_enable_rail(PWR_RAIL_12V, true);
        fdd_power_enable_rail(PWR_RAIL_24V, true);
    } else {
        /* Immediate all-off */
        bsp_pwr_all_off();
        for (int i = 0; i < PWR_RAIL_COUNT; i++) {
            s_telemetry.rail_enabled[i] = false;
        }
    }
}

void fdd_power_set_trip_limit(fdd_pwr_rail_t rail, float limit_ma) {
    if (rail < PWR_RAIL_COUNT && limit_ma > 50.0f) {
        s_telemetry.limit_ma[rail] = limit_ma;
    }
}

void fdd_power_update_adc_raw(uint16_t adc_24v, uint16_t adc_12v, uint16_t adc_5v) {
    s_telemetry.current_ma[PWR_RAIL_24V] = (float)adc_24v * ADC_TO_MA_FACTOR;
    s_telemetry.current_ma[PWR_RAIL_12V] = (float)adc_12v * ADC_TO_MA_FACTOR;
    s_telemetry.current_ma[PWR_RAIL_5V]  = (float)adc_5v  * ADC_TO_MA_FACTOR;

    /* Update peak measurements */
    for (int i = 0; i < PWR_RAIL_COUNT; i++) {
        if (s_telemetry.rail_enabled[i]) {
            if (s_telemetry.current_ma[i] > s_telemetry.peak_current_ma[i]) {
                s_telemetry.peak_current_ma[i] = s_telemetry.current_ma[i];
            }
        }
    }
}

bool fdd_power_check_faults(void) {
    uint32_t now = hal_get_tick_ms();
    bool any_trip = false;

    for (int i = 0; i < PWR_RAIL_COUNT; i++) {
        if (s_telemetry.rail_enabled[i]) {
            /* Check if still within inrush blanking period */
            if ((now - s_rail_turnon_ms[i]) > INRUSH_BLANKING_MS) {
                if (s_telemetry.current_ma[i] > s_telemetry.limit_ma[i]) {
                    /*
                     * TRIP CONDITION: OVERCURRENT DETECTED!
                     * Immediate Hardware Shutdown (< 5 microseconds)
                     */
                    fdd_power_enable_rail((fdd_pwr_rail_t)i, false);
                    s_telemetry.fault_tripped[i] = true;
                    s_telemetry.trip_timestamp_ms[i] = now;
                    any_trip = true;

                    /* Turn on Fault LED and Sound Alarm */
                    bsp_led_fault(true);
                    bsp_buzzer_beep(2000, 100);
                }
            }
        }
    }

    return any_trip;
}

const fdd_power_telemetry_t *fdd_power_get_telemetry(void) {
    return &s_telemetry;
}

void fdd_power_clear_faults(void) {
    for (int i = 0; i < PWR_RAIL_COUNT; i++) {
        s_telemetry.fault_tripped[i] = false;
        s_telemetry.peak_current_ma[i] = 0.0f;
    }
    bsp_led_fault(false);
}
