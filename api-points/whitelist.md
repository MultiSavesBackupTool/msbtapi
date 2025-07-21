# /whitelist

## Request

To access the whitelist of game, perform a GET request to the following endpoint:

```
GET https://msbt.lukiuwu.xyz/api/whitelist
```

## Response

The response from the API provides a list of whitelisted game programs and details for each one. Below are the key components explained:

* **Games Name**: The identifier or title of the game covered in the whitelist.
* **Save Path**: This is the file system location where the game's save data is located, using environment variables for flexibility on different systems.
* **Mod Path**: Specifies where user-created modifications for the game are stored, indicating customization areas.
* **Add Path**: Designates storage for additional files that are not native game mods but are relevant, such as game boosters or extensions.
* **Special Backup Mark**: A binary indicator (0 or 1) showing whether special actions are needed for backing up game data, helping manage data safety efficiently.

### Example

The response to the request will look like this:

```json
[
  [
    "ExampleProgram1", - game name
    "%userprofile%\\Documents\\My Games\\ExampleProgram1\\", - save path
    "%userprofile%\\Documents\\My Mods\\ExampleProgram1\\", - mod path
    "%userprofile%\\Documents\\My Add\\ExampleProgram1\\", - add path
    0 - specialbackup mark],
  [
    "ExampleProgram2",
    "%userprofile%\\Documents\\My Games\\ExampleProgram2\\",
    "%userprofile%\\Documents\\My Mods\\ExampleProgram2\\",
    "%userprofile%\\Documents\\My Add\\ExampleProgram2\\",
    0]
]
```
