#include "nrf_drv_spi.h"
#include "app_util_platform.h"
#include "nrf_gpio.h"
#include "nrf_delay.h"
#include "boards.h"
#include <string.h>
#include "wizchip_conf.h"
#include "w5500.h"
#include "socket.h"
#include "user_wiznet.h"

char msg[60];
char info[60];

void cs_sel() {
	nrf_gpio_pin_clear(SPI_SS_PIN); //CS LOW
	nrf_delay_ms(1);
}

void cs_desel() {
	nrf_delay_ms(1);
	nrf_gpio_pin_set(SPI_SS_PIN); //CS HIGH
}

uint8_t spi_rb(void) {
	uint8_t rbuf;
	nrf_drv_spi_transfer(&spi, NULL, 0, &rbuf, 1);
	
	return rbuf;
}

void spi_wb(uint8_t b) {
	nrf_drv_spi_transfer(&spi, &b, 1, NULL, 1);
}

void config_wiznet(){
	
		nrf_drv_spi_config_t spi_config = NRF_DRV_SPI_DEFAULT_CONFIG;
    spi_config.ss_pin   = SPI_SS_PIN;
    spi_config.miso_pin = SPI_MISO_PIN;
    spi_config.mosi_pin = SPI_MOSI_PIN;
    spi_config.sck_pin  = SPI_SCK_PIN;
    nrf_drv_spi_init(&spi, &spi_config, NULL, NULL);
	
		reg_wizchip_cs_cbfunc(cs_sel, cs_desel);
		reg_wizchip_spi_cbfunc(spi_rb, spi_wb);

		//Struktura do konfiguracji WizNeta 5500
		wiz_NetInfo netInfo = { .mac 	= {0x00, 0x08, 0xdc, 0xab, 0xcd, 0xef},		// Mac address
						  .ip 	= {192, 168, 1, 57},							// IP address
						  .sn 	= {255, 255, 255, 0},							// Subnet mask
						  .gw 	= {192, 168, 1, 1}};							// Gateway address
		
		//Ustawienie Wizneta								
		wizchip_setnetinfo(&netInfo);
							
		
}						

void config_server_param(){
	
		//Konfiguracja danych serwera, na ktory wiznet wysyla dane	
		uint8_t remoteIP[4] = {192, 168, 1, 192};
		uint16_t remotePort = 5000;
		
		while(socket(0, Sn_MR_TCP, 5000, 0) == -1);	
		while(connect(0, remoteIP, remotePort) == -1);
}

void send_to_server(){
	
		sprintf(msg, MES, 10, 123);
		send(0, msg, strlen(msg));
	
}