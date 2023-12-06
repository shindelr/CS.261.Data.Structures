# Please enter your name, favorite color, favorite hobby, and hometown in the list
my_list = ['Robin', 'Red', 'Surfing', 'Newport']

def my_info(my_list):
    """ A function that passes a list of my information """
    count = 0
    for value in my_list:
        count += 1
    return count


if __name__ == '__main__':
    print(my_info(my_list))

