# M3566 RGB Controller for Home Assistant

Custom Home Assistant integration for the M3566/RK3566 Android wall tablet RGB bridge.

It exposes the tablet RGB strip as a real Home Assistant `light` entity. The integration
talks to the Android app's local HTTP API:

```text
http://TABLET_IP:8765
```

## Requirements

Install and run the companion Android app on the tablet first:

```text
https://github.com/rodgrech/m3566-rgb-controller
```

The Android app must show a reachable API address such as:

```text
API: http://192.168.1.92:8765
```

## HACS Install

This repository supports HACS as a custom repository.

In Home Assistant:

```text
HACS > Integrations > Custom repositories
```

Add:

```text
https://github.com/rodgrech/m3566-Home-Assistant-Intergration
```

Category:

```text
Integration
```

Then install **M3566 RGB Controller** from HACS and restart Home Assistant.

## Manual Install

Copy this folder into your Home Assistant configuration directory:

```text
custom_components/m3566_rgb
```

Resulting path:

```text
/config/custom_components/m3566_rgb
```

Restart Home Assistant.

## Configure

In Home Assistant:

```text
Settings > Devices & services > Add integration > M3566 RGB Controller
```

Use the tablet IP shown in the Android app.

Example:

```text
Host: 192.168.1.92
Port: 8765
```

## Multiple Tablets

Multiple tablets are supported. Add the integration once per tablet using each tablet's
own IP address and port.

Example:

```text
Tablet 1: 192.168.1.92:8765
Tablet 2: 192.168.1.93:8765
Tablet 3: 192.168.1.94:8765
```

Each tablet becomes its own Home Assistant device with its own `light` entity.

## Entity

The integration creates one RGB `light` entity.

Because the tablet hardware exposes three binary RGB channels, colors are mapped to
channel on/off states rather than smooth brightness values:

- red on, green off, blue off = red
- red on, green on, blue off = yellow
- red on, green on, blue on = white
- all channels off = off

## API Endpoints Used

```text
GET /status
GET /set?red=1&green=0&blue=1
GET /color/off
```

## Companion Android App

The tablet-side Android bridge lives here:

```text
https://github.com/rodgrech/m3566-rgb-controller
```
