/**
 * @file    display_ui.c
 * @brief   Retro-Diag FDD Master Tester 160x80 IPS RGB565 Graphical UI Implementation
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 */

#include "display_ui.h"
#include "hal_display.h"
#include "ord_boot_logo_rgb565.h"
#include <stdio.h>
#include <string.h>

static uint16_t g_framebuffer[LCD_WIDTH * LCD_HEIGHT];

uint16_t *ui_get_framebuffer(void) {
    return g_framebuffer;
}

void ui_clear(uint16_t color_rgb565) {
    for (uint32_t i = 0U; i < (LCD_WIDTH * LCD_HEIGHT); i++) {
        g_framebuffer[i] = color_rgb565;
    }
}

void ui_draw_rect(uint16_t x, uint16_t y, uint16_t w, uint16_t h, uint16_t color) {
    for (uint16_t py = y; (py < (y + h)) && (py < LCD_HEIGHT); py++) {
        for (uint16_t px = x; (px < (x + w)) && (px < LCD_WIDTH); px++) {
            g_framebuffer[py * LCD_WIDTH + px] = color;
        }
    }
}

/* 5x7 ASCII Bitmap Font */
static const uint8_t k_font5x7_digits[10][5] = {
    {0x3E,0x51,0x49,0x45,0x3E}, /* 0 */
    {0x00,0x42,0x7F,0x40,0x00}, /* 1 */
    {0x42,0x61,0x51,0x49,0x46}, /* 2 */
    {0x21,0x41,0x45,0x4B,0x31}, /* 3 */
    {0x18,0x14,0x12,0x7F,0x10}, /* 4 */
    {0x27,0x45,0x45,0x45,0x39}, /* 5 */
    {0x3C,0x4A,0x49,0x49,0x30}, /* 6 */
    {0x01,0x71,0x09,0x05,0x03}, /* 7 */
    {0x36,0x49,0x49,0x49,0x36}, /* 8 */
    {0x06,0x49,0x49,0x29,0x1E}  /* 9 */
};

static const uint8_t k_font5x7_alpha[26][5] = {
    {0x7E,0x11,0x11,0x11,0x7E}, /* A */
    {0x7F,0x49,0x49,0x49,0x36}, /* B */
    {0x3E,0x41,0x41,0x41,0x22}, /* C */
    {0x7F,0x41,0x41,0x22,0x1C}, /* D */
    {0x7F,0x49,0x49,0x49,0x41}, /* E */
    {0x7F,0x09,0x09,0x09,0x01}, /* F */
    {0x3E,0x41,0x49,0x49,0x7A}, /* G */
    {0x7F,0x08,0x08,0x08,0x7F}, /* H */
    {0x00,0x41,0x7F,0x41,0x00}, /* I */
    {0x20,0x40,0x41,0x3F,0x01}, /* J */
    {0x7F,0x08,0x14,0x22,0x41}, /* K */
    {0x7F,0x40,0x40,0x40,0x40}, /* L */
    {0x7F,0x02,0x0C,0x02,0x7F}, /* M */
    {0x7F,0x04,0x08,0x10,0x7F}, /* N */
    {0x3E,0x41,0x41,0x41,0x3E}, /* O */
    {0x7F,0x09,0x09,0x09,0x06}, /* P */
    {0x3E,0x41,0x51,0x21,0x5E}, /* Q */
    {0x7F,0x09,0x19,0x29,0x46}, /* R */
    {0x46,0x49,0x49,0x49,0x31}, /* S */
    {0x01,0x01,0x7F,0x01,0x01}, /* T */
    {0x3F,0x40,0x40,0x40,0x3F}, /* U */
    {0x1F,0x20,0x40,0x20,0x1F}, /* V */
    {0x3F,0x40,0x38,0x40,0x3F}, /* W */
    {0x63,0x14,0x08,0x14,0x63}, /* X */
    {0x07,0x08,0x70,0x08,0x07}, /* Y */
    {0x61,0x51,0x49,0x45,0x43}  /* Z */
};

