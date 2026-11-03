/**
 * @file    hal_display.c
 * @brief   Hardware Abstraction Layer for ST7735S / ST7789 IPS Display on STM32F407
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 */

#include "hal_display.h"
#include "bsp_fdd_pins.h"
#include <stdbool.h>

/* Display Dimensions */
#define LCD_WIDTH_PIXELS        160U
#define LCD_HEIGHT_PIXELS       80U
#define LCD_FRAMEBUFFER_BYTES   (LCD_WIDTH_PIXELS * LCD_HEIGHT_PIXELS * 2U)

/* ST7735S / ST7789 Command Set */
#define CMD_SWRESET             0x01U
#define CMD_SLPIN               0x10U
#define CMD_SLPOUT              0x11U
#define CMD_NORON               0x13U
#define CMD_INVOFF              0x20U
#define CMD_INVON               0x21U
#define CMD_DISPOFF             0x28U
#define CMD_DISPON              0x29U
#define CMD_CASET               0x2AU
#define CMD_RASET               0x2BU
#define CMD_RAMWR               0x2CU
#define CMD_MADCTL              0x36U
#define CMD_COLMOD              0x3AU

/* Low-level GPIO Pin Helpers */
static inline void lcd_cs_low(void)   { HAL_GPIO_WritePin(LCD_CS_PORT, LCD_CS_PIN, GPIO_PIN_RESET); }
static inline void lcd_cs_high(void)  { HAL_GPIO_WritePin(LCD_CS_PORT, LCD_CS_PIN, GPIO_PIN_SET); }
static inline void lcd_dc_cmd(void)   { HAL_GPIO_WritePin(LCD_DC_PORT, LCD_DC_PIN, GPIO_PIN_RESET); }
static inline void lcd_dc_data(void)  { HAL_GPIO_WritePin(LCD_DC_PORT, LCD_DC_PIN, GPIO_PIN_SET); }
static inline void lcd_rst_low(void)  { HAL_GPIO_WritePin(LCD_RST_PORT, LCD_RST_PIN, GPIO_PIN_RESET); }
static inline void lcd_rst_high(void) { HAL_GPIO_WritePin(LCD_RST_PORT, LCD_RST_PIN, GPIO_PIN_SET); }
static inline void lcd_blk_on(void)   { HAL_GPIO_WritePin(LCD_BLK_PORT, LCD_BLK_PIN, GPIO_PIN_SET); }

/* Software / Hardware SPI Transmit Byte */
static void spi_write_byte(uint8_t byte) {
    /* If SPI1 hardware register is used */
    while (!(SPI1->SR & SPI_SR_TXE)) {
        /* Wait for TX buffer empty */
    }
    SPI1->DR = byte;
    while (SPI1->SR & SPI_SR_BSY) {
        /* Wait for transmission complete */
    }
}

static void lcd_write_cmd(uint8_t cmd) {
    lcd_cs_low();
    lcd_dc_cmd();
    spi_write_byte(cmd);
    lcd_cs_high();
}

static void lcd_write_data_byte(uint8_t data) {
    lcd_cs_low();
    lcd_dc_data();
    spi_write_byte(data);
    lcd_cs_high();
}

static void lcd_set_address_window(uint16_t x0, uint16_t y0, uint16_t x1, uint16_t y1) {
    /* Column Address Set */
    lcd_write_cmd(CMD_CASET);
    lcd_write_data_byte((uint8_t)(x0 >> 8));
    lcd_write_data_byte((uint8_t)(x0 & 0xFF));
    lcd_write_data_byte((uint8_t)(x1 >> 8));
    lcd_write_data_byte((uint8_t)(x1 & 0xFF));

    /* Row Address Set */
    lcd_write_cmd(CMD_RASET);
    lcd_write_data_byte((uint8_t)(y0 >> 8));
    lcd_write_data_byte((uint8_t)(y0 & 0xFF));
    lcd_write_data_byte((uint8_t)(y1 >> 8));
    lcd_write_data_byte((uint8_t)(y1 & 0xFF));

    /* Memory Write Command */
    lcd_write_cmd(CMD_RAMWR);
}

