cdef class Shrubbery:
    cdef int width, height

    def __init__(self, w, h):
        self.width = w
        self.height = h

    def get_area(self):
        return self.width * self.height

    def get_perimeter(self):
        return 2 * (self.width + self.height)

    def describe(self):
        print(f"This shrubbery is {self.width} by {self.height} cubits I think.")
