import json


def admin_data(path) -> dict:
    with open(path) as config_file:
        config_data = json.load(config_file)

        return config_data


admin_data_dict = admin_data("todo/admin.json")
admin_field_name = "dimochka"