/**
 * @file    bsp_fdd_pins.h
 * @brief   Hardware Pinout & Low-Level Register Definitions for Retro-Diag FDD Master Tester
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 * 
 * Hardware Target: STM32F407VET6 (LQFP-100, 168 MHz)
 * PCB Design: FDD-Test-Board Rev 1.0 + FDD_UI_Panel Rev 1.0 (KiCad 9.0)
 */

#ifndef BSP_FDD_PINS_H
#define BSP_FDD_PINS_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ========================================================================== */
/* 1. POWER RAILS & CURRENT SENSING PINOUT                                    */
/* ========================================================================== */

/* Power Rails Enable Pins (Active HIGH) */
#define EN_24V_PORT             GPIOC
#define EN_24V_PIN              GPIO_PIN_4         /* Pin 33 */

#define EN_12V_PORT             GPIOC
#define EN_12V_PIN              GPIO_PIN_5         /* Pin 34 */

#define EN_5V_PORT              GPIOB
#define EN_5V_PIN               GPIO_PIN_0         /* Pin 35 */

/* Analog Current Sensing (INA180A1 with Gain = 20 V/V, Shunt = 0.05 Ohm) */
#define ISENSE_24V_PORT         GPIOC
#define ISENSE_24V_PIN          GPIO_PIN_0         /* Pin 15, ADC1_IN10 */
#define ISENSE_24V_ADC_CH       ADC_CHANNEL_10

#define ISENSE_12V_PORT         GPIOC
#define ISENSE_12V_PIN          GPIO_PIN_1         /* Pin 16, ADC1_IN11 */
#define ISENSE_12V_ADC_CH       ADC_CHANNEL_11

#define ISENSE_5V_PORT          GPIOC
#define ISENSE_5V_PIN           GPIO_PIN_2         /* Pin 17, ADC1_IN12 */
#define ISENSE_5V_ADC_CH        ADC_CHANNEL_12

/* Shunt & Amplifier Parameters */
#define INA180_GAIN_V_PER_V     20.0f
#define SHUNT_RESISTOR_OHM      0.050f             /* 50 mOhm */
#define VREF_VOLTAGE_V          3.30f
#define ADC_MAX_COUNT           4095.0f

/* ========================================================================== */
/* 2. FDD BUS CONTROL OUTPUTS (Driven via 7406 Open-Collector Inverters)       */
/* ========================================================================== */
/*
 * Inversion Logic Note:
 * The 7406 is an inverting Open-Collector buffer.
 * - STM32 LOW (0V)  -> 7406 Output HIGH-Z (Pulled HIGH by drive pull-up: INACTIVE)
 * - STM32 HIGH (3.3V)-> 7406 Output LOW (Pulls drive line to GND: ACTIVE)
 *
 * Therefore, to assert an active-low floppy signal on the bus, set STM32 pin HIGH.
 * At power-on, all pins MUST be set to LOW to keep the drive completely idle.
 */

#define FDD_READY_PORT          GPIOD
#define FDD_READY_PIN           GPIO_PIN_0         /* Pin 81 */

#define FDD_STEP_PORT           GPIOD
#define FDD_STEP_PIN            GPIO_PIN_1         /* Pin 82 */

#define FDD_DIR_PORT            GPIOD
#define FDD_DIR_PIN             GPIO_PIN_2         /* Pin 83: HIGH=In (Cylinder++), LOW=Out (Cylinder--) */

#define FDD_MOTOR_ON_PORT       GPIOD
#define FDD_MOTOR_ON_PIN        GPIO_PIN_3         /* Pin 84 */

#define FDD_DRV_SEL0_PORT       GPIOD
#define FDD_DRV_SEL0_PIN        GPIO_PIN_4         /* Pin 85 */

#define FDD_DRV_SEL1_PORT       GPIOD
#define FDD_DRV_SEL1_PIN        GPIO_PIN_5         /* Pin 86 */

