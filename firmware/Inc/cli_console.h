/**
 * @file    cli_console.h
 * @brief   Diagnostic Serial Command Line Interface (CLI) for Bench Testing
 * @author  Alessio Iodice <alessio67@gmail.com>
 * @license CC BY-NC-SA 4.0
 */

#ifndef CLI_CONSOLE_H
#define CLI_CONSOLE_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

void cli_console_init(void);
void cli_console_process_char(char c);
void cli_console_printf(const char *fmt, ...);
void cli_console_puts(const char *str);

#ifdef __cplusplus
}
#endif

#endif /* CLI_CONSOLE_H */
