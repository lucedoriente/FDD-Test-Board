/**
 * @file    ui_panel.h
 * @brief   Retro-Diag FDD Master Tester Front Panel UI State Machine & Controller
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 */

#ifndef UI_PANEL_H
#define UI_PANEL_H

#include <stdint.h>
#include <stdbool.h>
#include "fdd_diagnostics.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
    UI_STATE_BOOT = 0,
    UI_STATE_MODEL_SELECT,
    UI_STATE_LIVE_TACHOMETER,
    UI_STATE_STEPPER_SEEK,
    UI_STATE_CAT_EYE_ALIGN,
    UI_STATE_DIAG_PROGRESS,
    UI_STATE_DIAG_REPORT,
    UI_STATE_REPAIR_ADVISOR,
    UI_STATE_ERROR_ALERT
} ui_state_t;

/**
 * @brief Initializes display, encoders, buttons, and state machine
 */
void ui_panel_init(void);

/**
 * @brief Periodic UI update (called in superloop at ~30-60 Hz)
 * @param delta_ms Elapsed time in milliseconds since last call
 */
void ui_panel_update(uint32_t delta_ms);

/**
 * @brief Triggers an emergency error popup on display
 * @param title Error title
 * @param msg Error explanation
 */
void ui_panel_trigger_error(const char *title, const char *msg);

/**
 * @brief Gets current UI state
 */
ui_state_t ui_panel_get_state(void);

#ifdef __cplusplus
}
#endif

#endif /* UI_PANEL_H */
