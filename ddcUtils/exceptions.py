# -*- encoding: utf-8 -*-


def get_exception(e) -> str:
    """
    Get exception
    :param e: exception string
    :return: str
    """

    module = e.__class__.__module__
    if module is None or module == str.__class__.__module__:
        module_and_exception = f"[{e.__class__.__name__}]:[{e}]"
    else:
        module_and_exception = f"[{module}.{e.__class__.__name__}]:[{e}]"
    return module_and_exception.replace("\r\n", " ").replace("\n", " ")
