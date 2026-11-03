/**
 * @file    fdd_motion.h
 * @brief   Floppy Disk Stepper Motion & Seek Engine Specification
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 */

#ifndef FDD_MOTION_H
#define FDD_MOTION_H

#include "bsp_fdd_pins.h"

#ifdef __cplusplus
extern "C" {
#endif

/* Step Rate Presets (Millisecond Period) */
typedef enum {
    STEP_RATE_2MS  = 2,
    STEP_RATE_3MS  = 3,     /**< Standard 3.5" HD (1.44MB) & Fast 5.25" */
    STEP_RATE_4MS  = 4,
    STEP_RATE_6MS  = 6,     /**< Standard 5.25" PC/AT (360KB / 1.2MB) */
    STEP_RATE_8MS  = 8,     /**< Standard 8" Shugart SA800 */
    STEP_RATE_10MS = 10,
    STEP_RATE_12MS = 12,    /**< Shugart SA400 / Slow Mini-Floppy */
    STEP_RATE_20MS = 20,    /**< High inertia stepper / alignment */
    STEP_RATE_30MS = 30     /**< Slowest vintage 35-track drive */
} fdd_step_rate_t;

/* Stepper Driving Mode */
typedef enum {
    MOTION_MODE_STANDARD_BUS = 0,   /**< Driven via STEP / DIR pins through 7406 */
    MOTION_MODE_4PHASE_FULL,        /**< Direct 4-phase stepper (PE0..PE3) Full Step */
    MOTION_MODE_4PHASE_HALF,        /**< Direct 4-phase stepper Half Step (Apple II 0.5 track) */
    MOTION_MODE_4PHASE_WAVE         /**< Direct 4-phase stepper Wave Drive */
} fdd_motion_mode_t;

/* Motion Engine State */
typedef struct {
    uint8_t             current_cylinder;       /**< Estimated cylinder position (0..79/82) */
    uint8_t             max_cylinders;          /**< Maximum drive cylinder limit (40, 77, 80) */
    fdd_step_rate_t     step_rate_ms;           /**< Current step period in ms */
    uint16_t            step_pulse_width_us;    /**< Step pulse active width (typically 4-8 us) */
    uint16_t            head_settle_time_ms;    /**< Settling delay after seek (10-20 ms) */
    fdd_motion_mode_t   mode;                   /**< Stepper driving method */
    bool                is_homed;               /**< True if Track 0 has been confirmed */
    bool                is_moving;              /**< True during seek execution */
    uint8_t             phase_index_4phase;     /**< 4-phase stepper rotor step state */
} fdd_motion_state_t;

/* Initialization */
void fdd_motion_init(uint8_t max_cylinders, fdd_step_rate_t default_rate);

/* Configuration */
void fdd_motion_set_step_rate(fdd_step_rate_t rate_ms);
void fdd_motion_set_mode(fdd_motion_mode_t mode);
void fdd_motion_set_max_cylinders(uint8_t max_cyl);

/* Elementary Step Operations */
bool fdd_motion_step(bool inward);
bool fdd_motion_step_multiple(bool inward, uint8_t count);

/* High-Level Positioning Routines */
bool fdd_motion_home(void);
bool fdd_motion_seek(uint8_t target_cylinder);
bool fdd_motion_cycle_alignment(uint8_t center_cylinder);

/* Continuous Exercise / Burn-in Test (Non-blocking or pollable) */
bool fdd_motion_run_exercise(uint8_t start_cyl, uint8_t end_cyl, uint16_t cycles, bool (*abort_check)(void));

/* Status Query */
const fdd_motion_state_t *fdd_motion_get_state(void);

#ifdef __cplusplus
}
#endif

#endif /* FDD_MOTION_H */
