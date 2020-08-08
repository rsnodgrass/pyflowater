# pyflowater - Python interface for the Flo by Moen API

[![PyPi](https://img.shields.io/pypi/v/pyflowater.svg)](https://pypi.python.org/pypi/pyflowater)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WREP29UDAMB6G)

Python library for communicating with the [Flo smart water monitoring and control devices](http://fbuy.me/v/rsnodgrass) via the Flo cloud API. [Flo](http://fbuy.me/v/rsnodgrass) is typically installed on the main water supply line and has sensors for flow rate, pressure, and temperature as well as shut off capabilities. Water shut off can be done manually, remotely, as well as automatically by Flo's emergency monitoring service when a leak is detected.

NOTE:

* This library is community supported, please submit changes and improvements.
* This is a very basic interface, not well thought out at this point, but works for the use cases that initially prompted spitting this out from.

## Supports

- current pressure
- consumpation data
- valve turn on/off
- location modes (home, away, sleep)

#### Not Supported

- water temp (DEPRECATED by FLO)

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
* [Flo by Moen](http://fbuy.me/v/rsnodgrass) (official product page)
* *[Special Flo Deal: Purchase Flo and get two free Smart Water Detectors](http://fbuy.me/v/rsnodgrass)*
* [Flo on Amazon](https://amzn.to/2WBn8tW?tag=rynoshark-20)

## Known Issues

* not all APIs supported
