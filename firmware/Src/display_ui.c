/**
 * @file    display_ui.c
 * @brief   Retro-Diag FDD Master Tester 160x80 IPS RGB565 Graphical UI Engine Implementation
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 */

#include "display_ui.h"
#include "hal_display.h"
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

void ui_fill_rect(uint16_t x, uint16_t y, uint16_t w, uint16_t h, uint16_t color) {
    for (uint16_t py = y; (py < (y + h)) && (py < LCD_HEIGHT); py++) {
        for (uint16_t px = x; (px < (x + w)) && (px < LCD_WIDTH); px++) {
            g_framebuffer[py * LCD_WIDTH + px] = color;
        }
    }
}

void ui_draw_rect(uint16_t x, uint16_t y, uint16_t w, uint16_t h, uint16_t color) {
    if (w == 0 || h == 0) return;
    for (uint16_t px = x; (px < (x + w)) && (px < LCD_WIDTH); px++) {
        g_framebuffer[y * LCD_WIDTH + px] = color;
        if (y + h - 1 < LCD_HEIGHT) {
            g_framebuffer[(y + h - 1) * LCD_WIDTH + px] = color;
        }
    }
    for (uint16_t py = y; (py < (y + h)) && (py < LCD_HEIGHT); py++) {
        g_framebuffer[py * LCD_WIDTH + x] = color;
        if (x + w - 1 < LCD_WIDTH) {
            g_framebuffer[py * LCD_WIDTH + (x + w - 1)] = color;
        }
    }
}

/* ========================================================================== */
/* Font 5x7 ASCII Bitmap Data                                                 */
/* ========================================================================== */

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
        else if (c == ',') { punct[2]=0x60; }
        else if (c == ':') { punct[2]=0x24; }
        else if (c == '?') { punct[0]=0x02; punct[1]=0x01; punct[2]=0x51; punct[3]=0x09; punct[4]=0x06; }
        else if (c == '!') { punct[2]=0x5F; }
        else if (c == '[') { punct[1]=0x7F; punct[2]=0x41; punct[3]=0x41; }
        else if (c == ']') { punct[1]=0x41; punct[2]=0x41; punct[3]=0x7F; }
        else if (c == '(') { punct[2]=0x3E; punct[3]=0x41; }
        else if (c == ')') { punct[1]=0x41; punct[2]=0x3E; }
        else if (c == '=') { punct[1]=0x14; punct[2]=0x14; punct[3]=0x14; }
        else if (c == '/') { punct[0]=0x20; punct[1]=0x10; punct[2]=0x08; punct[3]=0x04; punct[4]=0x02; }
        else if (c == '%') { punct[0]=0x62; punct[1]=0x64; punct[2]=0x08; punct[3]=0x13; punct[4]=0x23; }
        else if (c == '"') { punct[1]=0x03; punct[3]=0x03; }
        else if (c == '\'') { punct[2]=0x03; }
        else if (c == '>') { punct[1]=0x41; punct[2]=0x22; punct[3]=0x14; punct[4]=0x08; }
        else if (c == '<') { punct[0]=0x08; punct[1]=0x14; punct[2]=0x22; punct[3]=0x41; }
        else if (c == '|') { punct[2]=0x7F; }
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

/* 2x Scaled Large Digits for RPM */
void ui_draw_large_digit(uint16_t x, uint16_t y, char digit, uint16_t fg, uint16_t bg) {
    if (digit < '0' || digit > '9') {
        if (digit == '.') {
            ui_fill_rect(x + 2, y + 10, 3, 3, fg);
        }
        return;
    }
    const uint8_t *g = k_font5x7_digits[digit - '0'];
    for (uint8_t col = 0; col < 5; col++) {
        uint8_t b = g[col];
        for (uint8_t row = 0; row < 7; row++) {
            if (b & (1U << row)) {
                ui_fill_rect(x + col * 2, y + row * 2, 2, 2, fg);
            } else if (bg != fg) {
                ui_fill_rect(x + col * 2, y + row * 2, 2, 2, bg);
            }
        }
    }
}

