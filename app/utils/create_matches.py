import math


class CreateMatches(object):
    @staticmethod
    def create(l):
        """

        :param list l: a list with lists
        :return:
        """
        i = CreateMatches.calculate_number_of_matches(l)
        l.reverse()
        matches = []
        for number in range(i):
            q = []
            for j in range(len(l)):
                m = number % len(l[j])
                number = math.floor(number/len(l[j]))
                q.append(l[j][m])
            matches.append(q)
        return matches

    @staticmethod
    def calculate_number_of_matches(l):
        i = 1
        for item in l:
            i *= len(item)
        return i

