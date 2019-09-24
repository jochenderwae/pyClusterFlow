from typing import List, Optional
import copy


# FIXME: move this to its own library: YamlDict seems a good name
from adhesive.workspace.kube.YamlDictNavigator import YamlDictNavigator
from adhesive.workspace.kube.YamlNavigator import YamlNavigator


class YamlListNavigator(YamlNavigator):
    """
    A property navigator that allows accessing a list and
    correctly wraps potentially nested dictionaries.
    """
    def __init__(self,
                 *args,
                 content: Optional[List]=None,
                 property_name: str=""):
        if args:
            raise Exception("You need to pass the argument names")

        super(YamlListNavigator, self).__init__()

        self.__content = content if content is not None else list()
        self.__property_name = property_name

    def __deepcopy__(self, memodict={}):
        return YamlListNavigator(property_name=self.__property_name,
                                 content=copy.deepcopy(self.__content))

    def __getitem__(self, item):
        result = self.__content[item]

        if isinstance(result, dict):
            return YamlDictNavigator(
                property_name=f"{self.__property_name}.{item}",
                content=result)

        if isinstance(result, list):
            return YamlListNavigator(
                property_name=f"{self.__property_name}.{item}",
                content=result)

        return result

    def __setitem__(self, key, value):
        if isinstance(value, YamlNavigator):
            value = value._raw

        self.__content[key] = value

    def __delitem__(self, key):
        self.__content.__delitem__(key)

    def __iter__(self):
        return self.__content.__iter__()

    def __len__(self) -> int:
        return len(self.__content)

    @property
    def _raw(self) -> List:
        """
        Get access to the underlying collection.
        :return:
        """
        return self.__content

    def __repr__(self):
        return f"YamlListNavigator({self.__property_name}) {self.__content}"