/* ========================================================================== */
/* SCREEN 1: BOOT & SELF-TEST                                                 */
/* ========================================================================== */
void ui_render_boot(void) {
    ui_clear(COL_BG_OBSIDIAN);

    /* Header Bar */
    ui_fill_rect(0, 0, LCD_WIDTH, 11, COL_BLUE_COBALT);
    ui_draw_text_5x7(4, 2, "RETRO-DIAG FDD TESTER", COL_TEXT_WHITE, COL_BLUE_COBALT);
    ui_draw_text_5x7(LCD_WIDTH - 42, 2, "v1.0-K9", COL_CYAN_NEON, COL_BLUE_COBALT);

    /* Self-test checks */
    ui_draw_text_5x7(6, 16, "MCU Core: STM32F407 168M", COL_TEXT_WHITE, COL_BG_OBSIDIAN);
    ui_draw_text_5x7(LCD_WIDTH - 24, 16, "[OK]", COL_GREEN_PASS, COL_BG_OBSIDIAN);

    ui_draw_text_5x7(6, 26, "Active E-Fuses (24/12/5V)", COL_TEXT_WHITE, COL_BG_OBSIDIAN);
    ui_draw_text_5x7(LCD_WIDTH - 30, 26, "[ARM]", COL_GREEN_PASS, COL_BG_OBSIDIAN);

    ui_draw_text_5x7(6, 36, "Shunt INA180 (0.8mA/LSB)", COL_TEXT_WHITE, COL_BG_OBSIDIAN);
    ui_draw_text_5x7(LCD_WIDTH - 24, 36, "[OK]", COL_GREEN_PASS, COL_BG_OBSIDIAN);

    ui_draw_text_5x7(6, 46, "Tachometer TIM4 (1MHz)", COL_TEXT_WHITE, COL_BG_OBSIDIAN);
    ui_draw_text_5x7(LCD_WIDTH - 30, 46, "[RDY]", COL_GREEN_PASS, COL_BG_OBSIDIAN);

    ui_draw_text_5x7(6, 56, "ULN2003 4-Phase Stepper", COL_TEXT_WHITE, COL_BG_OBSIDIAN);
    ui_draw_text_5x7(LCD_WIDTH - 24, 56, "[OK]", COL_GREEN_PASS, COL_BG_OBSIDIAN);

    /* Footer */
    ui_fill_rect(0, 68, LCD_WIDTH, 12, COL_PANEL_DARK);
    ui_draw_text_5x7(4, 70, "PREMI RUN PER INIZIARE", COL_CYAN_NEON, COL_PANEL_DARK);

    hal_display_flush_rgb565(g_framebuffer);
}

/* ========================================================================== */
/* SCREEN 2: OEM DRIVE SELECTION MENU                                         */
/* ========================================================================== */
void ui_render_model_select(uint8_t selected_idx) {
    ui_clear(COL_BG_OBSIDIAN);

    const fdd_model_spec_t *spec = fdd_diagnostics_get_model_spec((fdd_drive_model_t)selected_idx);

    /* Header Bar */
    ui_fill_rect(0, 0, LCD_WIDTH, 11, COL_BLUE_COBALT);
    char hbuf[32];
    snprintf(hbuf, sizeof(hbuf), "MODELLO: [%u/%u]", (unsigned)selected_idx, (unsigned)(DRIVE_MODEL_COUNT - 1));
    ui_draw_text_5x7(4, 2, hbuf, COL_TEXT_WHITE, COL_BLUE_COBALT);
    ui_draw_text_5x7(LCD_WIDTH - 30, 2, spec->size_str, COL_AMBER_GOLD, COL_BLUE_COBALT);

    /* Model Name (Prominent) */
    char name_trunc[26];
    strncpy(name_trunc, spec->display_name, sizeof(name_trunc) - 1);
    name_trunc[sizeof(name_trunc) - 1] = '\0';
    ui_draw_text_5x7(4, 18, name_trunc, COL_AMBER_GOLD, COL_BG_OBSIDIAN);

    /* Parameters Box */
    ui_draw_rect(4, 30, LCD_WIDTH - 8, 26, COL_GRID_SLATE);
    char pbuf[32];
    snprintf(pbuf, sizeof(pbuf), "TARGET : %4.0f RPM (+/-%2.0f%%)", (double)spec->nominal_rpm, (double)spec->rpm_tolerance_pct);
    ui_draw_text_5x7(8, 33, pbuf, COL_TEXT_WHITE, COL_BG_OBSIDIAN);

    snprintf(pbuf, sizeof(pbuf), "TRACCE : %2u | STEP: %ums", (unsigned)spec->max_cylinders, (unsigned)spec->recommended_step_rate);
    ui_draw_text_5x7(8, 44, pbuf, COL_CYAN_NEON, COL_BG_OBSIDIAN);

    /* Footer Navigation */
    ui_fill_rect(0, 68, LCD_WIDTH, 12, COL_PANEL_DARK);
    ui_draw_text_5x7(4, 70, "[ENC]:SCORRI  [RUN]:COLLAUDO", COL_TEXT_MUTED, COL_PANEL_DARK);

    hal_display_flush_rgb565(g_framebuffer);
}

