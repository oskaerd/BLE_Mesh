#include <stdio.h>
#include "boards.h"
#include "nrf_drv_twi.h"

/* TWI instance ID. */
#if TWI0_ENABLED
#define TWI_INSTANCE_ID     0
#endif

 /* Number of possible TWI addresses. */
 #define TWI_ADDRESSES      	127
 #define sens_addr						0x76
 
 #define SDA									11
 #define SCL									12
 
/* TWI instance. */
	static const nrf_drv_twi_t m_twi = NRF_DRV_TWI_INSTANCE(TWI_INSTANCE_ID);
	
void twi_init(void);

void temp_init(void);

double temp_odczyt(void);

double cisnienie_odczyt(void);

