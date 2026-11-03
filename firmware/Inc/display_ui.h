/**
 * @file    display_ui.h
 * @brief   Retro-Diag FDD Master Tester 160x80 IPS RGB565 Graphical UI Specification
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 */

#ifndef DISPLAY_UI_H
#define DISPLAY_UI_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

#define LCD_WIDTH               160U
#define LCD_HEIGHT              80U

/* RGB565 Color Palette (Retro-Diag Family Visual Identity) */
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

/* FDD Drive Types Supported */
typedef enum {
    FDD_TYPE_350_HD = 0,    /**< 3.5" 1.44MB / 720KB (300 RPM) */
    FDD_TYPE_525_HD,        /**< 5.25" 1.2MB High Density (360 RPM) */
    FDD_TYPE_525_DD,        /**< 5.25" 360KB Double Density (300 RPM) */
    FDD_TYPE_800_SHUGART,   /**< 8" Shugart SA800/SA850 (360 RPM, 50-pin) */
    FDD_TYPE_300_COMPACT,   /**< 3" Amstrad / Spectrum +3 (300 RPM, 26-pin) */
    FDD_TYPE_APPLE_II,      /**< Apple II Disk II (20-pin ribbon) */
    FDD_TYPE_COUNT
} fdd_drive_type_t;

/* Framebuffer Access (160x80x2 = 25,600 Bytes in STM32F407 SRAM) */
uint16_t *ui_get_framebuffer(void);
void      ui_clear(uint16_t color_rgb565);
void      ui_draw_rect(uint16_t x, uint16_t y, uint16_t w, uint16_t h, uint16_t color);
void      ui_draw_text_5x7(uint16_t x, uint16_t y, const char *str, uint16_t fg, uint16_t bg);

/* Boot Logo Functions */
void      ui_show_boot_logo_static(void);
void      ui_show_boot_logo_animated(uint16_t duration_ms);

/* Application Screen Renderers */
void      ui_render_drive_select(fdd_drive_type_t selected_type);
void      ui_render_rpm_monitor(float current_rpm, float target_rpm, float jitter_percent, bool index_pulse);
void      ui_render_track_seek(uint8_t current_track, uint8_t target_track, bool trk0_sensor, bool wp_sensor);
void      ui_render_head_alignment(uint8_t track, float lobe_a_vpp, float lobe_b_vpp, float symmetry_pct);
void      ui_render_error_alert(const char *title, const char *msg);

#ifdef __cplusplus
}
#endif

#endif /* DISPLAY_UI_H */