/* ========================================================================== */
/* SCREEN 3: LIVE TACHOMETER & EXERCISER                                      */
/* ========================================================================== */
void ui_render_live_tachometer(float rpm, float target_rpm, float wf_pct,
                               float ma_5v, float ma_12v, bool motor_on, bool idx_pulse) {
    ui_clear(COL_BG_OBSIDIAN);

    /* Header Bar */
    ui_fill_rect(0, 0, LCD_WIDTH, 11, COL_BLUE_COBALT);
    ui_draw_text_5x7(4, 2, "TACOMETRO MANDRINO LIVE", COL_TEXT_WHITE, COL_BLUE_COBALT);
    if (idx_pulse) {
        ui_fill_rect(LCD_WIDTH - 16, 2, 12, 7, COL_CYAN_NEON);
        ui_draw_text_5x7(LCD_WIDTH - 15, 2, "ID", COL_BG_OBSIDIAN, COL_CYAN_NEON);
    }

    /* Big RPM Digits */
    char s_rpm[16];
    snprintf(s_rpm, sizeof(s_rpm), "%5.1f", (double)rpm);
    uint16_t x_pos = 6;
    for (uint8_t i = 0; s_rpm[i]; i++) {
        if (s_rpm[i] == '.') {
            ui_draw_large_digit(x_pos, 16, '.', COL_CYAN_NEON, COL_BG_OBSIDIAN);
            x_pos += 6;
        } else {
            ui_draw_large_digit(x_pos, 16, s_rpm[i], COL_CYAN_NEON, COL_BG_OBSIDIAN);
            x_pos += 12;
        }
    }
    ui_draw_text_5x7(x_pos + 4, 22, "RPM", COL_TEXT_MUTED, COL_BG_OBSIDIAN);

    /* Target & W&F readout */
    char buf[32];
    snprintf(buf, sizeof(buf), "W&F: %4.2f%%", (double)wf_pct);
    uint16_t wf_col = (wf_pct < 0.50f) ? COL_GREEN_PASS : ((wf_pct < 1.0f) ? COL_AMBER_GOLD : COL_RED_FAIL);
    ui_draw_text_5x7(LCD_WIDTH - 58, 16, buf, wf_col, COL_BG_OBSIDIAN);

    snprintf(buf, sizeof(buf), "TGT: %3.0f", (double)target_rpm);
    ui_draw_text_5x7(LCD_WIDTH - 58, 26, buf, COL_TEXT_WHITE, COL_BG_OBSIDIAN);

    /* Deviation Bar (-2% to +2%) */
    ui_fill_rect(4, 38, LCD_WIDTH - 8, 8, COL_PANEL_DARK);
    ui_draw_rect(4, 38, LCD_WIDTH - 8, 8, COL_GRID_SLATE);
    /* Center green zone */
    ui_fill_rect(LCD_WIDTH / 2 - 10, 39, 20, 6, COL_GREEN_PASS);
    /* Center mark */
    ui_fill_rect(LCD_WIDTH / 2, 38, 1, 8, COL_TEXT_WHITE);

    float dev_pct = ((rpm - target_rpm) / target_rpm) * 100.0f;
    int16_t needle_offset = (int16_t)(dev_pct * 30.0f);
    if (needle_offset < -60) needle_offset = -60;
    if (needle_offset > 60) needle_offset = 60;
    ui_fill_rect(LCD_WIDTH / 2 + needle_offset - 1, 38, 3, 8, COL_AMBER_GOLD);

    /* Telemetry Currents */
    snprintf(buf, sizeof(buf), "+5V:%3.0fmA  +12V:%3.0fmA", (double)ma_5v, (double)ma_12v);
    ui_draw_text_5x7(6, 52, buf, COL_TEXT_MUTED, COL_BG_OBSIDIAN);

    /* Footer */
    ui_fill_rect(0, 68, LCD_WIDTH, 12, COL_PANEL_DARK);
    snprintf(buf, sizeof(buf), "[RUN]:%s  [BACK]:MENU", motor_on ? "STOP MTR" : "START MTR");
    ui_draw_text_5x7(4, 70, buf, COL_CYAN_NEON, COL_PANEL_DARK);

    hal_display_flush_rgb565(g_framebuffer);
}

