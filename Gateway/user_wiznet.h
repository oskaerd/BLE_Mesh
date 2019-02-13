#include "nrf_drv_spi.h"
#include "app_util_platform.h"
#include "nrf_gpio.h"
#include "nrf_delay.h"
#include "boards.h"
#include <string.h>
#include "wizchip_conf.h"
#include "w5500.h"
#include "socket.h"


#define SPI_INSTANCE  0 /**< SPI instance index. */
static const nrf_drv_spi_t spi = NRF_DRV_SPI_INSTANCE(SPI_INSTANCE);  /**< SPI instance. */
static volatile bool spi_xfer_done;  /**< Flag used to indicate that SPI instance completed the transfer. */

#define MES				"%d %d"

void cs_sel(void);

void cs_desel(void);

uint8_t spi_rb(void);

void spi_wb(uint8_t b);

void config_wiznet(void);

void config_server_param(void);

void send_to_server(void);
