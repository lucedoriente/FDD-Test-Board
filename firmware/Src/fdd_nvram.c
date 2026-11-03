/**
 * @file    fdd_nvram.c
 * @brief   Non-Volatile Configuration Storage Implementation (STM32 Flash Sector 11)
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 */

#include "fdd_nvram.h"
#include <string.h>

/* STM32F407 Flash Sector 11: Base 0x080E0000, Size 128 KB */
#define FLASH_NVRAM_BASE_ADDR   0x080E0000U
#define FLASH_NVRAM_SECTOR      FLASH_SECTOR_11

static fdd_nvram_config_t s_config;

static uint16_t calculate_crc16(const uint8_t *data, size_t length) {
    uint16_t crc = 0xFFFFU;
    for (size_t i = 0; i < length; i++) {
        crc ^= (uint16_t)data[i];
        for (uint8_t j = 0; j < 8; j++) {
            if (crc & 0x0001U) {
                crc = (crc >> 1) ^ 0xA001U;
            } else {
                crc >>= 1;
            }
        }
    }
    return crc;
}

void fdd_nvram_reset_defaults(void) {
    memset(&s_config, 0, sizeof(s_config));
    s_config.magic = NVRAM_MAGIC_WORD;
    s_config.version = NVRAM_STRUCT_VERSION;
    s_config.last_selected_model = (uint8_t)DRIVE_MODEL_CHINON_FB354;
    s_config.buzzer_enabled = 1;
    s_config.display_brightness = 100;
    s_config.shunt_zero_offset_5v_ma = 0.0f;
    s_config.shunt_zero_offset_12v_ma = 0.0f;
    s_config.shunt_zero_offset_24v_ma = 0.0f;
    s_config.total_seek_cycles_count = 0;
    s_config.total_operating_minutes = 0;
    s_config.crc16 = calculate_crc16((const uint8_t *)&s_config.last_selected_model,
                                     sizeof(s_config) - offsetof(fdd_nvram_config_t, last_selected_model));
}

void fdd_nvram_init(void) {
    const fdd_nvram_config_t *flash_ptr = (const fdd_nvram_config_t *)FLASH_NVRAM_BASE_ADDR;

    /* Check magic word and version */
    if (flash_ptr->magic == NVRAM_MAGIC_WORD && flash_ptr->version == NVRAM_STRUCT_VERSION) {
        uint16_t calc = calculate_crc16((const uint8_t *)&flash_ptr->last_selected_model,
                                        sizeof(fdd_nvram_config_t) - offsetof(fdd_nvram_config_t, last_selected_model));
        if (calc == flash_ptr->crc16) {
            /* Valid configuration found */
            memcpy(&s_config, flash_ptr, sizeof(fdd_nvram_config_t));
            return;
        }
    }

    /* Fallback to factory defaults if Flash is unwritten or corrupted */
    fdd_nvram_reset_defaults();
}

fdd_nvram_config_t *fdd_nvram_get(void) {
    return &s_config;
}

bool fdd_nvram_save(void) {
    /* Recalculate CRC */
    s_config.crc16 = calculate_crc16((const uint8_t *)&s_config.last_selected_model,
                                     sizeof(fdd_nvram_config_t) - offsetof(fdd_nvram_config_t, last_selected_model));

    /* Unlock Flash */
    HAL_FLASH_Unlock();

    /* Erase Sector 11 */
    FLASH_EraseInitTypeDef erase = {0};
    erase.TypeErase = FLASH_TYPEERASE_SECTORS;
    erase.Sector = FLASH_NVRAM_SECTOR;
    erase.NbSectors = 1;
    erase.VoltageRange = FLASH_VOLTAGE_RANGE_3;

    uint32_t sector_error = 0;
    if (HAL_FLASHEx_Erase(&erase, &sector_error) != HAL_OK) {
        HAL_FLASH_Lock();
        return false;
    }

    /* Program Word by Word */
    uint32_t *src = (uint32_t *)&s_config;
    uint32_t dst = FLASH_NVRAM_BASE_ADDR;
    uint32_t words = (sizeof(fdd_nvram_config_t) + 3U) / 4U;

    for (uint32_t i = 0; i < words; i++) {
        if (HAL_FLASH_Program(FLASH_TYPEPROGRAM_WORD, dst, src[i]) != HAL_OK) {
            HAL_FLASH_Lock();
            return false;
        }
        dst += 4U;
    }

    HAL_FLASH_Lock();

    /* Verification Read-Back */
    const fdd_nvram_config_t *verify = (const fdd_nvram_config_t *)FLASH_NVRAM_BASE_ADDR;
    return (memcmp(&s_config, verify, sizeof(fdd_nvram_config_t)) == 0);
}