/* ========================================================================== */
/* SCREEN 4: HEAD STEPPER & SEEK BENCHMARK                                    */
/* ========================================================================== */
void ui_render_stepper_seek(uint8_t cur_trk, uint8_t max_trk,
                             bool trk0, bool wp, bool rdy, bool idx, uint8_t step_loss) {
    ui_clear(COL_BG_OBSIDIAN);

    /* Header Bar */
    ui_fill_rect(0, 0, LCD_WIDTH, 11, COL_BLUE_COBALT);
    ui_draw_text_5x7(4, 2, "CARRELLO STEPPER & SENSORI", COL_TEXT_WHITE, COL_BLUE_COBALT);

    /* Cylinder big readout */
    char buf[32];
    snprintf(buf, sizeof(buf), "TRK: %02u", (unsigned)cur_trk);
    ui_draw_large_digit(6, 16, '0' + (cur_trk / 10), COL_CYAN_NEON, COL_BG_OBSIDIAN);
    ui_draw_large_digit(18, 16, '0' + (cur_trk % 10), COL_CYAN_NEON, COL_BG_OBSIDIAN);

    snprintf(buf, sizeof(buf), "/ %02u MAX", (unsigned)max_trk);
    ui_draw_text_5x7(32, 22, buf, COL_TEXT_MUTED, COL_BG_OBSIDIAN);

    /* Sensors badges */
    uint16_t b_trk0 = trk0 ? COL_GREEN_PASS : COL_GRID_SLATE;
    ui_fill_rect(LCD_WIDTH - 65, 14, 28, 9, b_trk0);
    ui_draw_text_5x7(LCD_WIDTH - 63, 15, "TRK0", trk0 ? COL_BG_OBSIDIAN : COL_TEXT_MUTED, b_trk0);

    uint16_t b_wp = wp ? COL_AMBER_GOLD : COL_GRID_SLATE;
    ui_fill_rect(LCD_WIDTH - 32, 14, 26, 9, b_wp);
    ui_draw_text_5x7(LCD_WIDTH - 29, 15, "WP", wp ? COL_BG_OBSIDIAN : COL_TEXT_MUTED, b_wp);

    uint16_t b_rdy = rdy ? COL_GREEN_PASS : COL_GRID_SLATE;
    ui_fill_rect(LCD_WIDTH - 65, 26, 28, 9, b_rdy);
    ui_draw_text_5x7(LCD_WIDTH - 63, 27, "RDY", rdy ? COL_BG_OBSIDIAN : COL_TEXT_MUTED, b_rdy);

    uint16_t b_idx = idx ? COL_CYAN_NEON : COL_GRID_SLATE;
    ui_fill_rect(LCD_WIDTH - 32, 26, 26, 9, b_idx);
    ui_draw_text_5x7(LCD_WIDTH - 29, 27, "IDX", idx ? COL_BG_OBSIDIAN : COL_TEXT_MUTED, b_idx);

    /* Position Bar Across Disc Radius */
    ui_fill_rect(4, 42, LCD_WIDTH - 8, 8, COL_PANEL_DARK);
    ui_draw_rect(4, 42, LCD_WIDTH - 8, 8, COL_GRID_SLATE);
    if (max_trk > 0) {
        uint16_t bar_pos = 6 + (uint16_t)(((LCD_WIDTH - 16) * cur_trk) / max_trk);
        ui_fill_rect(bar_pos, 43, 4, 6, COL_CYAN_NEON);
    }

    snprintf(buf, sizeof(buf), "PERDITA PASSI: %u", (unsigned)step_loss);
    uint16_t loss_col = (step_loss == 0) ? COL_GREEN_PASS : COL_RED_FAIL;
    ui_draw_text_5x7(6, 54, buf, loss_col, COL_BG_OBSIDIAN);

    /* Footer */
    ui_fill_rect(0, 68, LCD_WIDTH, 12, COL_PANEL_DARK);
    ui_draw_text_5x7(4, 70, "[ENC]:SEEK  [RUN]:BURN-IN", COL_TEXT_MUTED, COL_PANEL_DARK);

    hal_display_flush_rgb565(g_framebuffer);
}

