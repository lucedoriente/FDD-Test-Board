/**
 * @file    display_ui.h
 * @brief   Retro-Diag FDD Master Tester 160x80 IPS RGB565 Graphical UI Engine
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 */

#ifndef DISPLAY_UI_H
#define DISPLAY_UI_H

#include <stdint.h>
#include <stdbool.h>
#include "fdd_diagnostics.h"

#ifdef __cplusplus
extern "C" {
#endif

#define LCD_WIDTH               160U
#define LCD_HEIGHT              80U

/* RGB565 Color Palette (Retro-Diag Visual Identity) */
#define RGB565(r, g, b)         ((uint16_t)((((r) & 0xF8U) << 8) | (((g) & 0xFCU) << 3) | (((b) & 0xF8U) >> 3)))

#define COL_BG_OBSIDIAN         RGB565(6, 10, 18)
#define COL_PANEL_DARK          RGB565(14, 22, 36)
#define COL_GRID_SLATE          RGB565(35, 52, 78)
#define COL_TEXT_WHITE          RGB565(240, 246, 255)
#define COL_TEXT_MUTED          RGB565(130, 150, 175)
#define COL_CYAN_NEON           RGB565(0, 228, 255)
#define COL_BLUE_COBALT         RGB565(15, 110, 255)
#define COL_AMBER_GOLD          RGB565(255, 185, 0)
#define COL_ORANGE_WARM         RGB565(255, 95, 0)
#define COL_GREEN_PASS          RGB565(0, 230, 118)
#define COL_RED_FAIL            RGB565(255, 45, 65)

/* Framebuffer Access */
uint16_t *ui_get_framebuffer(void);
void      ui_clear(uint16_t color_rgb565);
void      ui_draw_rect(uint16_t x, uint16_t y, uint16_t w, uint16_t h, uint16_t color);
void      ui_fill_rect(uint16_t x, uint16_t y, uint16_t w, uint16_t h, uint16_t color);
void      ui_draw_text_5x7(uint16_t x, uint16_t y, const char *str, uint16_t fg, uint16_t bg);
void      ui_draw_large_digit(uint16_t x, uint16_t y, char digit, uint16_t fg, uint16_t bg);

/* 8 Standard Screen Renderers (Approved Architecture) */
void      ui_render_boot(void);
void      ui_render_model_select(uint8_t selected_idx);
void      ui_render_live_tachometer(float rpm, float target_rpm, float wf_pct,
                                    float ma_5v, float ma_12v, bool motor_on, bool idx_pulse);
void      ui_render_stepper_seek(uint8_t cur_trk, uint8_t max_trk,
                                 bool trk0, bool wp, bool rdy, bool idx, uint8_t step_loss);
void      ui_render_cat_eye_alignment(uint8_t track, float lobe_a_mv, float lobe_b_mv,
                                      float sym_pct, float azimuth_arcmin);
void      ui_render_diag_progress(uint8_t percent, const char *stage_name,
                                  float elapsed_sec, float current_12v_ma);
void      ui_render_diag_report(const fdd_diagnostic_report_t *rep);
void      ui_render_repair_advisor(fdd_drive_model_t model, const char *guide_summary);

/* Alert popup */
void      ui_render_error_alert(const char *title, const char *msg);

#ifdef __cplusplus
}
#endif

#endif /* DISPLAY_UI_H */
