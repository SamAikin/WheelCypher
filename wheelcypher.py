# Written by Sam Aikin Aug 13, 2021.
#
# Copyright (c) 2021 Sam Aikin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# All rights reserved.
#
# A simple proof of concept implementation of a Wheel Cypher or a Jefferson Disk.
#
# https://en.wikipedia.org/wiki/Jefferson_disk
#
# A WHEEL contains a SEQUENCE of letters (this is the base encoding mechanisms)
# a DRUM contains a SEQUENCE of WHEELs (this is how a message is encoded / decoded)

class Wheel:
    elements = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '*']

    def __init__(self, sequence: list):
        if len(sequence) != 27 or sum(sequence) != 378:
            raise ValueError('Bad Wheel Sequence Passed')
        self._wheel = []
        for i in range(0, len(sequence)):
            self._wheel += self.elements[sequence[i] - 1]

    def encode(self, coded_letter: str):
        # first item is letter being encoded, so encoding value can be checked.
        offset = self._wheel.index(coded_letter)
        result = []
        for i in range(0, len(self._wheel)):
            index = (offset + i) % len(self._wheel)
            result += self._wheel[index]
        return result


class Drum:
    seq1 = [1, 27, 12, 15, 22, 20, 26, 19, 13, 8, 14, 10, 18,
            21, 9, 5, 23, 3, 4, 17, 16, 11, 2, 25, 7, 24, 6]
    seq2 = [1, 24, 26, 20, 11, 25, 13, 8, 16, 5, 19, 4, 21,
            18, 6, 12, 23, 9, 22, 15, 7, 14, 2, 17, 27, 10, 3]
    seq3 = [1, 10, 4, 23, 17, 9, 25, 3, 6, 24, 13, 21, 19, 7, 12,
            2, 26, 20, 8, 27, 18, 22, 5, 14, 11, 16, 15]
    seq4 = [1, 5, 22, 4, 17, 21, 12, 9, 2, 19, 10, 27, 8, 14, 16,
            6, 23, 13, 25, 11, 7, 24, 3, 26, 20, 18, 15]
    seq5 = [1, 8, 21, 14, 6, 18, 9, 12, 20, 7, 27, 13, 4, 15, 17,
            16, 5, 24, 19, 25, 10 ,11, 22, 23, 2, 3, 26]
    seq6 = [1, 5, 21, 13, 4, 7, 26, 18, 10, 2, 17, 20, 24, 3, 27,
            19, 12, 25, 6, 16, 14, 9, 22, 15, 8, 11, 23]
    # for now, fixed set of wheels, matching drum bought at Valley Forge.
    # Could be expanded to include ability to select an arbitrary order of wheels.
    def __init__(self):
        self._wheel = []
        while len(self._wheel) < 12:
            self._wheel += [Wheel(self.seq1)]
            self._wheel += [Wheel(self.seq2)]
            self._wheel += [Wheel(self.seq3)]
            self._wheel += [Wheel(self.seq4)]
            self._wheel += [Wheel(self.seq5)]
            self._wheel += [Wheel(self.seq6)]

    def encode(self, coded_str: str):
        letters = [str(letter) for letter in coded_str]
        # ensure that coded messages are always multiples of 12
        while len(letters) % 12 != 0:
            letters += 'Z'
        encodings = []
        for i in range(0, len(letters)):
            encodings += [self._wheel[i % 12].encode(letters[i])]
        result = []
        for i in range(0, len(encodings[0])):
            encoded_string = []
            for j in range(0, len(letters)):
                encoded_string += encodings[j][i]
            result += [''.join(encoded_string)]
        return result

if __name__ == "__main__":
    encoder = Drum()
    to_encode = input('Enter string to encode: ').upper()
    message = encoder.encode(to_encode)
    for i in range(0, len(message)):
        print(message[i])
