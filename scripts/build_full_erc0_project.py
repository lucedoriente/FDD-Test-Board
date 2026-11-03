import os
import sys

scripts_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts"
sys.path.append(scripts_dir)
from generate_clean_erc0_fdd_final import *

# ==============================================================================
# SHEET 2: MCU CORE & ANALOG FRONT-END
# ==============================================================================
components_s2 = [
    # U5: STM32F407VET6
    {"lib": "MCU_ST_STM32F4", "sym": "STM32F407VETx", "ref": "U5", "val": "STM32F407VET6", "fp": "Package_QFP:LQFP-100_14x14mm_P0.5mm", "x": 190.5, "y": 140.0, "unit": 1},
    
    # U6: AMS1117-3.3 Linear Regulator (+5V_REG -> +3.3V)
    {"lib": "Regulator_Linear", "sym": "AMS1117-3.3", "ref": "U6", "val": "AMS1117-3.3", "fp": "Package_TO_SOT_SMD:SOT-223-3_TabPin2", "x": 48.26, "y": 45.0, "unit": 1},
    {"lib": "Device", "sym": "C", "ref": "C1", "val": "10uF", "fp": "Capacitor_SMD:C_0805_2012Metric", "x": 25.4, "y": 45.0, "unit": 1},
    {"lib": "Device", "sym": "C", "ref": "C2", "val": "22uF", "fp": "Capacitor_SMD:C_0805_2012Metric", "x": 76.2, "y": 45.0, "unit": 1},

    # USB-C Interface (lateral connector to PC)
    {"lib": "Connector", "sym": "USB_C_Receptacle_USB2.0_16P", "ref": "J6", "val": "USB_C_PC", "fp": "Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12", "x": 48.26, "y": 95.0, "unit": 1},
    {"lib": "Power_Protection", "sym": "USBLC6-2SC6", "ref": "D1", "val": "USBLC6-2SC6", "fp": "Package_TO_SOT_SMD:SOT-23-6", "x": 90.0, "y": 95.0, "unit": 1},
    {"lib": "Device", "sym": "D_Schottky", "ref": "D2", "val": "SS34", "fp": "Diode_SMD:D_SMA", "x": 90.0, "y": 120.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R4", "val": "5.1k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 30.0, "y": 115.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R5", "val": "5.1k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 30.0, "y": 130.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R6", "val": "22R", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 120.0, "y": 90.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R7", "val": "22R", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 120.0, "y": 100.0, "unit": 1},

    # HSE 8MHz Crystal
    {"lib": "Device", "sym": "Crystal_GND24", "ref": "Y1", "val": "8MHz", "fp": "Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm", "x": 48.26, "y": 160.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R1", "val": "1M", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 80.0, "y": 160.0, "unit": 1},
    {"lib": "Device", "sym": "C", "ref": "C12", "val": "22pF", "fp": "Capacitor_SMD:C_0805_2012Metric", "x": 48.26, "y": 180.0, "unit": 1},
    {"lib": "Device", "sym": "C", "ref": "C13", "val": "22pF", "fp": "Capacitor_SMD:C_0805_2012Metric", "x": 70.0, "y": 180.0, "unit": 1},

    # Reset & Boot
    {"lib": "Switch", "sym": "SW_Push", "ref": "SW1", "val": "BTN_RST", "fp": "Button_Switch_THT:SW_PUSH_6mm_H5mm", "x": 48.26, "y": 205.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R2", "val": "10k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 80.0, "y": 205.0, "unit": 1},
    {"lib": "Device", "sym": "C", "ref": "C14", "val": "100nF", "fp": "Capacitor_SMD:C_0805_2012Metric", "x": 100.0, "y": 205.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R3", "val": "10k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 80.0, "y": 225.0, "unit": 1},
    {"lib": "Connector_Generic", "sym": "Conn_01x04", "ref": "J7", "val": "SWD_PROG", "fp": "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical", "x": 48.26, "y": 245.0, "unit": 1},

    # Decoupling Caps for STM32
    {"lib": "Device", "sym": "C", "ref": "C3", "val": "100nF", "fp": "Capacitor_SMD:C_0805_2012Metric", "x": 280.0, "y": 40.0, "unit": 1},
    {"lib": "Device", "sym": "C", "ref": "C4", "val": "100nF", "fp": "Capacitor_SMD:C_0805_2012Metric", "x": 280.0, "y": 60.0, "unit": 1},
    {"lib": "Device", "sym": "C", "ref": "C5", "val": "100nF", "fp": "Capacitor_SMD:C_0805_2012Metric", "x": 280.0, "y": 80.0, "unit": 1},
    {"lib": "Device", "sym": "C", "ref": "C6", "val": "100nF", "fp": "Capacitor_SMD:C_0805_2012Metric", "x": 280.0, "y": 100.0, "unit": 1},
    {"lib": "Device", "sym": "C", "ref": "C7", "val": "100nF", "fp": "Capacitor_SMD:C_0805_2012Metric", "x": 280.0, "y": 120.0, "unit": 1},
    {"lib": "Device", "sym": "C", "ref": "C8", "val": "100nF", "fp": "Capacitor_SMD:C_0805_2012Metric", "x": 280.0, "y": 140.0, "unit": 1},
    {"lib": "Device", "sym": "C", "ref": "C9", "val": "100nF", "fp": "Capacitor_SMD:C_0805_2012Metric", "x": 280.0, "y": 160.0, "unit": 1},
    {"lib": "Device", "sym": "C", "ref": "C10", "val": "100nF", "fp": "Capacitor_SMD:C_0805_2012Metric", "x": 280.0, "y": 180.0, "unit": 1},
    {"lib": "Device", "sym": "C", "ref": "C11", "val": "2.2uF", "fp": "Capacitor_SMD:C_0805_2012Metric", "x": 280.0, "y": 200.0, "unit": 1},
    {"lib": "Device", "sym": "C", "ref": "C15", "val": "2.2uF", "fp": "Capacitor_SMD:C_0805_2012Metric", "x": 280.0, "y": 220.0, "unit": 1},

    # LMV358 Cat-Eye Front-End
    {"lib": "Amplifier_Operational", "sym": "LMV358", "ref": "U7", "val": "LMV358", "fp": "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", "x": 340.0, "y": 60.0, "unit": 1},
    {"lib": "Amplifier_Operational", "sym": "LMV358", "ref": "U7", "val": "LMV358", "fp": "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", "x": 340.0, "y": 110.0, "unit": 2},
    {"lib": "Amplifier_Operational", "sym": "LMV358", "ref": "U7", "val": "LMV358", "fp": "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", "x": 340.0, "y": 160.0, "unit": 3},
    {"lib": "Device", "sym": "R", "ref": "R8", "val": "100k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 315.0, "y": 55.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R9", "val": "100k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 315.0, "y": 65.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R10", "val": "1M", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 340.0, "y": 45.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R11", "val": "1M", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 340.0, "y": 75.0, "unit": 1},
    {"lib": "Device", "sym": "C", "ref": "C16", "val": "100nF", "fp": "Capacitor_SMD:C_0805_2012Metric", "x": 300.0, "y": 55.0, "unit": 1},
    {"lib": "Device", "sym": "C", "ref": "C17", "val": "100nF", "fp": "Capacitor_SMD:C_0805_2012Metric", "x": 300.0, "y": 65.0, "unit": 1},
    {"lib": "Device", "sym": "D_Small", "ref": "D3", "val": "1N4148", "fp": "Diode_SMD:D_SOD-123", "x": 360.0, "y": 110.0, "unit": 1},
    {"lib": "Device", "sym": "C", "ref": "C18", "val": "100nF", "fp": "Capacitor_SMD:C_0805_2012Metric", "x": 380.0, "y": 110.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R12", "val": "100k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 380.0, "y": 130.0, "unit": 1},
]

net_map_s2 = {
    # U6 (AMS1117-3.3)
    ("U6", "1"): "GND", ("U6", "2"): "+3.3V", ("U6", "3"): "+5V_REG",
    ("C1", "1"): "+5V_REG", ("C1", "2"): "GND",
    ("C2", "1"): "+3.3V", ("C2", "2"): "GND",

    # J6 (USB-C)
    ("J6", "A1"): "GND", ("J6", "B1"): "GND", ("J6", "A12"): "GND", ("J6", "B12"): "GND", ("J6", "S1"): "GND",
    ("J6", "A4"): "VBUS_USB", ("J6", "B4"): "VBUS_USB", ("J6", "A9"): "VBUS_USB", ("J6", "B9"): "VBUS_USB",
    ("J6", "A5"): "CC1_USB", ("J6", "B5"): "CC2_USB",
    ("J6", "A6"): "USB_RAW_DP", ("J6", "B6"): "USB_RAW_DP", ("J6", "A7"): "USB_RAW_DM", ("J6", "B7"): "USB_RAW_DM",
    ("R4", "1"): "CC1_USB", ("R4", "2"): "GND",
    ("R5", "1"): "CC2_USB", ("R5", "2"): "GND",
    ("D1", "1"): "USB_RAW_DM", ("D1", "2"): "GND", ("D1", "3"): "USB_RAW_DP",
    ("D1", "4"): "NC", ("D1", "5"): "VBUS_USB", ("D1", "6"): "NC",
    ("D2", "1"): "+5V_REG", ("D2", "2"): "VBUS_USB",
    ("R6", "1"): "USB_RAW_DM", ("R6", "2"): "USB_DM",
    ("R7", "1"): "USB_RAW_DP", ("R7", "2"): "USB_DP",

    # Y1 (Crystal)
    ("Y1", "1"): "OSC_IN", ("Y1", "2"): "GND", ("Y1", "3"): "OSC_OUT", ("Y1", "4"): "GND",
    ("R1", "1"): "OSC_IN", ("R1", "2"): "OSC_OUT",
    ("C12", "1"): "OSC_IN", ("C12", "2"): "GND",
    ("C13", "1"): "OSC_OUT", ("C13", "2"): "GND",

    # SW1 (Reset) & J7 (SWD)
    ("SW1", "1"): "MCU_NRST", ("SW1", "2"): "GND",
    ("R2", "1"): "MCU_NRST", ("R2", "2"): "+3.3V",
    ("C14", "1"): "MCU_NRST", ("C14", "2"): "GND",
    ("R3", "1"): "BOOT0", ("R3", "2"): "GND",
    ("J7", "1"): "+3.3V", ("J7", "2"): "SWDIO", ("J7", "3"): "SWCLK", ("J7", "4"): "GND",

    # Decoupling Caps
    ("C3", "1"): "+3.3V", ("C3", "2"): "GND",
    ("C4", "1"): "+3.3V", ("C4", "2"): "GND",
    ("C5", "1"): "+3.3V", ("C5", "2"): "GND",
    ("C6", "1"): "+3.3V", ("C6", "2"): "GND",
    ("C7", "1"): "+3.3V", ("C7", "2"): "GND",
    ("C8", "1"): "+3.3V", ("C8", "2"): "GND",
    ("C9", "1"): "+3.3V", ("C9", "2"): "GND",
    ("C10", "1"): "+3.3V", ("C10", "2"): "GND",
    ("C11", "1"): "VCAP_1", ("C11", "2"): "GND",
    ("C15", "1"): "VCAP_2", ("C15", "2"): "GND",

    # U7 (LMV358 Cat-Eye Front-End)
    ("C16", "1"): "PROBE_TP1", ("C16", "2"): "DIFF_IN_P",
    ("C17", "1"): "PROBE_TP2", ("C17", "2"): "DIFF_IN_N",
    ("R8", "1"): "DIFF_IN_P", ("R8", "2"): "GND",
    ("R9", "1"): "DIFF_IN_N", ("R9", "2"): "DIFF_AMP_N",
    ("R10", "1"): "DIFF_AMP_N", ("R10", "2"): "DIFF_OUT",
    ("R11", "1"): "DIFF_IN_P", ("R11", "2"): "GND",
    ("U7", "3"): "DIFF_IN_P", ("U7", "2"): "DIFF_AMP_N", ("U7", "1"): "DIFF_OUT",
    ("U7", "5"): "DIFF_OUT", ("U7", "6"): "ADC_CATEYE", ("U7", "7"): "RECT_OUT",
    ("D3", "1"): "ADC_CATEYE", ("D3", "2"): "RECT_OUT",
    ("C18", "1"): "ADC_CATEYE", ("C18", "2"): "GND",
    ("R12", "1"): "ADC_CATEYE", ("R12", "2"): "GND",
    ("U7", "8"): "+3.3V", ("U7", "4"): "GND",

    # U5: STM32F407VET6 Pin Mapping
    ("U5", "1"): "APPLE_PH2",
    ("U5", "2"): "APPLE_PH3",
    ("U5", "3"): "NC",
    ("U5", "4"): "NC",
    ("U5", "5"): "NC",
    ("U5", "6"): "+3.3V",
    ("U5", "7"): "ENC_SW",
    ("U5", "8"): "NC",
    ("U5", "9"): "NC",
    ("U5", "10"): "GND",
    ("U5", "11"): "+3.3V",
    ("U5", "12"): "OSC_IN",
    ("U5", "13"): "OSC_OUT",
    ("U5", "14"): "MCU_NRST",
    ("U5", "15"): "ISENSE_24V",
    ("U5", "16"): "ISENSE_12V",
    ("U5", "17"): "ISENSE_5V",
    ("U5", "18"): "NC",
    ("U5", "19"): "+3.3V",
    ("U5", "20"): "GND",
    ("U5", "21"): "+3.3V",
    ("U5", "22"): "+3.3V",
    ("U5", "23"): "ENC_A",
    ("U5", "24"): "ADC_CATEYE",
    ("U5", "25"): "NC",
    ("U5", "26"): "NC",
    ("U5", "27"): "GND",
    ("U5", "28"): "+3.3V",
    ("U5", "29"): "NC",
    ("U5", "30"): "NC",
    ("U5", "31"): "NC",
    ("U5", "32"): "NC",
    ("U5", "33"): "EN_24V",
    ("U5", "34"): "EN_12V",
    ("U5", "35"): "EN_5V",
    ("U5", "36"): "NC",
    ("U5", "37"): "NC",
    ("U5", "38"): "NC",
    ("U5", "39"): "NC",
    ("U5", "40"): "NC",
    ("U5", "41"): "NC",
    ("U5", "42"): "NC",
    ("U5", "43"): "NC",
    ("U5", "44"): "NC",
    ("U5", "45"): "NC",
    ("U5", "46"): "NC",
    ("U5", "47"): "NC",
    ("U5", "48"): "NC",
    ("U5", "49"): "VCAP_1",
    ("U5", "50"): "+3.3V",
    ("U5", "51"): "BTN_RUN",
    ("U5", "52"): "BTN_BACK",
    ("U5", "53"): "NC",
    ("U5", "54"): "NC",
    ("U5", "55"): "NC",
    ("U5", "56"): "NC",
    ("U5", "57"): "NC",
    ("U5", "58"): "NC",
    ("U5", "59"): "NC",
    ("U5", "60"): "NC",
    ("U5", "61"): "NC",
    ("U5", "62"): "NC",
    ("U5", "63"): "LED_READY",
    ("U5", "64"): "LED_BUSY",
    ("U5", "65"): "LED_FAULT",
    ("U5", "66"): "LED_INDEX",
    ("U5", "67"): "LED_READ",
    ("U5", "68"): "USART1_TX",
    ("U5", "69"): "USART1_RX",
    ("U5", "70"): "USB_DM",
    ("U5", "71"): "USB_DP",
    ("U5", "72"): "SWDIO",
    ("U5", "73"): "VCAP_2",
    ("U5", "74"): "GND",
    ("U5", "75"): "+3.3V",
    ("U5", "76"): "SWCLK",
    ("U5", "77"): "ENC_B",
    ("U5", "78"): "NC",
    ("U5", "79"): "NC",
    ("U5", "80"): "NC",
    ("U5", "81"): "FDD_READY",
    ("U5", "82"): "FDD_STEP",
    ("U5", "83"): "FDD_DIR",
    ("U5", "84"): "FDD_MOTOR_ON",
    ("U5", "85"): "FDD_DRV_SEL0",
    ("U5", "86"): "FDD_DRV_SEL1",
    ("U5", "87"): "FDD_SIDE1_SEL",
    ("U5", "88"): "FDD_WRITE_GATE",
    ("U5", "89"): "FDD_TRACK00",
    ("U5", "90"): "FDD_WRITE_PROTECT",
    ("U5", "91"): "FDD_DISK_CHANGE",
    ("U5", "92"): "FDD_INDEX",
    ("U5", "93"): "FDD_READ_DATA",
    ("U5", "94"): "BOOT0",
    ("U5", "95"): "BUZZER_PWM",
    ("U5", "96"): "FDD_WRITE_DATA",
    ("U5", "97"): "APPLE_PH0",
    ("U5", "98"): "APPLE_PH1",
    ("U5", "99"): "GND",
    ("U5", "100"): "+3.3V"
}

# ==============================================================================
# SHEET 3: UI CONTROLS, LEDS, BUZZER & TEST POINTS
# ==============================================================================
components_s3 = [
    # SW2: Rotary Encoder PEC11R
    {"lib": "Device", "sym": "RotaryEncoder_Switch", "ref": "SW2", "val": "PEC11R_ENC", "fp": "Rotary_Encoder:RotaryEncoder_Bourns_PEC11R-Switch_Vertical", "x": 50.8, "y": 60.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R13", "val": "10k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 90.0, "y": 55.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R14", "val": "10k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 90.0, "y": 65.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R15", "val": "10k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 90.0, "y": 75.0, "unit": 1},
    {"lib": "Device", "sym": "C", "ref": "C19", "val": "10nF", "fp": "Capacitor_SMD:C_0805_2012Metric", "x": 110.0, "y": 55.0, "unit": 1},
    {"lib": "Device", "sym": "C", "ref": "C20", "val": "10nF", "fp": "Capacitor_SMD:C_0805_2012Metric", "x": 110.0, "y": 65.0, "unit": 1},
    {"lib": "Device", "sym": "C", "ref": "C21", "val": "100nF", "fp": "Capacitor_SMD:C_0805_2012Metric", "x": 110.0, "y": 75.0, "unit": 1},

    # SW3: RUN / AUTO TEST Button
    {"lib": "Switch", "sym": "SW_Push", "ref": "SW3", "val": "BTN_RUN", "fp": "Button_Switch_THT:SW_PUSH_6mm_H5mm", "x": 50.8, "y": 120.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R16", "val": "10k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 90.0, "y": 120.0, "unit": 1},
    {"lib": "Device", "sym": "C", "ref": "C22", "val": "100nF", "fp": "Capacitor_SMD:C_0805_2012Metric", "x": 110.0, "y": 120.0, "unit": 1},

    # SW4: BACK / ESC Button
    {"lib": "Switch", "sym": "SW_Push", "ref": "SW4", "val": "BTN_BACK", "fp": "Button_Switch_THT:SW_PUSH_6mm_H5mm", "x": 50.8, "y": 160.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R17", "val": "10k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 90.0, "y": 160.0, "unit": 1},
    {"lib": "Device", "sym": "C", "ref": "C23", "val": "100nF", "fp": "Capacitor_SMD:C_0805_2012Metric", "x": 110.0, "y": 160.0, "unit": 1},

    # 5x Status LEDs
    {"lib": "Device", "sym": "LED", "ref": "D4", "val": "LED_READY_GRN", "fp": "LED_SMD:LED_0805_2012Metric", "x": 170.0, "y": 50.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R18", "val": "1k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 200.0, "y": 50.0, "unit": 1},
    {"lib": "Device", "sym": "LED", "ref": "D5", "val": "LED_BUSY_YEL", "fp": "LED_SMD:LED_0805_2012Metric", "x": 170.0, "y": 75.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R19", "val": "1k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 200.0, "y": 75.0, "unit": 1},
    {"lib": "Device", "sym": "LED", "ref": "D6", "val": "LED_FAULT_RED", "fp": "LED_SMD:LED_0805_2012Metric", "x": 170.0, "y": 100.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R20", "val": "1k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 200.0, "y": 100.0, "unit": 1},
    {"lib": "Device", "sym": "LED", "ref": "D7", "val": "LED_INDEX_BLU", "fp": "LED_SMD:LED_0805_2012Metric", "x": 170.0, "y": 125.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R21", "val": "1k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 200.0, "y": 125.0, "unit": 1},
    {"lib": "Device", "sym": "LED", "ref": "D8", "val": "LED_READ_ORG", "fp": "LED_SMD:LED_0805_2012Metric", "x": 170.0, "y": 150.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R22", "val": "1k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 200.0, "y": 150.0, "unit": 1},

    # Buzzer Subsystem
    {"lib": "Device", "sym": "Buzzer", "ref": "BZ1", "val": "BUZZER_5V", "fp": "Buzzer_Beeper:Buzzer_12x9.5mm_P7.62mm_Vertical", "x": 170.0, "y": 200.0, "unit": 1},
    {"lib": "Transistor_BJT", "sym": "2N3904", "ref": "Q1", "val": "2N3904", "fp": "Package_TO_SOT_SMD:SOT-23", "x": 200.0, "y": 200.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R23", "val": "1k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 230.0, "y": 200.0, "unit": 1},
    {"lib": "Device", "sym": "D_Small", "ref": "D9", "val": "1N4148", "fp": "Diode_SMD:D_SOD-123", "x": 170.0, "y": 180.0, "unit": 1},

    # Test Points & Cat-Eye Front Jacks
    {"lib": "Connector", "sym": "TestPoint", "ref": "TP1", "val": "TP_INDEX", "fp": "TestPoint:TestPoint_Pad_D2.0mm", "x": 270.0, "y": 50.0, "unit": 1},
    {"lib": "Connector", "sym": "TestPoint", "ref": "TP2", "val": "TP_READ_DATA", "fp": "TestPoint:TestPoint_Pad_D2.0mm", "x": 270.0, "y": 75.0, "unit": 1},
    {"lib": "Connector", "sym": "TestPoint", "ref": "TP3", "val": "TP_STEP", "fp": "TestPoint:TestPoint_Pad_D2.0mm", "x": 270.0, "y": 100.0, "unit": 1},
    {"lib": "Connector", "sym": "TestPoint", "ref": "TP4", "val": "TP_TRACK00", "fp": "TestPoint:TestPoint_Pad_D2.0mm", "x": 270.0, "y": 125.0, "unit": 1},
    {"lib": "Connector", "sym": "TestPoint", "ref": "TP5", "val": "TP_WRITE_GATE", "fp": "TestPoint:TestPoint_Pad_D2.0mm", "x": 270.0, "y": 150.0, "unit": 1},
    {"lib": "Connector", "sym": "TestPoint", "ref": "TP6", "val": "TP_GND", "fp": "TestPoint:TestPoint_Pad_D2.0mm", "x": 270.0, "y": 175.0, "unit": 1},

    # Front Jacks
    {"lib": "Connector", "sym": "Conn_01x02_Pin", "ref": "J8", "val": "JACK_PROBE_TP1", "fp": "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Horizontal", "x": 270.0, "y": 210.0, "unit": 1},
    {"lib": "Connector", "sym": "Conn_01x02_Pin", "ref": "J9", "val": "JACK_PROBE_TP2", "fp": "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Horizontal", "x": 270.0, "y": 240.0, "unit": 1},
]

net_map_s3 = {
    # Encoder
    ("SW2", "A"): "ENC_A", ("SW2", "B"): "ENC_B", ("SW2", "C"): "GND",
    ("SW2", "S1"): "ENC_SW", ("SW2", "S2"): "GND",
    ("R13", "1"): "ENC_A", ("R13", "2"): "+3.3V",
    ("R14", "1"): "ENC_B", ("R14", "2"): "+3.3V",
    ("R15", "1"): "ENC_SW", ("R15", "2"): "+3.3V",
    ("C19", "1"): "ENC_A", ("C19", "2"): "GND",
    ("C20", "1"): "ENC_B", ("C20", "2"): "GND",
    ("C21", "1"): "ENC_SW", ("C21", "2"): "GND",

    # Buttons
    ("SW3", "1"): "BTN_RUN", ("SW3", "2"): "GND",
    ("R16", "1"): "BTN_RUN", ("R16", "2"): "+3.3V",
    ("C22", "1"): "BTN_RUN", ("C22", "2"): "GND",
    ("SW4", "1"): "BTN_BACK", ("SW4", "2"): "GND",
    ("R17", "1"): "BTN_BACK", ("R17", "2"): "+3.3V",
    ("C23", "1"): "BTN_BACK", ("C23", "2"): "GND",

    # LEDs
    ("D4", "1"): "GND", ("D4", "2"): "LED_READY_A",
    ("R18", "1"): "LED_READY", ("R18", "2"): "LED_READY_A",
    ("D5", "1"): "GND", ("D5", "2"): "LED_BUSY_A",
    ("R19", "1"): "LED_BUSY", ("R19", "2"): "LED_BUSY_A",
    ("D6", "1"): "GND", ("D6", "2"): "LED_FAULT_A",
    ("R20", "1"): "LED_FAULT", ("R20", "2"): "LED_FAULT_A",
    ("D7", "1"): "GND", ("D7", "2"): "LED_INDEX_A",
    ("R21", "1"): "LED_INDEX", ("R21", "2"): "LED_INDEX_A",
    ("D8", "1"): "GND", ("D8", "2"): "LED_READ_A",
    ("R22", "1"): "LED_READ", ("R22", "2"): "LED_READ_A",

    # Buzzer
    ("BZ1", "1"): "+5V_REG", ("BZ1", "2"): "BUZZER_DRV",
    ("D9", "1"): "+5V_REG", ("D9", "2"): "BUZZER_DRV",
    ("Q1", "1"): "GND", ("Q1", "2"): "BUZZER_BASE", ("Q1", "3"): "BUZZER_DRV",
    ("R23", "1"): "BUZZER_PWM", ("R23", "2"): "BUZZER_BASE",

    # Test Points
    ("TP1", "1"): "FDD_INDEX",
    ("TP2", "1"): "FDD_READ_DATA",
    ("TP3", "1"): "FDD_STEP",
    ("TP4", "1"): "FDD_TRACK00",
    ("TP5", "1"): "FDD_WRITE_GATE",
    ("TP6", "1"): "GND",

    # Probe Jacks
    ("J8", "1"): "PROBE_TP1", ("J8", "2"): "GND",
    ("J9", "1"): "PROBE_TP2", ("J9", "2"): "GND",
}

# ==============================================================================
# SHEET 4: FDD PHYSICAL INTERFACES, BUFFERS & CONNECTORS
# ==============================================================================
components_s4 = [
    # J10: IDC-50 for 8" Floppy Drives
    {"lib": "Connector_Generic", "sym": "Conn_02x25_Odd_Even", "ref": "J10", "val": "IDC50_8INCH", "fp": "Connector_IDC:IDC-Header_2x25_P2.54mm_Horizontal", "x": 60.0, "y": 140.0, "unit": 1},
    
    # J11: IDC-34 for 5.25" and 3.5" Standard PC/Shugart Floppy Drives
    {"lib": "Connector_Generic", "sym": "Conn_02x17_Odd_Even", "ref": "J11", "val": "IDC34_STANDARD", "fp": "Connector_IDC:IDC-Header_2x17_P2.54mm_Horizontal", "x": 130.0, "y": 140.0, "unit": 1},
    
    # J12: IDC-26 for 3.5" Slimline Laptop Floppy Drives
    {"lib": "Connector_Generic", "sym": "Conn_02x13_Odd_Even", "ref": "J12", "val": "IDC26_SLIMLINE", "fp": "Connector_IDC:IDC-Header_2x13_P2.54mm_Horizontal", "x": 190.0, "y": 140.0, "unit": 1},

    # J13: IDC-20 for Apple II Disk II
    {"lib": "Connector_Generic", "sym": "Conn_02x10_Odd_Even", "ref": "J13", "val": "IDC20_APPLE_II", "fp": "Connector_IDC:IDC-Header_2x10_P2.54mm_Horizontal", "x": 250.0, "y": 140.0, "unit": 1},

    # J14: 6-pin Stepper Direct Drive Header
    {"lib": "Connector_Generic", "sym": "Conn_01x06", "ref": "J14", "val": "STEPPER_4PHASE", "fp": "Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Horizontal", "x": 300.0, "y": 140.0, "unit": 1},

    # U4: 74LS06 Open-Collector Hex Inverter Buffer (Drive signals)
    {"lib": "74xx", "sym": "74LS06", "ref": "U4", "val": "7406_HEX_OC", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 60.0, "y": 50.0, "unit": 1},
    {"lib": "74xx", "sym": "74LS06", "ref": "U4", "val": "7406_HEX_OC", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 60.0, "y": 70.0, "unit": 2},
    {"lib": "74xx", "sym": "74LS06", "ref": "U4", "val": "7406_HEX_OC", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 60.0, "y": 90.0, "unit": 3},
    {"lib": "74xx", "sym": "74LS06", "ref": "U4", "val": "7406_HEX_OC", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 90.0, "y": 50.0, "unit": 4},
    {"lib": "74xx", "sym": "74LS06", "ref": "U4", "val": "7406_HEX_OC", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 90.0, "y": 70.0, "unit": 5},
    {"lib": "74xx", "sym": "74LS06", "ref": "U4", "val": "7406_HEX_OC", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 90.0, "y": 90.0, "unit": 6},
    {"lib": "74xx", "sym": "74LS06", "ref": "U4", "val": "7406_HEX_OC", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 75.0, "y": 110.0, "unit": 7},

    # U8: 74LS06 (Secondary Driver)
    {"lib": "74xx", "sym": "74LS06", "ref": "U8", "val": "7406_HEX_OC", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 130.0, "y": 50.0, "unit": 1},
    {"lib": "74xx", "sym": "74LS06", "ref": "U8", "val": "7406_HEX_OC", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 130.0, "y": 70.0, "unit": 2},
    {"lib": "74xx", "sym": "74LS06", "ref": "U8", "val": "7406_HEX_OC", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 130.0, "y": 90.0, "unit": 3},
    {"lib": "74xx", "sym": "74LS06", "ref": "U8", "val": "7406_HEX_OC", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 160.0, "y": 50.0, "unit": 4},
    {"lib": "74xx", "sym": "74LS06", "ref": "U8", "val": "7406_HEX_OC", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 160.0, "y": 70.0, "unit": 5},
    {"lib": "74xx", "sym": "74LS06", "ref": "U8", "val": "7406_HEX_OC", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 160.0, "y": 90.0, "unit": 6},
    {"lib": "74xx", "sym": "74LS06", "ref": "U8", "val": "7406_HEX_OC", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 145.0, "y": 110.0, "unit": 7},

    # U9: 74HC14 Hex Schmitt-Trigger Inverter (Receiver)
    {"lib": "74xx", "sym": "74HC14", "ref": "U9", "val": "74HC14_HEX_SCHMITT", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 200.0, "y": 50.0, "unit": 1},
    {"lib": "74xx", "sym": "74HC14", "ref": "U9", "val": "74HC14_HEX_SCHMITT", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 200.0, "y": 70.0, "unit": 2},
    {"lib": "74xx", "sym": "74HC14", "ref": "U9", "val": "74HC14_HEX_SCHMITT", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 200.0, "y": 90.0, "unit": 3},
    {"lib": "74xx", "sym": "74HC14", "ref": "U9", "val": "74HC14_HEX_SCHMITT", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 230.0, "y": 50.0, "unit": 4},
    {"lib": "74xx", "sym": "74HC14", "ref": "U9", "val": "74HC14_HEX_SCHMITT", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 230.0, "y": 70.0, "unit": 5},
    {"lib": "74xx", "sym": "74HC14", "ref": "U9", "val": "74HC14_HEX_SCHMITT", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 230.0, "y": 90.0, "unit": 6},
    {"lib": "74xx", "sym": "74HC14", "ref": "U9", "val": "74HC14_HEX_SCHMITT", "fp": "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm", "x": 215.0, "y": 110.0, "unit": 7},

    # U10: ULN2003A (Apple II Stepper Phase Driver)
    {"lib": "Transistor_Array", "sym": "ULN2003A", "ref": "U10", "val": "ULN2003A", "fp": "Package_SO:SOIC-16_3.9x9.9mm_P1.27mm", "x": 280.0, "y": 70.0, "unit": 1},

    # Pull-up Resistors (1k to +5V_REG on input signals)
    {"lib": "Device", "sym": "R", "ref": "R24", "val": "1k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 330.0, "y": 50.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R25", "val": "1k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 330.0, "y": 65.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R26", "val": "1k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 330.0, "y": 80.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R27", "val": "1k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 330.0, "y": 95.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R28", "val": "1k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 330.0, "y": 110.0, "unit": 1},
    {"lib": "Device", "sym": "R", "ref": "R29", "val": "1k", "fp": "Resistor_SMD:R_0805_2012Metric", "x": 330.0, "y": 125.0, "unit": 1},
]

net_map_s4 = {
    # U4 (74LS06 Drivers)
    ("U4", "1"): "FDD_STEP", ("U4", "2"): "BUS_STEP_N",
    ("U4", "3"): "FDD_DIR", ("U4", "4"): "BUS_DIR_N",
    ("U4", "5"): "FDD_MOTOR_ON", ("U4", "6"): "BUS_MOTOR_ON_N",
    ("U4", "9"): "FDD_DRV_SEL0", ("U4", "8"): "BUS_DRV_SEL0_N",
    ("U4", "11"): "FDD_DRV_SEL1", ("U4", "10"): "BUS_DRV_SEL1_N",
    ("U4", "13"): "FDD_WRITE_GATE", ("U4", "12"): "BUS_WRITE_GATE_N",
    ("U4", "14"): "+5V_REG", ("U4", "7"): "GND",

    # U8 (74LS06 Secondary Drivers)
    ("U8", "1"): "FDD_WRITE_DATA", ("U8", "2"): "BUS_WRITE_DATA_N",
    ("U8", "3"): "FDD_SIDE1_SEL", ("U8", "4"): "BUS_SIDE1_SEL_N",
    ("U8", "5"): "NC", ("U8", "6"): "NC",
    ("U8", "9"): "NC", ("U8", "8"): "NC",
    ("U8", "11"): "NC", ("U8", "10"): "NC",
    ("U8", "13"): "NC", ("U8", "12"): "NC",
    ("U8", "14"): "+5V_REG", ("U8", "7"): "GND",

    # U9 (74HC14 Receivers)
    ("U9", "1"): "BUS_INDEX_N", ("U9", "2"): "FDD_INDEX",
    ("U9", "3"): "BUS_READ_DATA_N", ("U9", "4"): "FDD_READ_DATA",
    ("U9", "5"): "BUS_TRACK00_N", ("U9", "6"): "FDD_TRACK00",
    ("U9", "9"): "BUS_WRITE_PROTECT_N", ("U9", "8"): "FDD_WRITE_PROTECT",
    ("U9", "11"): "BUS_DISK_CHANGE_N", ("U9", "10"): "FDD_DISK_CHANGE",
    ("U9", "13"): "BUS_READY_N", ("U9", "12"): "FDD_READY",
    ("U9", "14"): "+5V_REG", ("U9", "7"): "GND",

    # Pull-ups on bus inputs
    ("R24", "1"): "+5V_REG", ("R24", "2"): "BUS_INDEX_N",
    ("R25", "1"): "+5V_REG", ("R25", "2"): "BUS_READ_DATA_N",
    ("R26", "1"): "+5V_REG", ("R26", "2"): "BUS_TRACK00_N",
    ("R27", "1"): "+5V_REG", ("R27", "2"): "BUS_WRITE_PROTECT_N",
    ("R28", "1"): "+5V_REG", ("R28", "2"): "BUS_DISK_CHANGE_N",
    ("R29", "1"): "+5V_REG", ("R29", "2"): "BUS_READY_N",

    # U10 (ULN2003A Stepper Driver)
    ("U10", "1"): "APPLE_PH0", ("U10", "16"): "APPLE_PH0_DRV",
    ("U10", "2"): "APPLE_PH1", ("U10", "15"): "APPLE_PH1_DRV",
    ("U10", "3"): "APPLE_PH2", ("U10", "14"): "APPLE_PH2_DRV",
    ("U10", "4"): "APPLE_PH3", ("U10", "13"): "APPLE_PH3_DRV",
    ("U10", "5"): "NC", ("U10", "12"): "NC",
    ("U10", "6"): "NC", ("U10", "11"): "NC",
    ("U10", "7"): "NC", ("U10", "10"): "NC",
    ("U10", "8"): "GND", ("U10", "9"): "+12V_DRV",

    # J10 (IDC-50 for 8" Floppy Drives)
    # Odd pins to GND
    **{( "J10", str(p) ): "GND" for p in range(1, 51, 2)},
    # Even signals
    ("J10", "2"): "NC",
    ("J10", "4"): "NC",
    ("J10", "6"): "NC",
    ("J10", "8"): "NC",
    ("J10", "10"): "NC",
    ("J10", "12"): "NC",
    ("J10", "14"): "NC",
    ("J10", "16"): "NC",
    ("J10", "18"): "BUS_DIR_N",
    ("J10", "20"): "BUS_STEP_N",
    ("J10", "22"): "BUS_WRITE_DATA_N",
    ("J10", "24"): "BUS_WRITE_GATE_N",
    ("J10", "26"): "BUS_TRACK00_N",
    ("J10", "28"): "BUS_WRITE_PROTECT_N",
    ("J10", "30"): "BUS_READ_DATA_N",
    ("J10", "32"): "NC",
    ("J10", "34"): "BUS_READY_N",
    ("J10", "36"): "NC",
    ("J10", "38"): "NC",
    ("J10", "40"): "NC",
    ("J10", "42"): "NC",
    ("J10", "44"): "NC",
    ("J10", "46"): "BUS_INDEX_N",
    ("J10", "48"): "NC",
    ("J10", "50"): "NC",

    # J11 (IDC-34 for standard 5.25" and 3.5" Drives)
    # Odd pins to GND
    **{( "J11", str(p) ): "GND" for p in range(1, 35, 2)},
    # Even signals
    ("J11", "2"): "NC",
    ("J11", "4"): "NC",
    ("J11", "6"): "NC",
    ("J11", "8"): "BUS_INDEX_N",
    ("J11", "10"): "BUS_DRV_SEL0_N",
    ("J11", "12"): "BUS_DRV_SEL1_N",
    ("J11", "14"): "NC",
    ("J11", "16"): "BUS_MOTOR_ON_N",
    ("J11", "18"): "BUS_DIR_N",
    ("J11", "20"): "BUS_STEP_N",
    ("J11", "22"): "BUS_WRITE_DATA_N",
    ("J11", "24"): "BUS_WRITE_GATE_N",
    ("J11", "26"): "BUS_TRACK00_N",
    ("J11", "28"): "BUS_WRITE_PROTECT_N",
    ("J11", "30"): "BUS_READ_DATA_N",
    ("J11", "32"): "BUS_SIDE1_SEL_N",
    ("J11", "34"): "BUS_DISK_CHANGE_N",

    # J12 (IDC-26 for 3.5" Slimline Drives)
    **{( "J12", str(p) ): "GND" for p in [5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]},
    ("J12", "1"): "+5V_DRV", ("J12", "2"): "+5V_DRV", ("J12", "3"): "+5V_DRV", ("J12", "4"): "+5V_DRV",
    ("J12", "6"): "BUS_INDEX_N",
    ("J12", "8"): "BUS_DRV_SEL0_N",
    ("J12", "10"): "BUS_MOTOR_ON_N",
    ("J12", "12"): "BUS_DIR_N",
    ("J12", "14"): "BUS_STEP_N",
    ("J12", "16"): "BUS_WRITE_DATA_N",
    ("J12", "18"): "BUS_WRITE_GATE_N",
    ("J12", "20"): "BUS_TRACK00_N",
    ("J12", "22"): "BUS_WRITE_PROTECT_N",
    ("J12", "24"): "BUS_READ_DATA_N",
    ("J12", "26"): "BUS_DISK_CHANGE_N",

    # J13 (IDC-20 for Apple II Disk II)
    ("J13", "1"): "APPLE_PH0_DRV", ("J13", "2"): "GND",
    ("J13", "3"): "APPLE_PH1_DRV", ("J13", "4"): "GND",
    ("J13", "5"): "APPLE_PH2_DRV", ("J13", "6"): "GND",
    ("J13", "7"): "APPLE_PH3_DRV", ("J13", "8"): "GND",
    ("J13", "9"): "BUS_MOTOR_ON_N", ("J13", "10"): "GND",
    ("J13", "11"): "BUS_DRV_SEL0_N", ("J13", "12"): "+5V_DRV",
    ("J13", "13"): "BUS_WRITE_GATE_N", ("J13", "14"): "+12V_DRV",
    ("J13", "15"): "BUS_WRITE_DATA_N", ("J13", "16"): "-12V_DRV",
    ("J13", "17"): "BUS_READ_DATA_N", ("J13", "18"): "GND",
    ("J13", "19"): "BUS_WRITE_PROTECT_N", ("J13", "20"): "GND",

    # J14 (Direct Stepper 4-Phase Header)
    ("J14", "1"): "+12V_DRV",
    ("J14", "2"): "APPLE_PH0_DRV",
    ("J14", "3"): "APPLE_PH1_DRV",
    ("J14", "4"): "APPLE_PH2_DRV",
    ("J14", "5"): "APPLE_PH3_DRV",
    ("J14", "6"): "GND",
}

print("Running sheet generation...")

# Generate Sheet 2
build_clean_sheet(
    "MCU Core & Analog Front-End",
    "STM32F407VET6, LDO 3.3V, USB-C, HSE 8MHz, LMV358 Differential Cat-Eye Pre-Amp",
    components_s2,
    net_map_s2,
    [("+3.3V", 50.8, 30.0)],
    "02_MCU_Core.kicad_sch",
    1
)

# Generate Sheet 3
build_clean_sheet(
    "UI Controls, LEDs, Buzzer & Scope Test Points",
    "Bourns PEC11R Encoder, RUN/BACK Buttons, 5x Status LEDs, Buzzer Driver, Test Points & Probe Jacks",
    components_s3,
    net_map_s3,
    [],
    "03_UI_Controls.kicad_sch",
    2
)

# Generate Sheet 4
build_clean_sheet(
    "FDD Physical Interfaces & Bus Drivers",
    "IDC-50 (8\"), IDC-34 (5.25\"/3.5\"), IDC-26 (Slimline), IDC-20 (Apple II), 7406 Drivers, 74HC14 Receivers, ULN2003A",
    components_s4,
    net_map_s4,
    [],
    "04_FDD_Interfaces.kicad_sch",
    3
)

print("All sheets generated successfully!")