/* ========================================================================== */
/* SCREEN 5: CAT'S EYE RADIAL ALIGNMENT (DYSAN 224/2A)                        */
/* ========================================================================== */
void ui_render_cat_eye_alignment(uint8_t track, float lobe_a_mv, float lobe_b_mv,
                                  float sym_pct, float azimuth_arcmin) {
    ui_clear(COL_BG_OBSIDIAN);

    /* Header Bar */
    ui_fill_rect(0, 0, LCD_WIDTH, 11, COL_ORANGE_WARM);
    char buf[32];
    snprintf(buf, sizeof(buf), "DYSAN 224/2A (TRACCIA %02u)", (unsigned)track);
    ui_draw_text_5x7(4, 2, buf, COL_TEXT_WHITE, COL_ORANGE_WARM);

    /* Dual Lobe Voltages */
    snprintf(buf, sizeof(buf), "LOBO A: %3.0fmV", (double)lobe_a_mv);
    ui_draw_text_5x7(6, 16, buf, COL_CYAN_NEON, COL_BG_OBSIDIAN);

    snprintf(buf, sizeof(buf), "LOBO B: %3.0fmV", (double)lobe_b_mv);
    ui_draw_text_5x7(LCD_WIDTH - 76, 16, buf, COL_CYAN_NEON, COL_BG_OBSIDIAN);

    /* Symmetry Gauges */
    ui_fill_rect(6, 26, (LCD_WIDTH / 2) - 12, 6, COL_PANEL_DARK);
    uint16_t w_a = (uint16_t)(((LCD_WIDTH / 2) - 14) * (lobe_a_mv / 1000.0f));
    if (w_a > ((LCD_WIDTH / 2) - 14)) w_a = (LCD_WIDTH / 2) - 14;
    ui_fill_rect(6, 26, w_a, 6, COL_CYAN_NEON);

    ui_fill_rect(LCD_WIDTH / 2 + 6, 26, (LCD_WIDTH / 2) - 12, 6, COL_PANEL_DARK);
    uint16_t w_b = (uint16_t)(((LCD_WIDTH / 2) - 14) * (lobe_b_mv / 1000.0f));
    if (w_b > ((LCD_WIDTH / 2) - 14)) w_b = (LCD_WIDTH / 2) - 14;
    ui_fill_rect(LCD_WIDTH / 2 + 6, 26, w_b, 6, COL_AMBER_GOLD);

    /* Symmetry and Azimuth Results */
    snprintf(buf, sizeof(buf), "SIMMETRIA: %4.1f%%", (double)sym_pct);
    uint16_t sym_col = (sym_pct >= 85.0f) ? COL_GREEN_PASS : ((sym_pct >= 70.0f) ? COL_AMBER_GOLD : COL_RED_FAIL);
    ui_draw_text_5x7(6, 38, buf, sym_col, COL_BG_OBSIDIAN);

    snprintf(buf, sizeof(buf), "AZIMUTH: %+2.1f'", (double)azimuth_arcmin);
    ui_draw_text_5x7(6, 50, buf, COL_TEXT_WHITE, COL_BG_OBSIDIAN);

    /* Footer */
    ui_fill_rect(0, 68, LCD_WIDTH, 12, COL_PANEL_DARK);
    ui_draw_text_5x7(4, 70, "[ENC]:LATO 0/1  [BACK]:ESCI", COL_TEXT_MUTED, COL_PANEL_DARK);

    hal_display_flush_rgb565(g_framebuffer);
}

