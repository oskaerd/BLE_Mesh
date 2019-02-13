#include "hw_interface.h"
#include "nrf_gpio.h"

void leds_init()
{
  nrf_gpio_cfg_output(RLED);
  nrf_gpio_cfg_output(GLED);
  nrf_gpio_cfg_output(BLED);

  nrf_gpio_pin_set(RLED);
  nrf_gpio_pin_set(BLED);
  nrf_gpio_pin_set(GLED);
}

