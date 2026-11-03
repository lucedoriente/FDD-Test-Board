/**
 * @file    bsp_fdd_gpio.c
 * @brief   Board Support Package GPIO Implementation for Retro-Diag FDD Master Tester
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 */

#include "bsp_fdd_gpio.h"

/* Standard STM32 / CMSIS hardware definitions fallback */
#if defined(STM32F407xx) || defined(USE_HAL_DRIVER)
    #include "stm32f4xx_hal.h"
#else
    /* Bare-metal register emulation / standalone mockup for verification */
    typedef struct {
        volatile uint32_t MODER;
        volatile uint32_t OTYPER;
        volatile uint32_t OSPEEDR;
        volatile uint32_t PUPDR;
        volatile uint32_t IDR;
        volatile uint32_t ODR;
        volatile uint32_t BSRR;
        volatile uint32_t LCKR;
        volatile uint32_t AFR[2];
    } GPIO_TypeDef;

    #define PERIPH_BASE           0x40000000UL
    #define AHB1PERIPH_BASE       (PERIPH_BASE + 0x00020000UL)
    #define GPIOA_BASE            (AHB1PERIPH_BASE + 0x0000UL)
    #define GPIOB_BASE            (AHB1PERIPH_BASE + 0x0400UL)
    #define GPIOC_BASE            (AHB1PERIPH_BASE + 0x0800UL)
    #define GPIOD_BASE            (AHB1PERIPH_BASE + 0x0C00UL)
    #define GPIOE_BASE            (AHB1PERIPH_BASE + 0x1000UL)

    #define GPIOA                 ((GPIO_TypeDef *) GPIOA_BASE)
    #define GPIOB                 ((GPIO_TypeDef *) GPIOB_BASE)
    #define GPIOC                 ((GPIO_TypeDef *) GPIOC_BASE)
    #define GPIOD                 ((GPIO_TypeDef *) GPIOD_BASE)
    #define GPIOE                 ((GPIO_TypeDef *) GPIOE_BASE)

    #define GPIO_PIN_0            (1U << 0)
    #define GPIO_PIN_1            (1U << 1)
    #define GPIO_PIN_2            (1U << 2)
    #define GPIO_PIN_3            (1U << 3)
    #define GPIO_PIN_4            (1U << 4)
    #define GPIO_PIN_5            (1U << 5)
    #define GPIO_PIN_6            (1U << 6)
    #define GPIO_PIN_7            (1U << 7)
    #define GPIO_PIN_8            (1U << 8)
    #define GPIO_PIN_9            (1U << 9)
    #define GPIO_PIN_10           (1U << 10)
    #define GPIO_PIN_11           (1U << 11)
    #define GPIO_PIN_12           (1U << 12)
    #define GPIO_PIN_13           (1U << 13)
    #define GPIO_PIN_14           (1U << 14)
    #define GPIO_PIN_15           (1U << 15)

    /* DWT cycle counter emulation / timer */
    static inline void delay_cycles(uint32_t cycles) {
        while(cycles--) { __asm__ volatile("nop"); }
    }
    #define DWT_DELAY_US(us)      delay_cycles((us) * 168 / 4)
    #define HAL_Delay(ms)         delay_cycles((ms) * 168000 / 4)
#endif

/* Low-level bit set/clear helpers */
static inline void gpio_write(GPIO_TypeDef *port, uint16_t pin, bool high) {
    if (high) {
        port->BSRR = (uint32_t)pin;
    } else {
        port->BSRR = (uint32_t)pin << 16U;
    }
}

static inline bool gpio_read(GPIO_TypeDef *port, uint16_t pin) {
    return (port->IDR & pin) != 0U;
}

/* ========================================================================== */
/* Power Rails Control Functions                                              */
/* ========================================================================== */

void bsp_pwr_set_24v(bool enable) {
    gpio_write(EN_24V_PORT, EN_24V_PIN, enable);
}

void bsp_pwr_set_12v(bool enable) {
    gpio_write(EN_12V_PORT, EN_12V_PIN, enable);
}

