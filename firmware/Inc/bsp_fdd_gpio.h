/**
 * @file    bsp_fdd_gpio.h
 * @brief   Board Support Package GPIO Driver & Fail-Safe Initialization
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 */

#ifndef BSP_FDD_GPIO_H
#define BSP_FDD_GPIO_H

#include "bsp_fdd_pins.h"

#ifdef __cplusplus
extern "C" {
#endif

/* Power Rails Control */
void bsp_pwr_set_24v(bool enable);
void bsp_pwr_set_12v(bool enable);
void bsp_pwr_set_5v(bool enable);
void bsp_pwr_all_off(void);

/* Status LEDs Control */
void bsp_led_ready(bool on);
void bsp_led_busy(bool on);
void bsp_led_fault(bool on);
void bsp_led_index(bool on);
void bsp_led_read(bool on);
void bsp_led_all_off(void);
void bsp_led_self_test(uint32_t delay_ms);

/* Buzzer Control */
void bsp_buzzer_beep(uint16_t freq_hz, uint16_t duration_ms);

/* Floppy Drive Bus Control (7406 Open-Collector) */
void bsp_fdd_set_motor(bool active);
void bsp_fdd_set_drive_select(uint8_t drive_num, bool active);
void bsp_fdd_set_side(uint8_t side);
void bsp_fdd_set_direction(bool inward);
void bsp_fdd_pulse_step(uint16_t pulse_us);
void bsp_fdd_set_write_gate(bool active);

/* Floppy Drive Sensor Readings (74HC14 Schmitt Inverter) */
bool bsp_fdd_is_track00(void);
bool bsp_fdd_is_write_protected(void);
bool bsp_fdd_is_disk_changed(void);
bool bsp_fdd_get_index_raw(void);

/* Physical Buttons & Encoder Readings */
bool bsp_btn_run_pressed(void);
bool bsp_btn_back_pressed(void);
bool bsp_btn_enc_pressed(void);

/* Initialization */
void bsp_fdd_init(void);

#ifdef __cplusplus
}
#endif

#endif /* BSP_FDD_GPIO_H */