static void draw_char_5x7(uint16_t x, uint16_t y, char c, uint16_t fg, uint16_t bg) {
    const uint8_t *glyph = NULL;
    uint8_t punct[5] = {0, 0, 0, 0, 0};

    if (c >= '0' && c <= '9') {
        glyph = k_font5x7_digits[c - '0'];
    } else if (c >= 'A' && c <= 'Z') {
        glyph = k_font5x7_alpha[c - 'A'];
    } else if (c >= 'a' && c <= 'z') {
        glyph = k_font5x7_alpha[c - 'a'];
    } else {
        if (c == '-')      { punct[1]=0x08; punct[2]=0x08; punct[3]=0x08; }
        else if (c == '+') { punct[1]=0x08; punct[2]=0x1C; punct[3]=0x08; }
        else if (c == '.') { punct[2]=0x40; }
        else if (c == ':') { punct[2]=0x24; }
        else if (c == '?') { punct[0]=0x02; punct[1]=0x01; punct[2]=0x51; punct[3]=0x09; punct[4]=0x06; }
        else if (c == '!') { punct[2]=0x5F; }
        else if (c == '[') { punct[1]=0x7F; punct[2]=0x41; punct[3]=0x41; }
        else if (c == ']') { punct[1]=0x41; punct[2]=0x41; punct[3]=0x7F; }
        else if (c == '=') { punct[1]=0x14; punct[2]=0x14; punct[3]=0x14; }
        else if (c == '/') { punct[0]=0x20; punct[1]=0x10; punct[2]=0x08; punct[3]=0x04; punct[4]=0x02; }
        else if (c == '%') { punct[0]=0x62; punct[1]=0x64; punct[2]=0x08; punct[3]=0x13; punct[4]=0x23; }
        else if (c == '"') { punct[1]=0x03; punct[3]=0x03; }
        glyph = punct;
    }

    for (uint8_t col = 0U; col < 5U; col++) {
        uint8_t bits = glyph[col];
        for (uint8_t row = 0U; row < 7U; row++) {
            uint16_t px = x + col;
            uint16_t py = y + row;
            if (px < LCD_WIDTH && py < LCD_HEIGHT) {
                if (bits & (1U << row)) {
                    g_framebuffer[py * LCD_WIDTH + px] = fg;
                } else if (bg != fg) {
                    g_framebuffer[py * LCD_WIDTH + px] = bg;
                }
            }
        }
    }
}

void ui_draw_text_5x7(uint16_t x, uint16_t y, const char *str, uint16_t fg, uint16_t bg) {
    uint16_t cur_x = x;
    while (str && *str && (cur_x + 5U <= LCD_WIDTH)) {
        draw_char_5x7(cur_x, y, *str++, fg, bg);
        cur_x += 6U;
    }
}

/* ============================================================================
 * BOOT SPLASH SCREEN IMPLEMENTATION (Retro-Diag FDD Master Tester)
 * ============================================================================ */

void ui_show_boot_logo_static(void) {
    /* Render stabilized frame (phase t=30) of the FDD Master Tester splash */
    ord_boot_render_frame(g_framebuffer, 30U);
    hal_display_flush_rgb565(g_framebuffer);
}

void ui_show_boot_logo_animated(uint16_t duration_ms) {
    uint32_t start = hal_get_tick_ms();
    uint32_t frame = 0U;
    while ((hal_get_tick_ms() - start) < duration_ms) {
        ord_boot_render_frame(g_framebuffer, frame++);
        hal_display_flush_rgb565(g_framebuffer);
        hal_delay_ms(16U); /* ~60 FPS smooth dynamic rainbow shader */
    }
}

/* ============================================================================
 * APPLICATION SCREEN RENDERERS
 * ============================================================================ */

static const char *k_drive_names[FDD_TYPE_COUNT] = {
    "3.5\" 1.44M/720K (300 RPM)",
    "5.25\" 1.2M HD (360 RPM)",
    "5.25\" 360K DD (300 RPM)",
    "8\" SHUGART SA800 (360 RPM)",
    "3\" AMSTRAD/CPC (300 RPM)",
    "APPLE II DISK II (20-PIN)"
};

