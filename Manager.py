class Manager:
    MANAGERS = []

    FIELDS = {}

    def __init__(self) -> None:
        Manager.MANAGERS.append(self)

    @staticmethod
    def set_field(key, value):
        Manager.FIELDS[key] = value

    @staticmethod
    def get_field(key):
        return Manager.FIELDS[key]

    @staticmethod
    def get_manager(manager_name):
        found = None

        for manager in Manager.MANAGERS:
            if type(manager).__name__ == manager_name:
                found = manager
                break

        return found