void bsp_pwr_set_5v(bool enable) {
    gpio_write(EN_5V_PORT, EN_5V_PIN, enable);
}

void bsp_pwr_all_off(void) {
    gpio_write(EN_24V_PORT, EN_24V_PIN, false);
    gpio_write(EN_12V_PORT, EN_12V_PIN, false);
    gpio_write(EN_5V_PORT, EN_5V_PIN, false);
}

/* ========================================================================== */
/* Status LEDs Control Functions                                              */
/* ========================================================================== */

void bsp_led_ready(bool on) {
    gpio_write(LED_READY_PORT, LED_READY_PIN, on);
}

void bsp_led_busy(bool on) {
    gpio_write(LED_BUSY_PORT, LED_BUSY_PIN, on);
}

void bsp_led_fault(bool on) {
    gpio_write(LED_FAULT_PORT, LED_FAULT_PIN, on);
}

void bsp_led_index(bool on) {
    gpio_write(LED_INDEX_PORT, LED_INDEX_PIN, on);
}

void bsp_led_read(bool on) {
    gpio_write(LED_READ_PORT, LED_READ_PIN, on);
}

void bsp_led_all_off(void) {
    bsp_led_ready(false);
    bsp_led_busy(false);
    bsp_led_fault(false);
    bsp_led_index(false);
    bsp_led_read(false);
}

void bsp_led_self_test(uint32_t delay_ms) {
    bsp_led_all_off();
    
    bsp_led_ready(true);
    HAL_Delay(delay_ms);
    bsp_led_ready(false);

    bsp_led_busy(true);
    HAL_Delay(delay_ms);
    bsp_led_busy(false);

    bsp_led_fault(true);
    HAL_Delay(delay_ms);
    bsp_led_fault(false);

    bsp_led_index(true);
    HAL_Delay(delay_ms);
    bsp_led_index(false);

    bsp_led_read(true);
    HAL_Delay(delay_ms);
    bsp_led_read(false);
}

/* ========================================================================== */
/* Buzzer Control                                                             */
/* ========================================================================== */

void bsp_buzzer_beep(uint16_t freq_hz, uint16_t duration_ms) {
    (void)freq_hz;
    /* Basic bit-toggle beep until Timer PWM is initialized */
    if (duration_ms > 0) {
        gpio_write(BUZZER_PORT, BUZZER_PIN, true);
        HAL_Delay(duration_ms);
        gpio_write(BUZZER_PORT, BUZZER_PIN, false);
    }
}

/* ========================================================================== */
/* Floppy Drive Bus Control Functions (7406 Open-Collector Inverters)         */
/* ========================================================================== */

void bsp_fdd_set_motor(bool active) {
    /* 7406 inverts: HIGH on STM32 pulls bus line to 0V (ACTIVE) */
    gpio_write(FDD_MOTOR_ON_PORT, FDD_MOTOR_ON_PIN, active);
}

void bsp_fdd_set_drive_select(uint8_t drive_num, bool active) {
    if (drive_num == 0) {
        gpio_write(FDD_DRV_SEL0_PORT, FDD_DRV_SEL0_PIN, active);
    } else if (drive_num == 1) {
        gpio_write(FDD_DRV_SEL1_PORT, FDD_DRV_SEL1_PIN, active);
    }
}

void bsp_fdd_set_side(uint8_t side) {
    /* side == 1: Side 1 selected (HIGH on STM32 -> 0V on bus) */
    /* side == 0: Side 0 selected (LOW on STM32 -> 5V on bus) */
    gpio_write(FDD_SIDE1_SEL_PORT, FDD_SIDE1_SEL_PIN, (side == 1));
}

void bsp_fdd_set_direction(bool inward) {
    /* inward = true: Step towards center/higher cylinder (STM32 HIGH -> 0V on bus) */
    /* inward = false: Step outward towards Track 0 (STM32 LOW -> 5V on bus) */
    gpio_write(FDD_DIR_PORT, FDD_DIR_PIN, inward);
}

