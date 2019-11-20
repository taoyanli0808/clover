
class Extract():

    def __init__(self, type="delimiter"):
        """
        :param type:
        """
        if type not in ["delimiter", "re"]:
            self.type = "delimiter"
        else:
            self.type = type
