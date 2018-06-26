import shrubberylib


def main():
    print('creating a 10x20 shrub')
    x = shrubberylib.Shrubbery(10, 20)
    print('area is:', x.get_area())
    print('perimeter is:', x.get_perimeter())


if __name__ == '__main__':
    main()
