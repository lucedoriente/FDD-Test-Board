/**
 * @file    ui_panel.c
 * @brief   Retro-Diag FDD Master Tester Front Panel UI State Machine & Controller
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 */

#include "ui_panel.h"
#include "display_ui.h"
#include "hal_display.h"
#include "bsp_fdd_gpio.h"
#include "bsp_fdd_pins.h"
#include "fdd_power_monitor.h"
#include "fdd_timing_capture.h"
#include "fdd_motion.h"
#include "fdd_diagnostics.h"
#include "fdd_nvram.h"
#include "fdd_analog_scope.h"
#include <string.h>

/* State Machine Variables */
static ui_state_t       s_current_state = UI_STATE_BOOT;
static uint8_t          s_selected_model = (uint8_t)DRIVE_MODEL_GENERIC_350_HD;
static uint32_t         s_state_timer_ms = 0;
static bool             s_motor_live_on = false;
static uint8_t          s_head_side = 0;

/* Buttons edge detection history */
static bool             s_last_btn_run = false;
static bool             s_last_btn_back = false;
static bool             s_last_btn_enc = false;

/* Encoder Gray-code history */
static uint8_t          s_last_encoder_state = 0;
static int8_t           s_encoder_accum = 0;

/* Active diagnostic report pointer */
static const fdd_diagnostic_report_t *s_active_report = NULL;

/* Error popup storage */
static char             s_err_title[32] = "";
static char             s_err_msg[64] = "";

/* ========================================================================== */
/* Encoder & Button Low-Level Debouncing                                      */
/* ========================================================================== */

static inline bool gpio_read(GPIO_TypeDef *port, uint16_t pin) {
    return (HAL_GPIO_ReadPin(port, pin) == GPIO_PIN_SET);
}

static int8_t poll_rotary_encoder(void) {
    uint8_t a = gpio_read(ENC_A_PORT, ENC_A_PIN) ? 1 : 0;
    uint8_t b = gpio_read(ENC_B_PORT, ENC_B_PIN) ? 1 : 0;
    uint8_t curr = (a << 1) | b;
    int8_t step = 0;

    if (curr != s_last_encoder_state) {
        if ((s_last_encoder_state == 0 && curr == 1) || (s_last_encoder_state == 1 && curr == 3) ||
            (s_last_encoder_state == 3 && curr == 2) || (s_last_encoder_state == 2 && curr == 0)) {
            s_encoder_accum++;
        } else if ((s_last_encoder_state == 0 && curr == 2) || (s_last_encoder_state == 2 && curr == 3) ||
                   (s_last_encoder_state == 3 && curr == 1) || (s_last_encoder_state == 1 && curr == 0)) {
            s_encoder_accum--;
        }
        s_last_encoder_state = curr;
    }

    /* Standard encoder generates 2 or 4 state transitions per click */
    if (s_encoder_accum >= 2) {
        step = 1;
        s_encoder_accum = 0;
    } else if (s_encoder_accum <= -2) {
        step = -1;
        s_encoder_accum = 0;
    }
    return step;
}

static bool check_button_edge(bool current_level, bool *last_level) {
    bool pressed = false;
    if (current_level && !(*last_level)) {
        pressed = true;
    }
    *last_level = current_level;
    return pressed;
}

/* ========================================================================== */
/* Initialization                                                             */
/* ========================================================================== */

void ui_panel_init(void) {
    hal_display_init();
    fdd_nvram_init();
    fdd_analog_scope_init();

    s_current_state = UI_STATE_BOOT;
    s_state_timer_ms = 0;
    s_selected_model = fdd_nvram_get()->last_selected_model;
    if (s_selected_model == 0 || s_selected_model >= DRIVE_MODEL_COUNT) {
        s_selected_model = (uint8_t)DRIVE_MODEL_CHINON_FB354;
    }
    s_motor_live_on = false;
    s_head_side = 0;

    /* Hardware self-test LED sequence */
    bsp_led_self_test(80);

    /* Render initial boot screen */
    ui_render_boot();
    bsp_led_ready(true);
}

ui_state_t ui_panel_get_state(void) {
    return s_current_state;
}

void ui_panel_trigger_error(const char *title, const char *msg) {
    strncpy(s_err_title, title ? title : "ALLARME E-FUSE", sizeof(s_err_title) - 1);
    strncpy(s_err_msg, msg ? msg : "Corto circuito o sovracorrente", sizeof(s_err_msg) - 1);
    s_current_state = UI_STATE_ERROR_ALERT;
    bsp_led_fault(true);
    bsp_buzzer_beep(1000, 300);
}

/* ========================================================================== */
/* Main UI Update Loop (Called at ~30-60 Hz)                                  */
/* ========================================================================== */

