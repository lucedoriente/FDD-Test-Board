/**
 * @file    fdd_timing_capture.h
 * @brief   Floppy Drive High-Precision Spindle Tachometer & Index Profiler
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 */

#ifndef FDD_TIMING_CAPTURE_H
#define FDD_TIMING_CAPTURE_H

#include "bsp_fdd_pins.h"

#ifdef __cplusplus
extern "C" {
#endif

/* Nominal Floppy Drive Rotation Speeds */
typedef enum {
    SPINDLE_NOMINAL_300_RPM = 0,   /**< 3.5" (DD/HD) & 5.25" DD (300 RPM / 200.00 ms period) */
    SPINDLE_NOMINAL_360_RPM,       /**< 5.25" HD & 8" Shugart (360 RPM / 166.67 ms period) */
    SPINDLE_NOMINAL_CUSTOM
} fdd_spindle_speed_type_t;

/* Real-Time Tachometer Telemetry */
typedef struct {
    float    current_rpm;           /**< Instantaneous RPM of most recent revolution */
    float    average_rpm;           /**< Mean RPM calculated over sample window */
    float    min_rpm;               /**< Minimum recorded RPM */
    float    max_rpm;               /**< Maximum recorded RPM */
    uint32_t current_period_us;     /**< Revolution period in microseconds */
    uint32_t pulse_width_us;        /**< Index pulse active duration in microseconds */
    float    wow_flutter_percent;   /**< Speed variation / wow-and-flutter percentage */
    uint32_t total_index_pulses;    /**< Cumulative revolutions counted */
    bool     spindle_spinning;      /**< True if index pulses are arriving regularly */
    bool     speed_in_spec;         /**< True if RPM is within +/- 1.0% tolerance */
} fdd_tachometer_data_t;

/* Initialization */
void fdd_timing_capture_init(void);

/* Processing Hooks (Called from Timer Input Capture ISR or polling simulator) */
void fdd_timing_on_index_edge(uint32_t timer_timestamp_us, bool rising);

/* Periodic Engine Update (Called from SysTick / Main Loop at ~100 Hz) */
void fdd_timing_update(void);

/* Diagnostic Measurements */
void fdd_timing_reset_stats(void);
const fdd_tachometer_data_t *fdd_timing_get_data(void);
bool fdd_timing_evaluate_speed(fdd_spindle_speed_type_t nominal_type, float tolerance_percent);

#ifdef __cplusplus
}
#endif

#endif /* FDD_TIMING_CAPTURE_H */
