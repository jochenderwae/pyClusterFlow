import os
from typing import Union

from adhesive import config


def ensure_folder(item: Union['ExecutionToken', 'ActiveEvent', str]) -> str:
    """
    Ensures the folder for the given item exists.

    :param item:
    :return:
    """
    full_path = get_folder(item)
    os.makedirs(full_path, exist_ok=True)

    return full_path


def get_folder(item: Union['ExecutionToken', 'ActiveEvent', str]) -> str:

    if isinstance(item, ExecutionToken):
        return os.path.join(
            config.current.temp_folder,
            item.execution_id,
            "logs",
            _get_loop(item),
            item.task.id,
            item.token_id)

    if isinstance(item, ActiveEvent):
        return get_folder(item.context)

    if isinstance(item, str):
        return os.path.join(config.current.temp_folder, item)

    raise Exception(f"Unable to get_folder for {item}.")


def _get_loop(context: 'ExecutionToken') -> str:
    loop = context.loop
    result = ""

    while loop:
        result += f"_loop_{loop.event_id}_{loop.index}/"
        loop = loop.parent_loop

    return result


from adhesive.model.ActiveEvent import ActiveEvent
from adhesive.execution.ExecutionToken import ExecutionToken
