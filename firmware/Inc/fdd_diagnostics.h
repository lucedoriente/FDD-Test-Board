/**
 * @file    fdd_diagnostics.h
 * @brief   Automated Floppy Drive Diagnostic Suite & Expert Repair Advisor with OEM Database
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 */

#ifndef FDD_DIAGNOSTICS_H
#define FDD_DIAGNOSTICS_H

#include "bsp_fdd_pins.h"
#include "fdd_power_monitor.h"
#include "fdd_motion.h"
#include "fdd_timing_capture.h"

#ifdef __cplusplus
extern "C" {
#endif

/* Supported Drive Models in OEM Database */
typedef enum {
    DRIVE_MODEL_AUTO_DETECT = 0,
    DRIVE_MODEL_GENERIC_350_HD,     /**< Standard 3.5" 1.44MB Direct-Drive BLDC (300 RPM) */
    DRIVE_MODEL_SONY_MPF920,        /**< Sony MPF-920 3.5" (SMD Electrolytic notes) */
    DRIVE_MODEL_TEAC_FD235HF,       /**< TEAC FD-235HF 3.5" */
    DRIVE_MODEL_CHINON_FB354,       /**< Chinon FB-354 (Amiga 3.5" DD 880KB, Pin 34 RDY, Pin 2 CHNG) */
    DRIVE_MODEL_CHINON_FB357A,      /**< Chinon FB-357A/FZ-357A (Amiga 3.5" HD 1.76MB, 150 RPM HD mode) */
    DRIVE_MODEL_TANDON_TM100_2A,    /**< Tandon TM100-2A 5.25" 360KB (300 RPM, Belt, Trimmer R4) */
    DRIVE_MODEL_TEAC_FD55GFR,       /**< TEAC FD-55GFR 5.25" 1.2MB/360K Dual-Speed (360 RPM) */
    DRIVE_MODEL_SHUGART_SA400,      /**< Shugart SA400 Minifloppy (35 Track, Archimedes spiral) */
    DRIVE_MODEL_SHUGART_SA800,      /**< Shugart SA800 8" Single-Sided (360 RPM AC, Solenoid 24V) */
    DRIVE_MODEL_SHUGART_SA850,      /**< Shugart SA850 8" Double-Sided (360 RPM AC, Solenoid 24V) */
    DRIVE_MODEL_AMSTRAD_EME156,     /**< Matsushita EME-156 3" Compact Floppy (Black goo belt) */
    DRIVE_MODEL_APPLE_DISK_II,      /**< Apple II Disk II (Shugart SA390, 4-phase, no Trk0) */
    DRIVE_MODEL_COMMODORE_1541,     /**< Commodore 1541 Mechanics (4-phase, mechanical stop homing) */
    DRIVE_MODEL_ATARI_ST_EPSON,     /**< Atari ST (Epson SMD-380 / Chinon 720KB/1.44M, 300 RPM, DS0) */
    DRIVE_MODEL_JAPAN_3MODE,        /**< Japanese 3-Mode (TEAC FD-235HG PC-98 1.2MB @ 360 RPM) */
    DRIVE_MODEL_APPLE_MAC_SUPERDRIVE, /**< Apple Mac SuperDrive (Sony MP-F75W Auto-Eject Motor) */
    DRIVE_MODEL_COUNT
} fdd_drive_model_t;

/* Specification Profile for each Model */
typedef struct {
    fdd_drive_model_t   model_id;
    const char         *display_name;
    const char         *size_str;
    float               nominal_rpm;
    float               rpm_tolerance_pct;
    uint8_t             max_cylinders;
    fdd_step_rate_t     recommended_step_rate;
    fdd_motion_mode_t   motion_mode;
    bool                requires_24v;
    bool                has_track0_sensor;
    const char         *oem_manual_url;
} fdd_model_spec_t;

/* Test Stage Result Codes */
typedef enum {
    TEST_RESULT_PASS = 0,
    TEST_RESULT_WARN,
    TEST_RESULT_FAIL
} test_result_t;

/* Failure / Advisory Category */
typedef enum {
    FAULT_NONE = 0,
    FAULT_SHORT_CIRCUIT_24V,
    FAULT_SHORT_CIRCUIT_12V,
    FAULT_SHORT_CIRCUIT_5V,
    FAULT_QUIESCENT_CURRENT_HIGH,
    FAULT_SPINDLE_STALL_NO_ROTATION,
    FAULT_SPINDLE_SPEED_TOO_SLOW,
    FAULT_SPINDLE_SPEED_TOO_FAST,
    FAULT_SPINDLE_HIGH_WOW_FLUTTER,
    FAULT_INDEX_SENSOR_DEAD,
    FAULT_TRACK00_SENSOR_STUCK_OR_BLIND,
    FAULT_STEPPER_MECHANICAL_FRICTION,
    FAULT_STEPPER_STEP_LOSS,
    FAULT_WRITE_PROTECT_SWITCH_DEFECT,
    FAULT_DISK_CHANGE_SWITCH_DEFECT,
    FAULT_PIN34_NOT_READY,
    FAULT_AMIGA_LEAKY_CAPS,
    FAULT_MAC_AUTO_EJECT_CAUTION,
    FAULT_ATARI_DS0_MISCONFIG
} fdd_fault_code_t;

/* Individual Sub-Test Record */
typedef struct {
    const char         *test_name;
    test_result_t       result;
    float               measured_val;
    float               nominal_val;
    float               tolerance_val;
    const char         *unit_str;
    fdd_fault_code_t    fault_code;
    char                summary[128];
} fdd_subtest_record_t;

#define MAX_DIAG_SUBTESTS   10U

/* Overall Diagnostic Report Structure */
typedef struct {
    fdd_drive_model_t       selected_model;
    const fdd_model_spec_t *spec;
    uint32_t                test_duration_ms;
    test_result_t           overall_status;
    uint8_t                 subtest_count;
    fdd_subtest_record_t    subtests[MAX_DIAG_SUBTESTS];
    uint8_t                 fault_count;
    uint8_t                 warn_count;
} fdd_diagnostic_report_t;

/* Diagnostics API */
void fdd_diagnostics_init(void);

const fdd_model_spec_t *fdd_diagnostics_get_model_spec(fdd_drive_model_t model);
fdd_drive_model_t fdd_diagnostics_auto_probe(void);

const fdd_diagnostic_report_t *fdd_diagnostics_run_full(
    fdd_drive_model_t model,
    void (*progress_cb)(uint8_t percent, const char *stage),
    bool (*abort_cb)(void)
);

void fdd_diagnostics_print_report(const fdd_diagnostic_report_t *report);
const char *fdd_diagnostics_get_repair_guide(fdd_drive_model_t model, fdd_fault_code_t code);

#ifdef __cplusplus
}
#endif

#endif /* FDD_DIAGNOSTICS_H */
