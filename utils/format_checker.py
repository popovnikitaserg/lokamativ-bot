import re
def check_dimensions(cargos):
    flag = True
    for cargo in cargos:
        dimensions = re.split(r'[хx]', cargo)
        if len(dimensions) != 3:
            flag = False
        for dimension in dimensions:
            try:
                dimension = int(dimension)
            except:
                flag = False
    return flag

def check_weights(weights):
    flag = True
    for weight in weights:
        try:
            weight = int(weight)
        except:
            flag = False
    return flag