class Namer(object):
    def __init__(self):
        self.counts = {}
        self.symbols = [  # TODO: Select most visible ones
            u"\u0300",
            u"\u0301",
            u"\u0302",
            u"\u0303",
            u"\u0304",
            u"\u0305",
            u"\u0306",
            u"\u0307",
            u"\u0308",
            u"\u0309",
            u"\u0300",
            u"\u030A",
            u"\u030B",
            u"\u030C",
            u"\u030D",
            u"\u030E",
            u"\u030F",
            u"\u0310",
            u"\u0311",
            u"\u0312",
            u"\u0313",
            u"\u0314",
            u"\u0315",
            u"\u0316",
            u"\u0317",
            u"\u0318",
            u"\u0319",
            u"\u0310",
            u"\u031A",
            u"\u031B",
            u"\u031C",
            u"\u031D",
            u"\u031E",
            u"\u031F",
            u"\u0320",
            u"\u0321",
            u"\u0322",
            u"\u0323",
            u"\u0324",
            u"\u0325",
            u"\u0326",
            u"\u0327",
            u"\u0328",
            u"\u0329",
            u"\u0320",
            u"\u032A",
            u"\u032B",
            u"\u032C",
            u"\u032D",
            u"\u032E",
            u"\u032F",
            u"\u0330",
            u"\u0331",
            u"\u0332",
            u"\u0333",
            u"\u0334",
            u"\u0335",
            u"\u0336",
            u"\u0337",
            u"\u0338",
            u"\u0339",
            u"\u0330",
            u"\u033A",
            u"\u033B",
            u"\u033C",
            u"\u033D",
            u"\u033E",
            u"\u033F",
            u"\u0340",
            u"\u0341",
            u"\u0342",
            u"\u0343",
            u"\u0344",
            u"\u0345",
            u"\u0346",
            u"\u0347",
            u"\u0348",
            u"\u0349",
            u"\u0340",
            u"\u034A",
            u"\u034B",
            u"\u034C",
            u"\u034D",
            u"\u034E",
            u"\u034F",
            u"\u0350",
            u"\u0351",
            u"\u0352",
            u"\u0353",
            u"\u0354",
            u"\u0355",
            u"\u0356",
            u"\u0357",
            u"\u0358",
            u"\u0359",
            u"\u0350",
            u"\u035A",
            u"\u035B",
            u"\u035C",
            u"\u035D",
            u"\u035E",
            u"\u035F",
            u"\u0351",
            u"\u0352",
            u"\u0353",
            u"\u0354",
            u"\u0355",
            u"\u0356",
            u"\u0357",
            u"\u0358",
            u"\u0359",
            u"\u035A",
            u"\u035B",
            u"\u035C",
            u"\u035D",
            u"\u035E",
            u"\u035F",
            u"\u0360",
            u"\u036A",
            u"\u036B",
            u"\u036C",
            u"\u036D",
            u"\u036E",
            u"\u036F",
            u"\u0361",
            u"\u0362",
            u"\u0363",
            u"\u0364",
            u"\u0365",
            u"\u0366",
            u"\u0367",
            u"\u0368",
            u"\u0369",
            u"\u036A",
            u"\u036B",
            u"\u036C",
            u"\u036D",
            u"\u036E",
            u"\u036F",
        ]

    def reset(self):
        self.counts = {}

    def next_symbol(self, parent_name):
        """

        :type parent_name: str
        """
        if parent_name in self.counts:
            self.counts[parent_name] += 1
        else:
            self.counts[parent_name] = 1

        index = -self.counts[parent_name] % len(self.symbols)
        return self.symbols[index]

    def name_child(self, parent_name):
        """
         Returns a child's unique fixed-width glyph and its name.

         :type parent_name str
         :rtype tuple
         """
        glyph = str(parent_name[0] + self.next_symbol(parent_name))
        name = glyph + str(self.counts[parent_name])

        return glyph, name


namer = Namer()

if __name__ == "__main__":
    name = "O"
    glyph = name
    for i in range(6 * 16):
        glyph, child_name = namer.name_child(glyph)
        print("{:3}: {}".format(i, child_name))
