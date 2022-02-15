import json
from copy import deepcopy
from enum import Enum


class JsonObjectType (Enum):
    OBJECT = 1
    ARRAY = 2
    STRING = 3
    NUMBER = 4
    BOOLEAN = 5
    NULL = 6


DEBUG = False


def debug_print(info):
    global DEBUG
    if DEBUG:
        print(f'[DEBUG] {info}')

class FoundList:
    def __init__(self):
        self.found_list = []

    def add(self, item):
        if isinstance(item, FoundList):
            self.found_list.extend(item.json())
        else:
            self.found_list.append(item)

    def json(self):
        return self.found_list


class JsonObject():

    def __init__(self, object):
        self.raw_object = deepcopy(object)
        self.type_ = self._get_object_type()

    def _get_object_type(self):
        """
        Return the type of the object.
        """
        if isinstance(self.raw_object, dict):
            return JsonObjectType.OBJECT
        elif isinstance(self.raw_object, list):
            return JsonObjectType.ARRAY
        elif isinstance(self.raw_object, str):
            return JsonObjectType.STRING
        elif isinstance(self.raw_object, int) or isinstance(self.raw_object, float):
            return JsonObjectType.NUMBER
        elif isinstance(self.raw_object, bool):
            return JsonObjectType.BOOLEAN
        elif self.raw_object is None:
            return JsonObjectType.NULL
        else:
            raise Exception("Unknown type")

    def get(self, path, default=None, delimiter='.'):
        """
        Return the value of the node.
        :param path: json path
        """
        path_list = path.split(delimiter)
        result = self._get(path_list)
        if result is None:
            return default
        if isinstance(result, FoundList):
            return result.json()
        return result

    def _get(self, path: list):
        """
        Return the value of the node.
        :param path: json path list
        """
        debug_print(f'path: {path}')
        if not path:
            debug_print(f'path is empty, self.raw_object: {self.raw_object}')
            return self.raw_object
        if self.type_ == JsonObjectType.ARRAY:
            return self._array_get(path)
        elif self.type_ == JsonObjectType.OBJECT:
            return self._object_get(path)
        elif (self.type_ == JsonObjectType.STRING 
                or self.type_ == JsonObjectType.NUMBER
                or self.type_ == JsonObjectType.BOOLEAN
                or self.type_ == JsonObjectType.NULL):
            return self.raw_object
        else:
            raise Exception(f"Invalid path: {'.'.join(path)}")

    def _get_by_index(self, index):
        """
        Return the value of the node.
        :param index: index of the node
        """
        if self.type_ != JsonObjectType.ARRAY:
            return
        if index >= len(self.raw_object):
            return
        return self.raw_object[index]

    def _object_get(self, path: list):
        """
        path[0] could be:
            - string
            - string with attribute selector
                e.g. 'a.b.c=1'
        """
        debug_print(f'_object_get() path: {path}')
        obj = self.raw_object.get(path[0])
        if not obj:
            return
        return JsonObject(obj)._get(path[1:])

    def _array_get(self, path):
        """
        path[0] could be:
            - number
            - '*' (all)
        """
        debug_print(f'_array_get() path: {path}')
        key = path[0]
        if key.isdigit():
            json_obj = self._get_by_index(int(key))
            return JsonObject(json_obj)._get(path[1:])
        elif key == '*':
            found_list = FoundList()
            for item in self.raw_object:
                found_node = JsonObject(item)._get(path[1:])
                debug_print(f'found_node: {found_node}')
                if not found_node:
                    continue
                found_list.add(found_node)
            return found_list
        return self._get(path[1:])

    def json(self):
        return self.raw_object

    def set(self, path, value, delimiter='.'):
        """
        Set the value of the node.
        """
        path_list = path.split(delimiter)
        if not path_list:
            return
        if self.type_ == JsonObjectType.ARRAY:
            self._array_set(path_list, value)
        elif self.type_ == JsonObjectType.OBJECT:
            self._object_set(path_list, value)
        else:
            raise Exception(f"Invalid path: {'.'.join(path_list)}")

    def _array_set(self, path: list, value):
        debug_print(f'_array_set() path: {path}')
        key = path[0]
        if key.isdigit():
            self._set_by_index(int(key), value)
        elif key == '*':
            for item in self.raw_object:
                JsonObject(item).set(path[1:], value)
        else:
            raise Exception(f"Invalid path: {'.'.join(path)}")

    def _set_by_index(self, index, value):
        """
        Set the value of the node.
        """
        if self.type_ != JsonObjectType.ARRAY:
            return
        if index >= len(self.raw_object):
            return
        self.raw_object[index] = value

    def _object_set(self, path: list, value):
        debug_print(f'_object_set() path: {path}')
        obj = self.raw_object.get(path[0])
        if not obj:
            return
        JsonObject(obj).set(path[1:], value)

    def __str__(self):
        return str(json.dumps(self.raw_object, indent=2))


def test():
    json_dict = {
        'edit': {
            'timeline': {
                'tracks': [
                    {
                        'clips': [
                            {
                                'asset': {
                                    'type': 'avatar',
                                    'id': 'lara_01',
                                }
                            }
                        ]
                    },
                    {
                        'clips': [
                            {
                                'asset': {
                                    'type': 'video',
                                    'id': 'video_01',
                                }
                            },
                            {
                                'asset': {
                                    'type': 'image',
                                    'id': 'image_01',
                                }
                            }
                        ]
                    }
                ]
            }
        }
    }
    b = JsonObject(json_dict)
    #print(b.get('layers.*.name'))
    print(b.get('edit.timeline.tracks.*.clips.*.asset'))


if __name__ == '__main__':
    test()

