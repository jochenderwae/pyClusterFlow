from typing import Optional, Dict
from adhesive import config


def deep_clone(o):
    if isinstance(o, set):
        result = set()

        for it in o:
            result.add(deep_clone(it))

        return result

    if isinstance(o, list):
        result = list()

        for it in o:
            result.append(deep_clone(it))

        return result

    if isinstance(o, dict):
        result = dict()

        for k, v in o.items():
            result[k] = deep_clone(v)

        return result

    return o


def noop_clone(o):
    return o


clone = noop_clone if config.current.parallel_processing == "process" else deep_clone


def merge_dict(dict1: Dict, dict2: Dict) -> None:
    for k2, v2 in dict2.items():
        if k2 not in dict1:
            dict1[k2] = clone(v2)
            continue

        if v2 is None:
            del dict1[k2]
            continue

        v1 = dict1[k2]

        if isinstance(v1, set) and isinstance(v2, set):
            v1.update(clone(v2))
            continue

        if isinstance(v1, dict) and isinstance(v2, dict):
            merge_dict(v1, clone(v2))
            continue

        dict1[k2] = clone(v2)


class ExecutionData:
    def __init__(self,
                 initial_data: Optional[Dict] = None):
        self._data = dict(initial_data) if initial_data else dict()

    def as_dict(self) -> Dict:
        return self._data

    def __getattr__(self, item: str):
        if item.startswith("__") or item == '_data':
            return super(ExecutionData, self).__getattribute__(item)

        if item not in self._data:
            return None

        return self._data[item]

    def __setattr__(self, key, value):
        if key == "_data":
            super(ExecutionData, self).__setattr__(key, value)
            return

        self._data[key] = value

    def __setitem__(self, key, value):
        self._data[key] = value

    def __html__(self):
        return self.as_dict()

    @staticmethod
    def merge(*data_items: 'ExecutionData') -> 'ExecutionData':
        result = ExecutionData()

        for data in data_items:
            merge_dict(result._data, data._data)

        return result
