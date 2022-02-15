
Quick-Json is a python module that provides a fast and simple way to manipulate json data.

## Installation

```
pip install quick-json
```

## Quick start


```python
import quick_json as qjson


json_str = '{"name":"quick_json","description":{"feature":"open to use."}}'

# Get by path
feature = qjson.JsonObject(json_str).get('description.feature')
print(feature) 
#
# Output:
# open to use
```

## Path syntax

Example Json: 

```
{
  "size": {"width": 100, "height": 200},
  "duration":37,
  "characters": ["Tom","Alex","Jack"],
  "scenes": [
    {"start": 0, "duration": 10, "music": "first.mp3", "type": {"name":"rock"}},
    {"start": 10, "duration": 20, "music": "second.mp3", "type": {"name":"rock"}},
    {"start": 20, "duration": 30, "music": "third.mp3", "type": {"name": "pop"}},
    {"start": 20, "duration": 30, "music": "third.mp3", "type": {"name": "pop"}}
  ],
  "name_a": "a",
  "name_b": "b"
}
```

Path:

```
size.width              -> 100
duration                -> 37
characters.0            -> "Tom"
scenes.$.music          -> "third.mp3"
scenes.0.music          -> "first.mp3"
scenes.1.music          -> "second.mp3"
scenes.2.music          -> "third.mp3"
scenes.*.music          -> ["first.mp3","second.mp3","third.mp3"]

NOT SUPPORT NOW:
scenes.*[type='pop']    -> [{"start": 0, "duration": 10, "music": "first.mp3", "type": "pop"}]
```


## Inspire

This project is heavily inspired by 

- [gjson](https://github.com/tidwall/gjson)

- [sjson](https://github.com/tidwall/sjson)
