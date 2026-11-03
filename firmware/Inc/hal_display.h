/**
 * @file    hal_display.h
 * @brief   Hardware Abstraction Layer for ST7735S / ST7789 IPS Display on STM32F407
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 */

#ifndef HAL_DISPLAY_H
#define HAL_DISPLAY_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Initializes SPI peripheral, GPIOs (DC, CS, RST, BLK) and LCD controller
 */
void hal_display_init(void);

/**
 * @brief Transmits full RGB565 framebuffer to display via high-speed SPI/DMA
 * @param fb Pointer to 160x80 RGB565 framebuffer (25,600 bytes)
 */
void hal_display_flush_rgb565(const uint16_t *fb);

/**
 * @brief Millisecond delay wrapper (HAL_Delay or DWT cycle counter)
 */
void hal_delay_ms(uint32_t ms);

/**
 * @brief Millisecond system tick counter (HAL_GetTick)
 */
uint32_t hal_get_tick_ms(void);

#ifdef __cplusplus
}
#endif

#endif /* HAL_DISPLAY_H */
