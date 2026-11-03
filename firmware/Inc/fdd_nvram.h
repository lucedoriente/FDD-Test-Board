/**
 * @file    fdd_nvram.h
 * @brief   Non-Volatile Configuration & Calibration Storage on STM32F407 Flash
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 */

#ifndef FDD_NVRAM_H
#define FDD_NVRAM_H

#include <stdint.h>
#include <stdbool.h>
#include "fdd_diagnostics.h"

#ifdef __cplusplus
extern "C" {
#endif

#define NVRAM_MAGIC_WORD        0x46444454U /* "FDDT" */
#define NVRAM_STRUCT_VERSION    1U

typedef struct __attribute__((packed)) {
    uint32_t magic;                     /**< Magic word for validity check */
    uint16_t version;                   /**< Configuration schema version */
    uint16_t crc16;                     /**< CRC-16 checksum */
    uint8_t  last_selected_model;       /**< Last chosen fdd_drive_model_t */
    uint8_t  buzzer_enabled;            /**< 1 = Audio on, 0 = Muted */
    uint8_t  display_brightness;        /**< Brightness percentage 0..100 */
    uint8_t  reserved;
    float    shunt_zero_offset_5v_ma;   /**< Factory zero-current offset for 5V */
    float    shunt_zero_offset_12v_ma;  /**< Factory zero-current offset for 12V */
    float    shunt_zero_offset_24v_ma;  /**< Factory zero-current offset for 24V */
    uint32_t total_seek_cycles_count;   /**< Total lifetime seek cycles */
    uint32_t total_operating_minutes;   /**< Total power-on hours */
} fdd_nvram_config_t;

/**
 * @brief Initializes NVRAM subsystem and loads config from Flash Sector 11
 */
void fdd_nvram_init(void);

/**
 * @brief Gets pointer to active in-memory configuration
 */
fdd_nvram_config_t *fdd_nvram_get(void);

/**
 * @brief Commits current configuration struct to STM32 Flash
 * @return true if successfully programmed and verified
 */
bool fdd_nvram_save(void);

/**
 * @brief Restores factory default settings
 */
void fdd_nvram_reset_defaults(void);

#ifdef __cplusplus
}
#endif

#endif /* FDD_NVRAM_H */
