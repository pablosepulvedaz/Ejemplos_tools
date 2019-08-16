"""
"""
import json, os, sys
class JsonTranslator(object):
    """
    """
    def __init__(self,filepath=None,data=None):
        """
        """
        self.setFilepath(filepath)
        self.setData(data)

    def getFilepath(self):
        """
        """
        return self._filepath

    def getData(self):
        """

        """
        return self._data

    def setFilepath(self,value):
        """
        """
        self._filepath = value

    def setData(self,value):
        """
        """
        if value == None:
            self._data = value
            return
        if not isinstance(value,dict):
            raise TypeError("{0} data must be a dictionary.".format(value))

        self._data = value

    def write(self):
        """
        """
        print self._filepath
        if not self._filepath:
            raise RuntimeError("No filepath was specified. Please set a filepath.")
        elif not self._data:
            raise RuntimeError("There was no data specified. Please set data.")

        # Write 
        with open(self._filepath, 'w') as f:
            f.write(json.dumps(self._data, sort_keys = True, indent = 4))

    def read(self):
        """
        """
        if not os.path.isfile(self._filepath):
            raise RuntimeError("This filepath {0} does not exist!.")

        # Write 
        with open(self._filepath, 'r') as f:
            self.setData(json.loads(f.read()))

        return self._data


