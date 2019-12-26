# pyflowater - Python interface for the Flo by Moen API

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WREP29UDAMB6G)

Python library for communicating with the [Flo smart water monitoring and control devices](https://amzn.to/2WBn8tW?tag=rynoshark-20) via the Flo cloud API. [Flo](https://meetflo.com) is typically installed on the main water supply line and has sensors for flow rate, pressure, and temperature as well as shut off capabilities. Water shut off can be done manually, remotely, as well as automatically by Flo's emergency monitoring service when a leak is detected.

This library is community supported, please submit changes and improvements.

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
* [Flo by Moen](https://meetflo.com) (official product page)
* [15% OFF purchases of Flo](https://meetflo.referralrock.com/l/818758/)

## Known Issues

* not all APIs supported