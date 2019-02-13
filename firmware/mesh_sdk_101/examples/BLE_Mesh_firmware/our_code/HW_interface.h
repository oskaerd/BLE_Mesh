#include "nrf_gpio.h"

#define RLED 25
#define GLED 26
#define BLED 27

#define RED_TOGGLE()  nrf_gpio_pin_toggle(RLED)
#define GRN_TOGGLE()  nrf_gpio_pin_toggle(GLED)
#define BLU_TOGGLE()  nrf_gpio_pin_toggle(BLED)

void leds_init(void);