void ui_render_drive_select(fdd_drive_type_t selected_type) {
    ui_clear(COL_BG_OBSIDIAN);

    /* Title Bar */
    ui_draw_rect(0, 0, LCD_WIDTH, 14, COL_BLUE_COBALT);
    ui_draw_text_5x7(4, 3, "RETRO-DIAG: SELEZIONA DRIVE", COL_TEXT_WHITE, COL_BLUE_COBALT);

    /* Drive Selection List */
    for (uint8_t i = 0; i < FDD_TYPE_COUNT && i < 3; i++) {
        uint8_t idx = (selected_type + i) % FDD_TYPE_COUNT;
        uint16_t y = 18 + i * 18;
        uint16_t bg = (i == 0) ? COL_AMBER_GOLD : COL_PANEL_DARK;
        uint16_t fg = (i == 0) ? COL_BG_OBSIDIAN : COL_TEXT_WHITE;

        ui_draw_rect(4, y, LCD_WIDTH - 8, 16, bg);
        ui_draw_text_5x7(8, y + 4, k_drive_names[idx], fg, bg);
    }

    /* Footer Navigation */
    ui_draw_rect(0, 68, LCD_WIDTH, 12, COL_PANEL_DARK);
    ui_draw_text_5x7(4, 70, "[ENC]:SCORRI   [RUN]:AVVIA", COL_TEXT_MUTED, COL_PANEL_DARK);

    hal_display_flush_rgb565(g_framebuffer);
}

void ui_render_rpm_monitor(float current_rpm, float target_rpm, float jitter_percent, bool index_pulse) {
    ui_clear(COL_BG_OBSIDIAN);

    /* Header */
    ui_draw_rect(0, 0, LCD_WIDTH, 14, COL_BLUE_COBALT);
    ui_draw_text_5x7(4, 3, "MONITOR RPM & INDEX PULSE", COL_TEXT_WHITE, COL_BLUE_COBALT);

    /* Index Pulse LED indicator */
    uint16_t led_col = index_pulse ? COL_CYAN_NEON : COL_GRID_SLATE;
    ui_draw_rect(LCD_WIDTH - 18, 3, 12, 8, led_col);

    /* Live RPM readout */
    char buf[32];
    snprintf(buf, sizeof(buf), "RPM: %6.1f", (double)current_rpm);
    ui_draw_text_5x7(6, 20, buf, COL_GREEN_PASS, COL_BG_OBSIDIAN);

    snprintf(buf, sizeof(buf), "TARGET: %3.0f RPM", (double)target_rpm);
    ui_draw_text_5x7(6, 32, buf, COL_AMBER_GOLD, COL_BG_OBSIDIAN);

    snprintf(buf, sizeof(buf), "JITTER: %4.2f%%", (double)jitter_percent);
    ui_draw_text_5x7(6, 44, buf, (jitter_percent > 1.5f) ? COL_RED_FAIL : COL_CYAN_NEON, COL_BG_OBSIDIAN);

    /* RPM Graphical Bar */
    ui_draw_rect(4, 56, LCD_WIDTH - 8, 8, COL_PANEL_DARK);
    float ratio = current_rpm / (target_rpm * 1.2f);
    if (ratio > 1.0f) ratio = 1.0f;
    uint16_t bar_w = (uint16_t)((LCD_WIDTH - 12) * ratio);
    if (bar_w > 0) {
        ui_draw_rect(6, 58, bar_w, 4, COL_GREEN_PASS);
    }

    /* Footer */
    ui_draw_rect(0, 68, LCD_WIDTH, 12, COL_PANEL_DARK);
    ui_draw_text_5x7(4, 70, "[BACK]:STOP MOTOR & MENU", COL_TEXT_MUTED, COL_PANEL_DARK);

    hal_display_flush_rgb565(g_framebuffer);
}

void ui_render_track_seek(uint8_t current_track, uint8_t target_track, bool trk0_sensor, bool wp_sensor) {
    ui_clear(COL_BG_OBSIDIAN);

    ui_draw_rect(0, 0, LCD_WIDTH, 14, COL_BLUE_COBALT);
    ui_draw_text_5x7(4, 3, "SEEK TEST & STEP MOTOR", COL_TEXT_WHITE, COL_BLUE_COBALT);

    char buf[32];
    snprintf(buf, sizeof(buf), "TRK ATTUALE : %2u", (unsigned)current_track);
    ui_draw_text_5x7(6, 20, buf, COL_TEXT_WHITE, COL_BG_OBSIDIAN);

    snprintf(buf, sizeof(buf), "TRK TARGET  : %2u", (unsigned)target_track);
    ui_draw_text_5x7(6, 32, buf, COL_CYAN_NEON, COL_BG_OBSIDIAN);

    snprintf(buf, sizeof(buf), "TRK00: %s  WP: %s",
             trk0_sensor ? "ATTIVO" : "OFF   ",
             wp_sensor   ? "PROTETTO" : "LIBERO  ");
    ui_draw_text_5x7(6, 44, buf, trk0_sensor ? COL_GREEN_PASS : COL_AMBER_GOLD, COL_BG_OBSIDIAN);

    /* Track position bar (0..79) */
    ui_draw_rect(4, 56, LCD_WIDTH - 8, 8, COL_PANEL_DARK);
    uint16_t pos_x = 6 + (uint16_t)(((LCD_WIDTH - 16) * current_track) / 79U);
    ui_draw_rect(pos_x, 57, 4, 6, COL_AMBER_GOLD);

    ui_draw_rect(0, 68, LCD_WIDTH, 12, COL_PANEL_DARK);
    ui_draw_text_5x7(4, 70, "[RUN]:PASSO  [BACK]:ANNULLA", COL_TEXT_MUTED, COL_PANEL_DARK);

    hal_display_flush_rgb565(g_framebuffer);
}

