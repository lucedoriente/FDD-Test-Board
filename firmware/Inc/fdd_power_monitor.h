/**
 * @file    fdd_power_monitor.h
 * @brief   Zero-Smoke Active E-Fuse & Power Monitoring Subsystem
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 */

#ifndef FDD_POWER_MONITOR_H
#define FDD_POWER_MONITOR_H

#include "bsp_fdd_pins.h"

#ifdef __cplusplus
extern "C" {
#endif

/* Power Rail Identifiers */
typedef enum {
    PWR_RAIL_24V = 0,
    PWR_RAIL_12V,
    PWR_RAIL_5V,
    PWR_RAIL_COUNT
} fdd_pwr_rail_t;

/* Telemetry Data Structure */
typedef struct {
    float    voltage_v[PWR_RAIL_COUNT];     /**< Estimated / Nominal Rail Voltage */
    float    current_ma[PWR_RAIL_COUNT];    /**< Instantaneous Measured Current in mA */
    float    peak_current_ma[PWR_RAIL_COUNT]; /**< Peak recorded current */
    float    limit_ma[PWR_RAIL_COUNT];      /**< Overcurrent Trip Limit in mA */
    bool     rail_enabled[PWR_RAIL_COUNT];  /**< Rail switch state */
    bool     fault_tripped[PWR_RAIL_COUNT]; /**< Trip flag */
    uint32_t trip_timestamp_ms[PWR_RAIL_COUNT];
} fdd_power_telemetry_t;

/* Initialization */
void fdd_power_monitor_init(void);

/* Rail Control with Soft-Start Inrush Blanking */
bool fdd_power_enable_rail(fdd_pwr_rail_t rail, bool enable);
void fdd_power_enable_all(bool enable);

/* Trip Limits Configuration */
void fdd_power_set_trip_limit(fdd_pwr_rail_t rail, float limit_ma);

/* Real-Time Processing (Called periodically from Timer / SysTick / Main Loop) */
void fdd_power_update_adc_raw(uint16_t adc_24v, uint16_t adc_12v, uint16_t adc_5v);
bool fdd_power_check_faults(void);

/* Telemetry Query */
const fdd_power_telemetry_t *fdd_power_get_telemetry(void);
void fdd_power_clear_faults(void);

#ifdef __cplusplus
}
#endif

#endif /* FDD_POWER_MONITOR_H */