#define FDD_SIDE1_SEL_PORT      GPIOD
#define FDD_SIDE1_SEL_PIN       GPIO_PIN_6         /* Pin 87: HIGH=Side 1, LOW=Side 0 */

#define FDD_WRITE_GATE_PORT     GPIOD
#define FDD_WRITE_GATE_PIN      GPIO_PIN_7         /* Pin 88 */

#define FDD_WRITE_DATA_PORT     GPIOB
#define FDD_WRITE_DATA_PIN      GPIO_PIN_9         /* Pin 96 */

/* ========================================================================== */
/* 3. FDD BUS SENSOR INPUTS (Conditioned via 74HC14 Schmitt Trigger Inverters) */
/* ========================================================================== */
/*
 * Inversion Logic Note:
 * The 74HC14 inverts the incoming signal.
 * - Drive asserts signal (LOW, 0V) -> 74HC14 Output is HIGH (3.3V) at STM32.
 * - Drive idle (HIGH, 5V)          -> 74HC14 Output is LOW (0V) at STM32.
 *
 * Therefore, a HIGH reading on these STM32 inputs represents ACTIVE condition.
 */

#define FDD_TRACK00_PORT        GPIOB
#define FDD_TRACK00_PIN         GPIO_PIN_3         /* Pin 89: 1 = At Track 00 */

#define FDD_WRITE_PROTECT_PORT  GPIOB
#define FDD_WRITE_PROTECT_PIN   GPIO_PIN_4         /* Pin 90: 1 = Disk is Write Protected */

#define FDD_DISK_CHANGE_PORT    GPIOB
#define FDD_DISK_CHANGE_PIN     GPIO_PIN_5         /* Pin 91: 1 = Disk changed / Door opened */

#define FDD_INDEX_PORT          GPIOB
#define FDD_INDEX_PIN           GPIO_PIN_6         /* Pin 92: TIM4_CH1 Input Capture */

#define FDD_READ_DATA_PORT      GPIOB
#define FDD_READ_DATA_PIN       GPIO_PIN_7         /* Pin 93: TIM4_CH2 Input Capture */

/* ========================================================================== */
/* 4. DIRECT 4-PHASE UNIPOLAR STEPPER DRIVE (Apple II / C1541 via ULN2003A)    */
/* ========================================================================== */
/*
 * ULN2003A Darlington array:
 * - STM32 HIGH (3.3V) -> Darlington conducts -> Coil energized to GND.
 * - STM32 LOW (0V)   -> Darlington OFF       -> Coil unenergized.
 */
#define APPLE_STEPPER_PORT      GPIOE
#define APPLE_PH0_PIN           GPIO_PIN_0         /* Pin 97 */
#define APPLE_PH1_PIN           GPIO_PIN_1         /* Pin 98 */
#define APPLE_PH2_PIN           GPIO_PIN_2         /* Pin 1  */
#define APPLE_PH3_PIN           GPIO_PIN_3         /* Pin 2  */
#define APPLE_PH_ALL_MASK       (GPIO_PIN_0 | GPIO_PIN_1 | GPIO_PIN_2 | GPIO_PIN_3)

/* ========================================================================== */
/* 5. DAUGHTERBOARD UI PANEL & STATUS LEDS (J15 Connector)                    */
/* ========================================================================== */

/* Physical Pushbuttons (Active LOW, internal/external pull-ups) */
#define BTN_RUN_PORT            GPIOB
#define BTN_RUN_PIN             GPIO_PIN_12        /* Pin 51 */

#define BTN_BACK_PORT           GPIOB
#define BTN_BACK_PIN            GPIO_PIN_13        /* Pin 52 */

#define ENC_SW_PORT             GPIOC
#define ENC_SW_PIN              GPIO_PIN_13        /* Pin 7 */

#define ENC_A_PORT              GPIOA
#define ENC_A_PIN               GPIO_PIN_0         /* Pin 23, EXTI0 */

