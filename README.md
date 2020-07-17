# bitfetch-home-assistant
Official Home Assistant Integration for BitFetch.io Cryptocurrency Market Data APIs. 

# About BitFetch
BitFetch provides High Performance cryptocurrency APIs. We have the fastest cryptocurrency APIs in the industry with servers in over 200 data centers in over 95 countries. We offer a 100% FREE plan with access to all of the crypto trading pairs and exchanges we support with generous API Credit limits. Our paid plans offer even more API Credits, additional features, and faster updates. 

Get your FREE API Key at https://bitfetch.io

BitFetch API Documentation: https://docs.bitfetch.io

# HA Integration Features
![BitFetch HA Sensor 1](https://github.com/BitFetch/bitfetch-home-assistant/raw/master/img/BitFetch_HA_Sensor_1.jpg)
- Adds a `sensor.bitfetch_<pair>` sensor to Home Assistant
- Supports all trading pairs BitFetch supports (Including XUSD pairs if you have a paid plan)
- Supports any update frequency, as low as 1 second
- Returns average price as the sensor state (volume-weighted average across all exchanges)
- Sensor attributes include:
  - 24 Hour Change Percent (volume-weighted average across all exchanges)
  - Price and Volume Data For Every Exchange
  - Timestamp of time data was last updated

![BitFetch HA Sensor 2](https://github.com/BitFetch/bitfetch-home-assistant/raw/master/img/BitFetch_HA_Sensor_2.jpg)
  
# HA Configuration
1. Install this integration via HACS
2. Add to your `configuration.yml` something similar to:
```
sensor:
  - platform: bitfetch
    pair: BTCUSD
    api_key: 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08 
    scan_interval: 1
```
`pair`: This is the trading pair you want to get data for, all supported pairs are at https://api.bitfetch.io/v1/price/pairs

`api_key`: Put your API Key here. !secrets is also supported

`scan_interval`: How often you want to poll the BitFetch API for new data. Default is 300 (5 minutes)
