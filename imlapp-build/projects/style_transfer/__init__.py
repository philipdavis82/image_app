from place_holder import *

_Function_Lookup_Table = {
    "stylize"           :   stylize_from_model  ,
    "noise_reduction"   :   noise_reduction     ,
    "down_scale"        :   down_scale          ,
    "up_scale"          :   up_scale            ,
    "gaussian_blur"     :   gaussian_blur       ,
}

def get_function_table():
    return _Function_Lookup_Table.copy()

def get_function(name:str):
    fn = _Function_Lookup_Table.get(name)
    if fn is None:
        raise Exception("Function Not Found In Table")
    else:
        return fn

class Meta_Data_Structer():
    img = None                      # Copy of Input Image Data
    fn_list = []    