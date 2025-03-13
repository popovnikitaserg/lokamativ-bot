import re
def calculate(quantity, dimensions, weights):
    price = 0
    base = 4800
    for cargo in range(quantity):
        lenght, width, height = [s.strip() for s in re.split(r'[xх]', dimensions[cargo])]
        lenght, width, height = cm_to_m(lenght), cm_to_m(width), cm_to_m(height)
        weight = int(weights[cargo])
        volume = lenght * width * height
        weight_volume = weight / 1000 / 0.4
        cargo_price = max(volume, weight_volume) * base
        if lenght >= 3 and weight >= 1500:
            cargo_price += cargo_price * 0.1
        price += cargo_price
    return price


def cm_to_m(dimension):
    return int(dimension) / 100