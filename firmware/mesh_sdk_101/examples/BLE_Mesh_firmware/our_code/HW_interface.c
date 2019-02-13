#include "hw_interface.h"
#include "nrf_gpio.h"

void leds_init()
{
  nrf_gpio_cfg_output(RLED);
  nrf_gpio_cfg_output(GLED);
  nrf_gpio_cfg_output(BLED);
}

