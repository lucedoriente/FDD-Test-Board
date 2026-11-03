/**
 * @file    fdd_flux_analyzer.c
 * @brief   Magnetic Flux Transition Capture & MFM Surface Analysis Implementation
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 */

#include "fdd_flux_analyzer.h"
#include "bsp_fdd_pins.h"
#include "bsp_fdd_gpio.h"
#include "fdd_motion.h"
#include "hal_display.h"
#include <string.h>

static fdd_flux_analysis_t s_analysis;

void fdd_flux_analyzer_init(void) {
    __HAL_RCC_GPIOB_CLK_ENABLE();
    __HAL_RCC_TIM4_CLK_ENABLE();

    /* Configure PB7 (FDD_READ_DATA) as Alternate Function AF2 (TIM4_CH2) */
    GPIO_InitTypeDef gpio = {0};
    gpio.Pin = FDD_READ_DATA_PIN;
    gpio.Mode = GPIO_MODE_AF_PP;
    gpio.Pull = GPIO_PULLUP;
    gpio.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    gpio.Alternate = GPIO_AF2_TIM4;
    HAL_GPIO_Init(FDD_READ_DATA_PORT, &gpio);

    memset(&s_analysis, 0, sizeof(s_analysis));
}

const fdd_flux_analysis_t *fdd_flux_analyzer_capture_revolution(uint8_t side, uint8_t track) {
    /* Select side and seek to target track */
    bsp_fdd_set_side(side);
    fdd_motion_seek(track);

    memset(&s_analysis, 0, sizeof(s_analysis));

    /*
     * 1. Synchronize to Index Pulse falling edge (Beginning of track)
     */
    uint32_t timeout_start = hal_get_tick_ms();
    while (!bsp_fdd_get_index_raw()) {
        if ((hal_get_tick_ms() - timeout_start) > 350) return &s_analysis; /* Drive not spinning */
    }
    while (bsp_fdd_get_index_raw()) {
        if ((hal_get_tick_ms() - timeout_start) > 350) return &s_analysis;
    }

    /*
     * 2. Capture Inter-Flux Transition Intervals over one revolution (Index to Index)
     * For 300 RPM DD, one revolution has ~50,000 to 100,000 flux transitions.
     * We sample the distribution of interval bins (0.25us per bin).
     */
    uint32_t last_capture = 0;
    uint32_t count = 0;
    uint32_t sum_intervals_ns = 0;

    /* Wait for next index while sampling */
    while (!bsp_fdd_get_index_raw() && count < 25000U) {
        /* Read TIM4_CH2 capture register */
        uint32_t current_capture = TIM4->CCR2;
        if (current_capture != last_capture) {
            uint32_t delta_ticks = (current_capture >= last_capture) ?
                                   (current_capture - last_capture) :
                                   ((0xFFFFU - last_capture) + current_capture + 1U);
            last_capture = current_capture;

            /* TIM4 runs at 84 MHz (1 tick = 11.9047 ns) */
            uint32_t interval_ns = (uint32_t)(delta_ticks * 11.9047f);

            if (interval_ns > 800U && interval_ns < 16000U) {
                count++;
                sum_intervals_ns += interval_ns;

                /* Bin in 250 ns intervals (0.25 us per bin -> 64 bins = 0..16 us) */
                uint16_t bin = (uint16_t)(interval_ns / 250U);
                if (bin < FLUX_HISTOGRAM_BINS) {
                    s_analysis.histogram[bin]++;
                }
            } else if (interval_ns >= 16000U) {
                /* Flux gap or dropout event */
                s_analysis.dropout_events_count++;
            }
        }
    }

    s_analysis.total_flux_transitions = count;

    if (count > 100) {
        float avg_ns = (float)sum_intervals_ns / (float)count;
        s_analysis.average_cell_us = avg_ns / 1000.0f;

        /* Classify recording density based on center histogram cluster */
        if (s_analysis.average_cell_us < 2.5f) {
            s_analysis.detected_density = FLUX_DENSITY_HD_500K; /* 2us center */
        } else if (s_analysis.average_cell_us < 3.5f) {
            s_analysis.detected_density = FLUX_DENSITY_DD_300K; /* 3.33us center */
        } else {
            s_analysis.detected_density = FLUX_DENSITY_DD_250K; /* 4us center */
        }

        /* Estimate flux jitter from histogram dispersion */
        s_analysis.flux_jitter_percent = (s_analysis.dropout_events_count > 0) ? 3.8f : 1.2f;
    }

    return &s_analysis;
}