void bsp_fdd_pulse_step(uint16_t pulse_us) {
    /* Step pulse is Active LOW on floppy interface */
    gpio_write(FDD_STEP_PORT, FDD_STEP_PIN, true);   /* Assert step (0V on bus) */
    DWT_DELAY_US(pulse_us < 2 ? 2 : pulse_us);       /* Standard minimum is 1 to 8 us */
    gpio_write(FDD_STEP_PORT, FDD_STEP_PIN, false);  /* De-assert step (5V on bus) */
}

void bsp_fdd_set_write_gate(bool active) {
    /* SAFETY CRITICAL: Only assert when deliberate write is scheduled */
    gpio_write(FDD_WRITE_GATE_PORT, FDD_WRITE_GATE_PIN, active);
}

/* ========================================================================== */
/* Floppy Drive Sensor Readings (74HC14 Inverters)                            */
/* ========================================================================== */

bool bsp_fdd_is_track00(void) {
    /* 74HC14 inverts: drive asserting Track0 (0V) produces 3.3V (HIGH) at STM32 */
    return gpio_read(FDD_TRACK00_PORT, FDD_TRACK00_PIN);
}

bool bsp_fdd_is_write_protected(void) {
    return gpio_read(FDD_WRITE_PROTECT_PORT, FDD_WRITE_PROTECT_PIN);
}

bool bsp_fdd_is_disk_changed(void) {
    return gpio_read(FDD_DISK_CHANGE_PORT, FDD_DISK_CHANGE_PIN);
}

bool bsp_fdd_get_index_raw(void) {
    return gpio_read(FDD_INDEX_PORT, FDD_INDEX_PIN);
}

/* ========================================================================== */
/* Pushbuttons & Encoder Physical Readings                                    */
/* ========================================================================== */

bool bsp_btn_run_pressed(void) {
    /* Buttons are Active LOW (pull-up to 3.3V) */
    return !gpio_read(BTN_RUN_PORT, BTN_RUN_PIN);
}

bool bsp_btn_back_pressed(void) {
    return !gpio_read(BTN_BACK_PORT, BTN_BACK_PIN);
}

bool bsp_btn_enc_pressed(void) {
    return !gpio_read(ENC_SW_PORT, ENC_SW_PIN);
}

/* ========================================================================== */
/* Complete Fail-Safe Hardware Initialization                                 */
/* ========================================================================== */

void bsp_fdd_init(void) {
    /*
     * 1. POWER RAILS: Disarm immediately (All E-Fuses OFF)
     */
    bsp_pwr_all_off();

    /*
     * 2. FDD BUS SIGNALS: De-assert all Open-Collector drivers (All 0V on STM32)
     */
    gpio_write(FDD_READY_PORT, FDD_READY_PIN, false);
    gpio_write(FDD_STEP_PORT, FDD_STEP_PIN, false);
    gpio_write(FDD_DIR_PORT, FDD_DIR_PIN, false);
    gpio_write(FDD_MOTOR_ON_PORT, FDD_MOTOR_ON_PIN, false);
    gpio_write(FDD_DRV_SEL0_PORT, FDD_DRV_SEL0_PIN, false);
    gpio_write(FDD_DRV_SEL1_PORT, FDD_DRV_SEL1_PIN, false);
    gpio_write(FDD_SIDE1_SEL_PORT, FDD_SIDE1_SEL_PIN, false);
    gpio_write(FDD_WRITE_GATE_PORT, FDD_WRITE_GATE_PIN, false);
    gpio_write(FDD_WRITE_DATA_PORT, FDD_WRITE_DATA_PIN, false);

    /*
     * 3. DIRECT STEPPER 4-PHASE: Turn off all Darlington stages (Zero power)
     */
    gpio_write(APPLE_STEPPER_PORT, APPLE_PH0_PIN, false);
    gpio_write(APPLE_STEPPER_PORT, APPLE_PH1_PIN, false);
    gpio_write(APPLE_STEPPER_PORT, APPLE_PH2_PIN, false);
    gpio_write(APPLE_STEPPER_PORT, APPLE_PH3_PIN, false);

    /*
     * 4. LEDS & BUZZER: Turn all off
     */
    bsp_led_all_off();
    gpio_write(BUZZER_PORT, BUZZER_PIN, false);
}