void ui_render_head_alignment(uint8_t track, float lobe_a_vpp, float lobe_b_vpp, float symmetry_pct) {
    ui_clear(COL_BG_OBSIDIAN);

    ui_draw_rect(0, 0, LCD_WIDTH, 14, COL_ORANGE_WARM);
    char buf[32];
    snprintf(buf, sizeof(buf), "ALLINEAMENTO TESTINA T%02u", (unsigned)track);
    ui_draw_text_5x7(4, 3, buf, COL_TEXT_WHITE, COL_ORANGE_WARM);

    snprintf(buf, sizeof(buf), "LOBO A: %4.2f Vpp", (double)lobe_a_vpp);
    ui_draw_text_5x7(6, 20, buf, COL_CYAN_NEON, COL_BG_OBSIDIAN);

    snprintf(buf, sizeof(buf), "LOBO B: %4.2f Vpp", (double)lobe_b_vpp);
    ui_draw_text_5x7(6, 32, buf, COL_CYAN_NEON, COL_BG_OBSIDIAN);

    snprintf(buf, sizeof(buf), "SIMMETRIA CAT-EYE: %4.1f%%", (double)symmetry_pct);
    uint16_t sym_col = (symmetry_pct >= 90.0f) ? COL_GREEN_PASS : ((symmetry_pct >= 75.0f) ? COL_AMBER_GOLD : COL_RED_FAIL);
    ui_draw_text_5x7(6, 44, buf, sym_col, COL_BG_OBSIDIAN);

    /* Visual dual-lobe gauge */
    ui_draw_rect(4, 56, LCD_WIDTH - 8, 8, COL_PANEL_DARK);
    uint16_t w_a = (uint16_t)(((LCD_WIDTH - 12) / 2) * (lobe_a_vpp / 2.0f));
    uint16_t w_b = (uint16_t)(((LCD_WIDTH - 12) / 2) * (lobe_b_vpp / 2.0f));
    if (w_a > (LCD_WIDTH / 2 - 8)) w_a = LCD_WIDTH / 2 - 8;
    if (w_b > (LCD_WIDTH / 2 - 8)) w_b = LCD_WIDTH / 2 - 8;

    ui_draw_rect(LCD_WIDTH / 2 - w_a, 58, w_a, 4, COL_CYAN_NEON);
    ui_draw_rect(LCD_WIDTH / 2 + 2, 58, w_b, 4, COL_AMBER_GOLD);

    ui_draw_rect(0, 68, LCD_WIDTH, 12, COL_PANEL_DARK);
    ui_draw_text_5x7(4, 70, "[ENC]:TRK REF  [BACK]:ESCI", COL_TEXT_MUTED, COL_PANEL_DARK);

    hal_display_flush_rgb565(g_framebuffer);
}

void ui_render_error_alert(const char *title, const char *msg) {
    ui_clear(COL_BG_OBSIDIAN);

    ui_draw_rect(0, 0, LCD_WIDTH, 14, COL_RED_FAIL);
    ui_draw_text_5x7(4, 3, title ? title : "ALLARME HARDWARE", COL_TEXT_WHITE, COL_RED_FAIL);

    ui_draw_text_5x7(6, 24, msg ? msg : "Errore generico riscontrato", COL_AMBER_GOLD, COL_BG_OBSIDIAN);
    ui_draw_text_5x7(6, 42, "Verifica rail o assorbimento", COL_TEXT_WHITE, COL_BG_OBSIDIAN);

    ui_draw_rect(0, 68, LCD_WIDTH, 12, COL_PANEL_DARK);
    ui_draw_text_5x7(4, 70, "[RUN]:RESET ALLARME", COL_GREEN_PASS, COL_PANEL_DARK);

    hal_display_flush_rgb565(g_framebuffer);
}
