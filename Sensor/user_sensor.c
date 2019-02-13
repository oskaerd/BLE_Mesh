#include "app_error.h"
#include "nrf_drv_twi.h"
#include "nrf_delay.h"
#include "math.h"

#include "nrf_log.h"
#include "nrf_log_ctrl.h"
#include "nrf_log_default_backends.h"

#include "app_error.h"
#include "nrf_drv_twi.h"
#include "nrf_delay.h"
#include "math.h"

#include "nrf_log.h"
#include "nrf_log_ctrl.h"
#include "nrf_log_default_backends.h"

#include "user_sensor.h"

 uint8_t temp_reg = 0x50;
 uint8_t pres_reg	=	0x40;
 uint8_t adc_read	=	0x00;
 
 uint16_t wsp_c_odczyt[6];
 int32_t dt;

void twi_init (void)
{
    ret_code_t err_code;

    const nrf_drv_twi_config_t twi_config = {
       .scl                = SCL,
       .sda                = SDA,
       .frequency          = NRF_DRV_TWI_FREQ_100K,
       .interrupt_priority = APP_IRQ_PRIORITY_HIGH,
       .clear_bus_init     = false
    };

    err_code = nrf_drv_twi_init(&m_twi, &twi_config, NULL, NULL);
    APP_ERROR_CHECK(err_code);

    nrf_drv_twi_enable(&m_twi);
}


void temp_init(void)
{
		ret_code_t err_code;
	
		uint8_t wsp_c[2];
		uint8_t reg[6] = {0xA2, 0xA4, 0xA6, 0xA8, 0xAA, 0xAC};
		int i = 0; 
		
		for(i=0; i<6; i++){
			
			err_code = nrf_drv_twi_tx(&m_twi, sens_addr, &reg[i], sizeof(reg[i]), false);
			err_code = nrf_drv_twi_rx(&m_twi, sens_addr, wsp_c, sizeof(wsp_c));		
			wsp_c_odczyt[i] = (wsp_c[0] + ((uint16_t)wsp_c[1] << 8));	
			
		}	
}

double temp_odczyt(void){
		
		ret_code_t err_code;
		uint8_t read_data[3];
		
		int32_t temp = 0;
		double temp1 = 0;

		
		//odczyt temperatury
		err_code = nrf_drv_twi_tx(&m_twi, sens_addr, &temp_reg, sizeof(temp_reg), false);
		nrf_delay_ms(10);
	
		err_code = nrf_drv_twi_tx(&m_twi, sens_addr, &adc_read, sizeof(adc_read), false);
		err_code = nrf_drv_twi_rx(&m_twi, sens_addr, read_data, sizeof(read_data));
		
		temp = read_data[0] + ((uint32_t)read_data[1] << 8) + ((uint32_t)read_data[2] << 16);

		dt = temp - (wsp_c_odczyt[4])*pow(2,8);
	
		temp1 = 2000+((double)((double)(dt*wsp_c_odczyt[5])/(pow(2,23))));

		return temp1/1000;		
}

double cisnienie_odczyt(void){
		
		ret_code_t err_code;
		uint8_t read_data[3];
		int64_t offset;
		int64_t sensit;
		int32_t cisn = 0;
		double cisn1 = 0;

		
		//odczyt temperatury
		err_code = nrf_drv_twi_tx(&m_twi, sens_addr, &pres_reg, sizeof(pres_reg), false);
		nrf_delay_ms(10);
	
		err_code = nrf_drv_twi_tx(&m_twi, sens_addr, &adc_read, sizeof(adc_read), false);
		err_code = nrf_drv_twi_rx(&m_twi, sens_addr, read_data, sizeof(read_data));
		
		cisn = read_data[0] + ((uint32_t)read_data[1] << 8) + ((uint32_t)read_data[2] << 16);

		offset = wsp_c_odczyt[1]*pow(2,17) + (wsp_c_odczyt[3]*dt)/pow(2,6);
		sensit = wsp_c_odczyt[0]*pow(2,16) + (wsp_c_odczyt[2]*dt)/pow(2,7);
	
		cisn1 = ((cisn*sensit/pow(2,21)) - offset)/pow(2,15);
	
		return cisn1/1000;			
}