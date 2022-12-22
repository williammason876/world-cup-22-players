from openweathersearcher import lookup

if __name__ == "__main__":
    val = input('Enter name of city: ')
    print(val)
    res = lookup(val)
    print(res)