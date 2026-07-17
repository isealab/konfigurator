from konfigurator import class_from_path, get_class_path, instantiate_object_from_config


class MyTestClass:
    def __init__(self, name: str, func=None) -> None:
        self._name = name
        self._func = func

    @property
    def name(self) -> str:
        return self._name


class MyNestedTestClass:
    def __init__(self, child) -> None:
        self.child = child


def test_my_test_class():
    class_name = get_class_path(MyTestClass)
    assert class_name == "test_instantiation.MyTestClass"


def test_class_from_path():
    class_name = get_class_path(MyTestClass)
    cls = class_from_path(class_name)
    assert cls is MyTestClass


def test_instantiate_object_from_config():
    def non_pickable():
        yield from range(10)

    config = {
        "type": "test_instantiation.MyTestClass",
        "name": "test_instance",
        "func": non_pickable(),
    }
    instance = instantiate_object_from_config(config)
    assert instance.__class__ is MyTestClass
    assert instance.name == "test_instance"


def test_instantiate_object_from_config_recursive():
    config = {
        "type": "test_instantiation.MyNestedTestClass",
        "child": {
            "type": "test_instantiation.MyTestClass",
            "name": "nested_instance",
        },
    }
    instance = instantiate_object_from_config(config)
    assert instance.__class__ is MyNestedTestClass
    assert instance.child.__class__ is MyTestClass
    assert instance.child.name == "nested_instance"


def test_instantiate_object_from_config_recursive_in_list():
    config = {
        "type": "test_instantiation.MyNestedTestClass",
        "child": [
            {"type": "test_instantiation.MyTestClass", "name": "item_0"},
            {"type": "test_instantiation.MyTestClass", "name": "item_1"},
        ],
    }
    instance = instantiate_object_from_config(config)
    assert [c.name for c in instance.child] == ["item_0", "item_1"]


def test_instantiate_object_from_config_nested_plain_dict_untouched():
    config = {
        "type": "test_instantiation.MyNestedTestClass",
        "child": {"a": 1, "b": 2},
    }
    instance = instantiate_object_from_config(config)
    assert instance.child == {"a": 1, "b": 2}
