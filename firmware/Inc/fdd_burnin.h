/**
 * @file    fdd_burnin.h
 * @brief   Endurance Burn-In & Long-Term Stress Testing Engine for Floppy Drives
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 */

#ifndef FDD_BURNIN_H
#define FDD_BURNIN_H

#include <stdint.h>
#include <stdbool.h>
#include "fdd_diagnostics.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    uint32_t        target_cycles;             /**< Target full sweep cycles (e.g. 500 or 1000) */
    uint8_t         start_track;               /**< Outer track (usually 0) */
    uint8_t         end_track;                 /**< Inner track (e.g. 39, 76, 79) */
    fdd_step_rate_t step_rate;                 /**< Step pulse rate in ms */
    uint16_t        homing_check_interval;     /**< Check Track 00 homing every N cycles */
    float           max_allowed_current_ma;    /**< Thermal shutdown current limit */
} fdd_burnin_config_t;

typedef struct {
    bool            is_running;                /**< Burn-in test active */
    uint32_t        completed_cycles;          /**< Number of full sweeps executed */
    uint32_t        elapsed_seconds;           /**< Total elapsed test time */
    uint16_t        total_step_loss_events;    /**< Count of detected step loss errors */
    float           baseline_12v_current_ma;   /**< Cold baseline current draw */
    float           current_12v_current_ma;    /**< Live measured current draw */
    float           current_drift_percent;     /**< Thermal / friction current drift % */
    bool            aborted_due_to_friction;   /**< Tripped due to bearing heat/friction */
    bool            aborted_due_to_user;       /**< Aborted by operator pressing BACK */
} fdd_burnin_status_t;

/**
 * @brief Starts endurance burn-in test session
 */
void fdd_burnin_start(const fdd_burnin_config_t *cfg);

/**
 * @brief Advances burn-in state machine (non-blocking, called periodically)
 * @return true if burn-in is still in progress, false if completed or aborted
 */
bool fdd_burnin_update(void);

/**
 * @brief Aborts current burn-in test safely
 */
void fdd_burnin_stop(void);

/**
 * @brief Retrieves live burn-in metrics
 */
const fdd_burnin_status_t *fdd_burnin_get_status(void);

#ifdef __cplusplus
}
#endif

#endif /* FDD_BURNIN_H */
