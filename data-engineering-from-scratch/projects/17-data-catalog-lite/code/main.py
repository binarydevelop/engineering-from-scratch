class DataCatalog:
    def __init__(self):
        self.assets = {}
    def register(self, name, owner, schema, description):
        self.assets[name] = {"owner": owner, "schema": schema, "description": description}
    def lookup(self, name):
        return self.assets.get(name)
