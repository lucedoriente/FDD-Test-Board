/**
 * @file    fdd_flux_analyzer.h
 * @brief   Magnetic Flux Transition Capture & MFM Surface Analysis Engine
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 */

#ifndef FDD_FLUX_ANALYZER_H
#define FDD_FLUX_ANALYZER_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

#define FLUX_HISTOGRAM_BINS     64U
#define FLUX_SAMPLE_BUFFER_SIZE 1024U

typedef enum {
    FLUX_DENSITY_UNKNOWN = 0,
    FLUX_DENSITY_DD_250K,       /**< Standard 3.5" 720KB / 5.25" 360KB (4us, 6us, 8us) */
    FLUX_DENSITY_DD_300K,       /**< 5.25" 360KB in 1.2M drive (3.33us, 5.0us, 6.67us) */
    FLUX_DENSITY_HD_500K,       /**< Standard 3.5" 1.44MB / 5.25" 1.2MB (2us, 3us, 4us) */
    FLUX_DENSITY_ED_1M          /**< Extra Density 2.88MB (1us, 1.5us, 2us) */
} fdd_flux_density_t;

typedef struct {
    uint32_t            total_flux_transitions;   /**< Total pulses captured per track revolution */
    float               average_cell_us;          /**< Center MFM cell duration in microseconds */
    float               flux_jitter_percent;      /**< Peak-to-peak jitter percentage */
    fdd_flux_density_t  detected_density;         /**< Classified recording density */
    uint16_t            dropout_events_count;     /**< Missing flux transitions / dropouts */
    uint16_t            histogram[FLUX_HISTOGRAM_BINS]; /**< 0.25us bin resolution histogram (0..16us) */
} fdd_flux_analysis_t;

/**
 * @brief Initializes TIM4_CH2 Input Capture on PB7 for raw READ_DATA sampling
 */
void fdd_flux_analyzer_init(void);

/**
 * @brief Captures raw magnetic flux transitions over one complete disk revolution (Index to Index)
 * @param side Head side (0 or 1)
 * @param track Cylinder to inspect
 * @return Pointer to analyzed flux metrics
 */
const fdd_flux_analysis_t *fdd_flux_analyzer_capture_revolution(uint8_t side, uint8_t track);

#ifdef __cplusplus
}
#endif

#endif /* FDD_FLUX_ANALYZER_H */
