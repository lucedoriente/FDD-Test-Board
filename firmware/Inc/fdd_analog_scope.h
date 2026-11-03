/**
 * @file    fdd_analog_scope.h
 * @brief   Real-Time ADC Head Alignment Scope (Dysan 224/2A Cat's Eye Dual-Lobe Engine)
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 */

#ifndef FDD_ANALOG_SCOPE_H
#define FDD_ANALOG_SCOPE_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

#define SCOPE_BUFFER_SAMPLES    512U

typedef struct {
    float    lobe_a_mv_vpp;      /**< Peak-to-peak amplitude of 125 kHz Lobe A in mV */
    float    lobe_b_mv_vpp;      /**< Peak-to-peak amplitude of 250 kHz Lobe B in mV */
    float    symmetry_percent;   /**< Radial alignment symmetry percentage (100% = ideal) */
    float    azimuth_arcmin;     /**< Estimated azimuth misalignment in arcminutes */
    uint16_t raw_buffer_a[SCOPE_BUFFER_SAMPLES];
    uint16_t raw_buffer_b[SCOPE_BUFFER_SAMPLES];
} fdd_cat_eye_metrics_t;

/**
 * @brief Initializes ADC1 channels (IN1, IN2) for TP1 and TP2 test point sampling
 */
void fdd_analog_scope_init(void);

/**
 * @brief Triggers rapid DMA burst sample of Head RF signals and computes Cat's Eye metrics
 * @param head_side 0 for Bottom Head (Side 0), 1 for Top Head (Side 1)
 * @return Pointer to computed alignment metrics structure
 */
const fdd_cat_eye_metrics_t *fdd_analog_scope_sample(uint8_t head_side);

#ifdef __cplusplus
}
#endif

#endif /* FDD_ANALOG_SCOPE_H */
