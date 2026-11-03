/**
 * @file    main.c
 * @brief   Retro-Diag FDD Master Tester Main Firmware Entry Point
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 * 
 * Hardware: STM32F407VET6 (LQFP-100, 168 MHz)
 * PCB Design: FDD-Test-Board Rev 1.0 (KiCad 9.0 Validated)
 */

#include "bsp_fdd_pins.h"
#include "bsp_fdd_gpio.h"
#include "fdd_power_monitor.h"
#include "fdd_motion.h"
#include "fdd_timing_capture.h"
#include "cli_console.h"
#include "ui_panel.h"
#include "fdd_nvram.h"
#include "fdd_analog_scope.h"
#include "fdd_flux_analyzer.h"
#include "fdd_burnin.h"

#include <stdint.h>
#include <stdbool.h>

/* Millisecond tick emulation / wrapper */
static volatile uint32_t s_systick_counter_ms = 0;

uint32_t hal_get_tick_ms(void) {
    return s_systick_counter_ms;
}

void hal_delay_ms(uint32_t ms) {
    uint32_t start = hal_get_tick_ms();
    while ((hal_get_tick_ms() - start) < ms) {
        /* Wait */
    }
}

/* System Tick Interrupt Hook (Called at 1 kHz) */
void SysTick_Handler_Hook(void) {
    s_systick_counter_ms++;
}

int main(void) {
    /*
     * 1. CRITICAL: Hardware Fail-Safe Initialization
     * Disarms all power rails and puts all bus lines in high-impedance / idle state
     */
    bsp_fdd_init();

    /*
     * 2. LED Hardware Self-Test (Sequence through panel LEDs on startup)
     */
    bsp_led_self_test(70);

    /*
     * 3. Subsystem Initialization
     */
    fdd_nvram_init();
    fdd_power_monitor_init();
    fdd_motion_init(80, STEP_RATE_3MS);
    fdd_timing_capture_init();
    fdd_analog_scope_init();
    fdd_flux_analyzer_init();
    cli_console_init();
    ui_panel_init();

    /* System Ready Indicator */
    bsp_led_ready(true);
    bsp_buzzer_beep(2000, 80);

    uint32_t last_heartbeat_ms = 0;
    uint32_t last_adc_poll_ms  = 0;
    uint32_t last_ui_update_ms = 0;

    /*
     * 4. Main Diagnostic Superloop
     */
    while (1) {
        uint32_t now = hal_get_tick_ms();

        /*
         * Safety Task 1: Check Current Sensing & Overcurrent E-Fuse (~1 kHz)
         */
        if ((now - last_adc_poll_ms) >= 1) {
            last_adc_poll_ms = now;
            fdd_power_check_faults();
        }

        /*
         * Task 2: Front Panel Graphical UI & Rotary Encoder (~50 Hz)
         */
        if ((now - last_ui_update_ms) >= 20) {
            uint32_t delta = now - last_ui_update_ms;
            last_ui_update_ms = now;
            ui_panel_update(delta);
        }

        /*
         * Task 3: Spindle Speed & Index Timing Watchdog (~100 Hz)
         */
        fdd_timing_update();

        /*
         * Task 4: Heartbeat & Status LED Update (1 Hz)
         */
        if ((now - last_heartbeat_ms) >= 1000) {
            last_heartbeat_ms = now;

            const fdd_power_telemetry_t *pwr = fdd_power_get_telemetry();
            bool has_fault = pwr->fault_tripped[PWR_RAIL_24V] ||
                             pwr->fault_tripped[PWR_RAIL_12V] ||
                             pwr->fault_tripped[PWR_RAIL_5V];

            if (!has_fault && ui_panel_get_state() != UI_STATE_BOOT) {
                bsp_led_ready(true);
            }
        }
    }

    return 0;
}
