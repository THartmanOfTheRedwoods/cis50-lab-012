#!/usr/bin/env python3

class Bijective:

    # dictionary = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~:/#[]@!$'()*+,;%="
    dictionary = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-~_"

    def __init__(self):
        self.dictionary = list(self.dictionary)

    def encode(self, i) -> str:
        if i == 0:
            return self.dictionary[0]

        result = []
        base = len(self.dictionary)

        while i > 0:
            result.append(self.dictionary[(i % base)])
            i = i // base  # floor of division

        result = result[::-1]  # reverse list

        return "".join(result)

    def decode(self, input_str) -> int:
        i = 0
        base = len(self.dictionary)

        input_str = list(input_str)

        for char in input_str:
            pos = self.dictionary.index(char)
            i = i * base + pos

        return i


def main():
    print("Class test started...")
    b = Bijective()
    my_id = 1000
    s = b.encode(my_id)
    print("Encoded {0} to {1}".format(my_id, s))
    my_id = b.decode(s)
    print("Decoded {0} to {1}".format(s, my_id))


if __name__ == "__main__":
    main()