/* ========================================================================== */
/* SCREEN 6: AUTOMATED 5-STAGE DIAGNOSTIC PROGRESS                            */
/* ========================================================================== */
void ui_render_diag_progress(uint8_t percent, const char *stage_name,
                              float elapsed_sec, float current_12v_ma) {
    ui_clear(COL_BG_OBSIDIAN);

    /* Header Bar */
    ui_fill_rect(0, 0, LCD_WIDTH, 11, COL_BLUE_COBALT);
    ui_draw_text_5x7(4, 2, "COLLAUDO AUTOMATICO", COL_TEXT_WHITE, COL_BLUE_COBALT);
    char buf[16];
    snprintf(buf, sizeof(buf), "%3u%%", (unsigned)percent);
    ui_draw_text_5x7(LCD_WIDTH - 28, 2, buf, COL_AMBER_GOLD, COL_BLUE_COBALT);

    /* Stage description */
    ui_draw_text_5x7(6, 18, stage_name ? stage_name : "Test in corso...", COL_CYAN_NEON, COL_BG_OBSIDIAN);

    /* Animated Progress Bar */
    ui_fill_rect(4, 32, LCD_WIDTH - 8, 12, COL_PANEL_DARK);
    ui_draw_rect(4, 32, LCD_WIDTH - 8, 12, COL_GRID_SLATE);
    uint16_t bar_w = (uint16_t)(((LCD_WIDTH - 12) * percent) / 100U);
    if (bar_w > 0) {
        ui_fill_rect(6, 34, bar_w, 8, COL_GREEN_PASS);
    }

    /* Real-time Telemetry */
    snprintf(buf, sizeof(buf), "TEMPO: %3.1fs | +12V: %3.0fmA", (double)elapsed_sec, (double)current_12v_ma);
    ui_draw_text_5x7(6, 50, buf, COL_TEXT_MUTED, COL_BG_OBSIDIAN);

    /* Footer */
    ui_fill_rect(0, 68, LCD_WIDTH, 12, COL_PANEL_DARK);
    ui_draw_text_5x7(4, 70, "[BACK]:INTERROMPI TEST", COL_RED_FAIL, COL_PANEL_DARK);

    hal_display_flush_rgb565(g_framebuffer);
}

/* ========================================================================== */
/* SCREEN 7: DIAGNOSTIC FINAL REPORT                                          */
/* ========================================================================== */
void ui_render_diag_report(const fdd_diagnostic_report_t *rep) {
    ui_clear(COL_BG_OBSIDIAN);

    if (!rep) return;

    /* Header Bar */
    uint16_t hdr_col = (rep->overall_status == TEST_RESULT_PASS) ? COL_GREEN_PASS :
                       ((rep->overall_status == TEST_RESULT_WARN) ? COL_AMBER_GOLD : COL_RED_FAIL);

    ui_fill_rect(0, 0, LCD_WIDTH, 11, hdr_col);
    const char *verdict_str = (rep->overall_status == TEST_RESULT_PASS) ? "ESITO: PASS (OEM OK)" :
                              ((rep->overall_status == TEST_RESULT_WARN) ? "ESITO: WARN (REVISIONE)" : "ESITO: FAIL (GUASTO)");
    ui_draw_text_5x7(4, 2, verdict_str, COL_BG_OBSIDIAN, hdr_col);

    /* Checklist of Subtests (Compact font) */
    uint16_t y = 16;
    for (uint8_t i = 0; i < rep->subtest_count && i < 4; i++) {
        const fdd_subtest_record_t *r = &rep->subtests[i];
        const char *t_res = (r->result == TEST_RESULT_PASS) ? "[P]" : ((r->result == TEST_RESULT_WARN) ? "[W]" : "[F]");
        uint16_t t_col = (r->result == TEST_RESULT_PASS) ? COL_GREEN_PASS : ((r->result == TEST_RESULT_WARN) ? COL_AMBER_GOLD : COL_RED_FAIL);

        char tbuf[28];
        snprintf(tbuf, sizeof(tbuf), "%s %-18.18s", t_res, r->test_name);
        ui_draw_text_5x7(4, y, tbuf, t_col, COL_BG_OBSIDIAN);
        y += 11;
    }

    char count_buf[32];
    snprintf(count_buf, sizeof(count_buf), "ERR: %u | WARN: %u", (unsigned)rep->fault_count, (unsigned)rep->warn_count);
    ui_draw_text_5x7(LCD_WIDTH - 64, 56, count_buf, (rep->fault_count > 0) ? COL_RED_FAIL : COL_GREEN_PASS, COL_BG_OBSIDIAN);

    /* Footer */
    ui_fill_rect(0, 68, LCD_WIDTH, 12, COL_PANEL_DARK);
    ui_draw_text_5x7(4, 70, "[RUN]:GUIDA RIPARAZIONE", COL_CYAN_NEON, COL_PANEL_DARK);

    hal_display_flush_rgb565(g_framebuffer);
}

