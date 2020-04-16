# pyflowater - Python interface for the Flo by Moen API

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WREP29UDAMB6G)

Python library for communicating with the [Flo smart water monitoring and control devices](https://amzn.to/2WBn8tW?tag=rynoshark-20) via the Flo cloud API. [Flo](https://meetflo.com) is typically installed on the main water supply line and has sensors for flow rate, pressure, and temperature as well as shut off capabilities. Water shut off can be done manually, remotely, as well as automatically by Flo's emergency monitoring service when a leak is detected.

NOTE:

* This library is community supported, please submit changes and improvements.
* This is a very basic interface, not well thought out at this point, but works for the use cases that initially prompted spitting this out from.

## Installation

```
pip3 install pyflowater
```

## Examples

```python
flo = PyFlo(username, password)
flo.locations
```

See also [example-client.py](example-client.py) for a working example.

## See Also

* [Home Assistant Flo sensor](https://github.com/rsnodgrass/hass-flo-water)
* [Order Flo water monitoring device on Amazon.com](https://amzn.to/2WBn8tW?tag=rynoshark-20)
* [Flo by Moen](https://l.facebook.com/l.php?u=http%3A%2F%2Ffbuy.me%2Fo7V9I%3Ffbm%3D16505%26fbclid%3DIwAR15JOQdK5VYZpQqKkmFcMrWIKDe8XyR4ecrEYU2ZWiBzT08GwSxVCzq7sA&h=AT1QzphEpsIm7u4bgH8j1mtOifoyCHenHjndQvsD1D2d7o3FD8Xni24PYC59NA3lhKrZGHUWA6R2BIdzvqCM_Zt5x6kgmKxeBI36p5W0gAgi4bKaYj6kjgRMTxpARYJEJaGpvzw&__tn__=H-R&c[0]=AT33dWStfMtxxLDbsvLiMQ7_USqTAwNn1AZpODVitM-88PyL-dNPwrBGjc-taRETr07nikaNpoOlmPclmak0KlONJjlG3z-ijZJRVZEE1Vhzkrkij_XXCGsTzRnwA_57qIJAiRsQCZmviPXt865_Zpv-VkNGu3tv3h9yMZL_tncm8w1Z) (official product page)
* *[Special Flo Deal: Purchase Flo and get two free Smart Water Detectors](https://l.facebook.com/l.php?u=http%3A%2F%2Ffbuy.me%2Fo7V9I%3Ffbm%3D16505%26fbclid%3DIwAR15JOQdK5VYZpQqKkmFcMrWIKDe8XyR4ecrEYU2ZWiBzT08GwSxVCzq7sA&h=AT1QzphEpsIm7u4bgH8j1mtOifoyCHenHjndQvsD1D2d7o3FD8Xni24PYC59NA3lhKrZGHUWA6R2BIdzvqCM_Zt5x6kgmKxeBI36p5W0gAgi4bKaYj6kjgRMTxpARYJEJaGpvzw&__tn__=H-R&c[0]=AT33dWStfMtxxLDbsvLiMQ7_USqTAwNn1AZpODVitM-88PyL-dNPwrBGjc-taRETr07nikaNpoOlmPclmak0KlONJjlG3z-ijZJRVZEE1Vhzkrkij_XXCGsTzRnwA_57qIJAiRsQCZmviPXt865_Zpv-VkNGu3tv3h9yMZL_tncm8w1Z)*

## Known Issues

* not all APIs supported
