# /gamesdetect

## Request

To access the gamesdetect list, make a GET request to the following endpoint:

```
GET https://msbt.lukiuwu.xyz/api/gamesdetect
```

## Response

### Explanation

The response from the GET request to the endpoint `/api/gamesdetect` returns a JSON array containing information about various software applications. Each object in the array provides details about a specific program, such as its executables, icon hash, and unique identifier (`id`). Additional attributes include whether the application supports in-game overlays (`overlay`), its associated themes, and whether it requires a hook for special handling. This API is used to identify programs that should not be categorized as games despite their executable names.

This is just a mirror of the Discord API `https://discord.com/api/applications/detectable`. It is not used yet.

### Example

The response to the request will look like this:

```json
[
  {
    "aliases": [],
    "executables": [
      {
        "is_launcher": false,
        "name": "speedrunners.exe",
        "os": "win32"
      }
    ],
    "hook": true,
    "icon_hash": "cb48279ea90e86fb4f71c709d3236395",
    "id": "259392830932254721",
    "name": "SpeedRunners",
    "overlay": false,
    "overlay_compatibility_hook": false,
    "overlay_methods": null,
    "overlay_warn": false,
    "themes": [
      "Action",
      "Party"
    ]
  }
]
```