/* ========================================================================== */
/* SCREEN 8: OEM REPAIR ADVISOR                                               */
/* ========================================================================== */
void ui_render_repair_advisor(fdd_drive_model_t model, const char *guide_summary) {
    ui_clear(COL_BG_OBSIDIAN);

    const fdd_model_spec_t *spec = fdd_diagnostics_get_model_spec(model);

    /* Header Bar */
    ui_fill_rect(0, 0, LCD_WIDTH, 11, COL_AMBER_GOLD);
    char hbuf[32];
    snprintf(hbuf, sizeof(hbuf), "GUIDA: %s", spec->size_str);
    ui_draw_text_5x7(4, 2, hbuf, COL_BG_OBSIDIAN, COL_AMBER_GOLD);

    /* Model label */
    ui_draw_text_5x7(4, 15, spec->display_name, COL_AMBER_GOLD, COL_BG_OBSIDIAN);

    /* Guide text (Truncated/formatted for 160x80) */
    if (guide_summary) {
        char line1[27], line2[27], line3[27];
        strncpy(line1, guide_summary, 26); line1[26] = '\0';
        ui_draw_text_5x7(4, 28, line1, COL_TEXT_WHITE, COL_BG_OBSIDIAN);

        size_t len1 = strlen(line1);
        if (strlen(guide_summary) > len1) {
            strncpy(line2, guide_summary + len1, 26); line2[26] = '\0';
            ui_draw_text_5x7(4, 40, line2, COL_CYAN_NEON, COL_BG_OBSIDIAN);
        }
        size_t len2 = len1 + strlen(line2);
        if (strlen(guide_summary) > len2) {
            strncpy(line3, guide_summary + len2, 26); line3[26] = '\0';
            ui_draw_text_5x7(4, 52, line3, COL_TEXT_MUTED, COL_BG_OBSIDIAN);
        }
    }

    /* Footer */
    ui_fill_rect(0, 68, LCD_WIDTH, 12, COL_PANEL_DARK);
    ui_draw_text_5x7(4, 70, "[BACK]:MENU PRINCIPALE", COL_TEXT_MUTED, COL_PANEL_DARK);

    hal_display_flush_rgb565(g_framebuffer);
}

/* ========================================================================== */
/* ERROR POPUP ALERT                                                          */
/* ========================================================================== */
void ui_render_error_alert(const char *title, const char *msg) {
    ui_clear(COL_BG_OBSIDIAN);

    ui_fill_rect(0, 0, LCD_WIDTH, 14, COL_RED_FAIL);
    ui_draw_text_5x7(4, 3, title ? title : "ALLARME HARDWARE", COL_TEXT_WHITE, COL_RED_FAIL);

    ui_draw_text_5x7(6, 24, msg ? msg : "Corto circuito o sovracorrente", COL_AMBER_GOLD, COL_BG_OBSIDIAN);
    ui_draw_text_5x7(6, 42, "E-Fuse aperto. Ispezionare rail", COL_TEXT_WHITE, COL_BG_OBSIDIAN);

    ui_fill_rect(0, 68, LCD_WIDTH, 12, COL_PANEL_DARK);
    ui_draw_text_5x7(4, 70, "[RUN]:RESET ALLARME", COL_GREEN_PASS, COL_PANEL_DARK);

    hal_display_flush_rgb565(g_framebuffer);
}