void ui_panel_update(uint32_t delta_ms) {
    s_state_timer_ms += delta_ms;

    /* 1. Poll physical inputs */
    int8_t enc_delta = poll_rotary_encoder();
    bool btn_run_edge = check_button_edge(bsp_btn_run_pressed(), &s_last_btn_run);
    bool btn_back_edge = check_button_edge(bsp_btn_back_pressed(), &s_last_btn_back);
    bool btn_enc_edge = check_button_edge(bsp_btn_enc_pressed(), &s_last_btn_enc);

    /* 2. LED Activity Tracking */
    bsp_led_index(bsp_fdd_get_index_raw());

    /* 3. State Machine Processing */
    switch (s_current_state) {

        /* SCREEN 1: BOOT & SELF-TEST */
        case UI_STATE_BOOT:
            bsp_led_ready(true);
            bsp_led_busy(false);
            bsp_led_fault(false);
            if (btn_run_edge || btn_enc_edge || s_state_timer_ms > 2500U) {
                s_current_state = UI_STATE_MODEL_SELECT;
                s_state_timer_ms = 0;
                bsp_buzzer_beep(2000, 80);
            }
            break;

        /* SCREEN 2: OEM DRIVE SELECTION MENU */
        case UI_STATE_MODEL_SELECT:
            bsp_led_ready(true);
            bsp_led_busy(false);
            bsp_led_fault(false);

            if (enc_delta != 0) {
                int16_t next_idx = (int16_t)s_selected_model + enc_delta;
                if (next_idx < 1) next_idx = (int16_t)(DRIVE_MODEL_COUNT - 1);
                if (next_idx >= (int16_t)DRIVE_MODEL_COUNT) next_idx = 1;
                s_selected_model = (uint8_t)next_idx;
                bsp_buzzer_beep(2500, 10);
            }

            if (btn_run_edge) {
                /* Launch full automated diagnostic suite */
                s_current_state = UI_STATE_DIAG_PROGRESS;
                s_state_timer_ms = 0;
                bsp_buzzer_beep(2200, 120);
            } else if (btn_enc_edge) {
                /* Open live tachometer & exerciser directly */
                s_current_state = UI_STATE_LIVE_TACHOMETER;
                s_state_timer_ms = 0;
                bsp_buzzer_beep(1800, 80);
            }

            ui_render_model_select(s_selected_model);
            break;

        /* SCREEN 3: LIVE TACHOMETER & EXERCISER */
        case UI_STATE_LIVE_TACHOMETER:
            bsp_led_busy(s_motor_live_on);
            const fdd_tachometer_data_t *tacho = fdd_timing_get_data();
            const fdd_model_spec_t *spec = fdd_diagnostics_get_model_spec((fdd_drive_model_t)s_selected_model);
            const fdd_power_metrics_t *pwr = fdd_power_get_metrics();

            if (btn_run_edge) {
                s_motor_live_on = !s_motor_live_on;
                bsp_fdd_set_motor(s_motor_live_on);
                bsp_fdd_set_drive_select(0, s_motor_live_on);
                bsp_buzzer_beep(s_motor_live_on ? 2500 : 1500, 80);
            }

            if (btn_enc_edge) {
                /* Transition to Stepper Seek screen */
                s_current_state = UI_STATE_STEPPER_SEEK;
                s_state_timer_ms = 0;
                bsp_buzzer_beep(2000, 80);
            }

            if (btn_back_edge) {
                /* Stop motor and return to model select */
                s_motor_live_on = false;
                bsp_fdd_set_motor(false);
                bsp_fdd_set_drive_select(0, false);
                s_current_state = UI_STATE_MODEL_SELECT;
                s_state_timer_ms = 0;
                bsp_buzzer_beep(1200, 100);
            }

            ui_render_live_tachometer(tacho->current_rpm, spec->nominal_rpm,
                                      tacho->wow_flutter_percent,
                                      pwr->current_5v_ma, pwr->current_12v_ma,
                                      s_motor_live_on, bsp_fdd_get_index_raw());
            break;

        /* SCREEN 4: HEAD STEPPER & SEEK BENCHMARK */
        case UI_STATE_STEPPER_SEEK:
            bsp_led_busy(true);
            const fdd_motion_state_t *m_state = fdd_motion_get_state();
            const fdd_model_spec_t *m_spec = fdd_diagnostics_get_model_spec((fdd_drive_model_t)s_selected_model);

            if (enc_delta != 0) {
                bool inward = (enc_delta > 0);
                fdd_motion_step(inward);
                bsp_buzzer_beep(inward ? 2800 : 2200, 15);
            }

            if (btn_run_edge) {
                /* Run burn-in / alignment seek cycle around track 40 */
                bsp_buzzer_beep(2400, 100);
                fdd_motion_cycle_alignment(m_spec->max_cylinders > 40 ? 40 : 20);
            }

            if (btn_enc_edge) {
                /* Transition to Cat's Eye Alignment */
                s_current_state = UI_STATE_CAT_EYE_ALIGN;
                s_state_timer_ms = 0;
                bsp_buzzer_beep(2000, 80);
            }

            if (btn_back_edge) {
                s_current_state = UI_STATE_MODEL_SELECT;
                s_state_timer_ms = 0;
                bsp_buzzer_beep(1200, 100);
            }

            ui_render_stepper_seek(m_state->current_cylinder, m_spec->max_cylinders,
                                   bsp_fdd_is_track00(), bsp_fdd_is_write_protected(),
                                   bsp_fdd_is_disk_changed(), bsp_fdd_get_index_raw(),
                                   m_state->step_loss_count);
            break;

        /* SCREEN 5: CAT'S EYE RADIAL ALIGNMENT (DYSAN 224/2A) */
        case UI_STATE_CAT_EYE_ALIGN:
            bsp_led_busy(true);
            if (btn_enc_edge) {
                s_head_side = 1 - s_head_side;
                bsp_fdd_set_side(s_head_side);
                bsp_buzzer_beep(2200, 50);
            }

            if (btn_back_edge) {
                s_current_state = UI_STATE_MODEL_SELECT;
                s_state_timer_ms = 0;
                bsp_buzzer_beep(1200, 100);
            }

            /* Read live analog lobe amplitudes from Dysan alignment track via ADC */
            const fdd_cat_eye_metrics_t *ce = fdd_analog_scope_sample(s_head_side);
            ui_render_cat_eye_alignment(40, ce->lobe_a_mv_vpp, ce->lobe_b_mv_vpp,
                                        ce->symmetry_percent, ce->azimuth_arcmin);
            break;

        /* SCREEN 6: AUTOMATED 5-STAGE DIAGNOSTIC PROGRESS */
        case UI_STATE_DIAG_PROGRESS:
            bsp_led_busy(true);
            bsp_led_ready(false);

            /* Run the complete diagnostic suite with live abort check */
            s_active_report = fdd_diagnostics_run_full((fdd_drive_model_t)s_selected_model,
                                                       NULL,
                                                       bsp_btn_back_pressed);

            /* When complete, switch to final report */
            s_current_state = UI_STATE_DIAG_REPORT;
            s_state_timer_ms = 0;
            break;

        /* SCREEN 7: DIAGNOSTIC FINAL REPORT */
        case UI_STATE_DIAG_REPORT:
            bsp_led_busy(false);
            if (s_active_report && s_active_report->overall_status == TEST_RESULT_PASS) {
                bsp_led_ready(true);
                bsp_led_fault(false);
            } else {
                bsp_led_ready(false);
                bsp_led_fault(true);
            }

            if (btn_run_edge) {
                /* Open Model Repair Advisor */
                s_current_state = UI_STATE_REPAIR_ADVISOR;
                s_state_timer_ms = 0;
                bsp_buzzer_beep(2000, 80);
            }

            if (btn_back_edge) {
                s_current_state = UI_STATE_MODEL_SELECT;
                s_state_timer_ms = 0;
                bsp_buzzer_beep(1200, 100);
            }

            ui_render_diag_report(s_active_report);
            break;

        /* SCREEN 8: OEM REPAIR ADVISOR */
        case UI_STATE_REPAIR_ADVISOR:
            bsp_led_busy(false);
            if (btn_back_edge || btn_run_edge) {
                s_current_state = UI_STATE_MODEL_SELECT;
                s_state_timer_ms = 0;
                bsp_buzzer_beep(1200, 100);
            }

            const char *guide = "Ispezione guide di scorrimento e recap elettrolitici SMD consigliato.";
            if (s_active_report && s_active_report->fault_count > 0) {
                guide = fdd_diagnostics_get_repair_guide((fdd_drive_model_t)s_selected_model,
                                                         s_active_report->subtests[0].fault_code);
            }
            ui_render_repair_advisor((fdd_drive_model_t)s_selected_model, guide);
            break;

        /* ERROR POPUP ALERT */
        case UI_STATE_ERROR_ALERT:
            bsp_led_fault(true);
            bsp_led_ready(false);
            bsp_led_busy(false);

            if (btn_run_edge || btn_back_edge) {
                fdd_power_clear_faults();
                s_current_state = UI_STATE_MODEL_SELECT;
                s_state_timer_ms = 0;
                bsp_led_fault(false);
                bsp_buzzer_beep(1500, 150);
            }

            ui_render_error_alert(s_err_title, s_err_msg);
            break;
    }
}
