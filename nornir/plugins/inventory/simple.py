import logging
import os

from nornir.core.inventory import Inventory
from nornir.core.serializer import InventorySerializer

import ruamel.yaml


def SimpleInventory(
    host_file: str = "hosts.yaml",
    group_file: str = "groups.yaml",
    defaults_file: str = "defaults.yaml",
    *args,
    **kwargs
) -> Inventory:
    yml = ruamel.yaml.YAML(typ="safe")
    with open(host_file, "r") as f:
        hosts = yml.load(f)

    groups = {}
    if group_file:
        if os.path.exists(group_file):
            with open(group_file, "r") as f:
                groups = yml.load(f)
        else:
            logging.warning("{}: doesn't exist".format(group_file))
            groups = {}

    defaults = {}
    if defaults_file:
        if os.path.exists(defaults_file):
            with open(defaults_file, "r") as f:
                defaults = yml.load(f)
        else:
            logging.warning("{}: doesn't exist".format(defaults_file))
            defaults = {}

    inv_dict = {"hosts": hosts, "groups": groups, "defaults": defaults}
    return InventorySerializer.deserialize(inv_dict, *args, **kwargs)
