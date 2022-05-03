from collections import OrderedDict
	
class DICT():
    def __getitem__(self,key):
        return self.dict[key]

    def __init__(self,_dict = {}):
        self.dict = _dict
    
    def SortBy(self,keys = None,reverse = False):
        
        if keys != None:
            return OrderedDict(
                    sorted(
                            self.dict.items(),
                            key = lambda x: self._l_Slice(keys,x),
                            reverse = reverse   
                    )
                                    )
        else:
            return OrderedDict(
                    sorted(
                            self.dict.items(),
                            
                            reverse = reverse   
                    )
                                    )
            
        
        
    def _l_Slice(self,keys,x):
        if keys == None:
            return

        x = x[1]
        for key in keys:
            x = x[key]
        
        return x