#define ENC_B_PORT              GPIOA
#define ENC_B_PIN               GPIO_PIN_15        /* Pin 77, EXTI15 */

/* Status Indicators (Active HIGH) */
#define LED_READY_PORT          GPIOC
#define LED_READY_PIN           GPIO_PIN_6         /* Pin 63 (Green) */

#define LED_BUSY_PORT           GPIOC
#define LED_BUSY_PIN            GPIO_PIN_7         /* Pin 64 (Yellow) */

#define LED_FAULT_PORT          GPIOC
#define LED_FAULT_PIN           GPIO_PIN_8         /* Pin 65 (Red) */

#define LED_INDEX_PORT          GPIOC
#define LED_INDEX_PIN           GPIO_PIN_9         /* Pin 66 (Blue) */

#define LED_READ_PORT           GPIOA
#define LED_READ_PIN            GPIO_PIN_8         /* Pin 67 (Orange) */

/* Audible Buzzer (TIM4_CH3 or GPIO) */
#define BUZZER_PORT             GPIOB
#define BUZZER_PIN              GPIO_PIN_8         /* Pin 95 */

/* ========================================================================== */
/* 6. COMMUNICATIONS & DISPLAY INTERFACES                                    */
/* ========================================================================== */

/* SPI IPS Graphic Display (ST7735S / ST7789 via SPI1) */
#define LCD_SPI_INSTANCE        SPI1
#define LCD_SCK_PORT            GPIOA
#define LCD_SCK_PIN             GPIO_PIN_5         /* Pin 30, SPI1_SCK */
#define LCD_MOSI_PORT           GPIOA
#define LCD_MOSI_PIN            GPIO_PIN_7         /* Pin 32, SPI1_MOSI */
#define LCD_CS_PORT             GPIOB
#define LCD_CS_PIN              GPIO_PIN_0         /* Pin 35 */
#define LCD_DC_PORT             GPIOB
#define LCD_DC_PIN              GPIO_PIN_1         /* Pin 36 (0=Command, 1=Data) */
#define LCD_RST_PORT            GPIOC
#define LCD_RST_PIN             GPIO_PIN_4         /* Pin 33 (Reset) */
#define LCD_BLK_PORT            GPIOC
#define LCD_BLK_PIN             GPIO_PIN_5         /* Pin 34 (Backlight) */

/* Analog Inputs for Head Scope (Cat's Eye TP1 / TP2 on ADC1) */
#define SCOPE_TP1_PORT          GPIOA
#define SCOPE_TP1_PIN           GPIO_PIN_1         /* Pin 24, ADC1_IN1 */
#define SCOPE_TP1_ADC_CH        ADC_CHANNEL_1
#define SCOPE_TP2_PORT          GPIOA
#define SCOPE_TP2_PIN           GPIO_PIN_2         /* Pin 25, ADC1_IN2 */
#define SCOPE_TP2_ADC_CH        ADC_CHANNEL_2

/* Display / HMI Serial Port (J5: +5V, GND, TX, RX) */
#define HMI_UART_INSTANCE       USART1
#define HMI_UART_PORT           GPIOA
#define HMI_UART_TX_PIN         GPIO_PIN_9         /* Pin 68 */
#define HMI_UART_RX_PIN         GPIO_PIN_10        /* Pin 69 */
#define HMI_UART_BAUDRATE       115200U

/* Native USB Full-Speed OTG Port (J6: USB-C) */
#define USB_FS_PORT             GPIOA
#define USB_FS_DM_PIN           GPIO_PIN_11        /* Pin 70 */
#define USB_FS_DP_PIN           GPIO_PIN_12        /* Pin 71 */

/* SWD Debug Header (J7) */
#define SWD_PORT                GPIOA
#define SWD_DIO_PIN             GPIO_PIN_13        /* Pin 72 */
#define SWD_CLK_PIN             GPIO_PIN_14        /* Pin 76 */

#ifdef __cplusplus
}
#endif

#endif /* BSP_FDD_PINS_H */