void hal_display_init(void) {
    /*
     * 1. GPIO Clock Enable (GPIOA, GPIOB, GPIOC)
     */
    __HAL_RCC_GPIOA_CLK_ENABLE();
    __HAL_RCC_GPIOB_CLK_ENABLE();
    __HAL_RCC_GPIOC_CLK_ENABLE();
    __HAL_RCC_SPI1_CLK_ENABLE();
    __HAL_RCC_DMA2_CLK_ENABLE();

    /*
     * 2. Configure Control Lines (CS, DC, RST, BLK) as Push-Pull Outputs
     */
    GPIO_InitTypeDef gpio = {0};

    gpio.Pin = LCD_CS_PIN;
    gpio.Mode = GPIO_MODE_OUTPUT_PP;
    gpio.Pull = GPIO_NOPULL;
    gpio.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    HAL_GPIO_Init(LCD_CS_PORT, &gpio);
    lcd_cs_high();

    gpio.Pin = LCD_DC_PIN;
    HAL_GPIO_Init(LCD_DC_PORT, &gpio);
    lcd_dc_cmd();

    gpio.Pin = LCD_RST_PIN;
    HAL_GPIO_Init(LCD_RST_PORT, &gpio);
    lcd_rst_high();

    gpio.Pin = LCD_BLK_PIN;
    HAL_GPIO_Init(LCD_BLK_PORT, &gpio);
    lcd_blk_on();

    /*
     * 3. Configure SPI1 Pins (PA5=SCK, PA7=MOSI) Alternate Function AF5
     */
    gpio.Pin = LCD_SCK_PIN | LCD_MOSI_PIN;
    gpio.Mode = GPIO_MODE_AF_PP;
    gpio.Pull = GPIO_NOPULL;
    gpio.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    gpio.Alternate = GPIO_AF5_SPI1;
    HAL_GPIO_Init(GPIOA, &gpio);

    /*
     * 4. Configure SPI1 Peripheral: 42 MHz (fPCLK2/2), Master, 8-bit, Mode 0
     */
    SPI1->CR1 = 0;
    SPI1->CR1 = SPI_CR1_MSTR | SPI_CR1_SSI | SPI_CR1_SSM | (0U << SPI_CR1_BR_Pos); /* BR=0 -> /2 (42MHz) */
    SPI1->CR1 |= SPI_CR1_SPE; /* Enable SPI */

    /*
     * 5. Hardware Reset Sequence
     */
    lcd_rst_high();
    hal_delay_ms(10);
    lcd_rst_low();
    hal_delay_ms(20);
    lcd_rst_high();
    hal_delay_ms(120);

    /*
     * 6. ST7735S / ST7789 Initialization Commands
     */
    lcd_write_cmd(CMD_SWRESET);
    hal_delay_ms(150);

    lcd_write_cmd(CMD_SLPOUT);
    hal_delay_ms(150);

    /* Color mode: 16-bit RGB565 */
    lcd_write_cmd(CMD_COLMOD);
    lcd_write_data_byte(0x55U);

    /* Memory Access Control (Orientation: Landscape 160x80) */
    lcd_write_cmd(CMD_MADCTL);
    lcd_write_data_byte(0x60U); /* MX=0, MY=1, MV=1 -> 160x80 landscape */

    /* Normal display on */
    lcd_write_cmd(CMD_NORON);
    hal_delay_ms(10);

    /* Display Inversion (IPS panels use INVON for correct RGB reproduction) */
    lcd_write_cmd(CMD_INVON);

    /* Display Power ON */
    lcd_write_cmd(CMD_DISPON);
    hal_delay_ms(50);
}

void hal_display_flush_rgb565(const uint16_t *fb) {
    if (!fb) return;

    /* Set 160x80 Display Window with 0.96" IPS panel offset */
    /* Typical 0.96" 160x80 ST7735S has column offset 24, row offset 0 */
    uint16_t x_offset = 24U;
    uint16_t y_offset = 0U;

    lcd_set_address_window(x_offset, y_offset, x_offset + LCD_WIDTH_PIXELS - 1U, y_offset + LCD_HEIGHT_PIXELS - 1U);

    lcd_cs_low();
    lcd_dc_data();

    /* Fast Burst Transmission over SPI1 */
    const uint8_t *byte_ptr = (const uint8_t *)fb;
    uint32_t total_bytes = LCD_FRAMEBUFFER_BYTES;

    for (uint32_t i = 0; i < total_bytes; i++) {
        /* Wait for TXE */
        while (!(SPI1->SR & SPI_SR_TXE)) {}
        /* Note: STM32 stores 16-bit little-endian; ST7735S expects big-endian */
        /* Transmit high byte then low byte */
        SPI1->DR = byte_ptr[i ^ 1U];
    }

    while (SPI1->SR & SPI_SR_BSY) {}
    lcd_cs_high();
}
