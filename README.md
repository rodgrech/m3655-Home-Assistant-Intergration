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

## Install

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

## HACS

This repository includes `hacs.json` so it can be added as a custom repository in HACS
once it has been pushed to GitHub.
