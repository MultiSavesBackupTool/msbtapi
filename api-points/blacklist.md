# /blacklist

## Request

To access the blacklist of non-game programs, perform a `GET` request to the following endpoint:

```
GET https://msbt.lukiuwu.xyz/api/blacklist
```

## Response

In this context, a `GET` request is used to retrieve data from a specific URL endpoint. When accessing the specified endpoint, you will receive a JSON array in response. Each element within this JSON array is another array containing the name of a program that has been blacklisted. Typically, these programs are non-game related and have been blocked from use for specific reasons. The example illustrates how program names are structured within the response.

### Example

The response to the request will look like this:

```json
[
    [
        "ExampleProgram1" - game name
    ],
    [
        "ExampleProgram2"
    ]
]
```
