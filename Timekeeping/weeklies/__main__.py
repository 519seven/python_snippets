import yaml

class Weekly():

    def __init__(self, s_file) -> None:
        self.source_file = s_file

    def get_yaml_obj(self):
        with open(self.source_file, "r") as input_stream:
            try:
                print(yaml.safe_load(input_stream))
            except yaml.YAMLError as exc:
                print(exc)
                pass
