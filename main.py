import csv
import enum
import sys

class Gender(enum.Enum):
    OTHER = 0
    MALE = 1
    FEMALE = 2

    @staticmethod
    def from_string(gender_string: str):
        gender: Gender = Gender.OTHER

        gender_string = gender_string.lower()

        if gender_string in ["male", "m"]:
            gender = Gender.MALE
        if gender_string in ["female", "f"]:
            gender = Gender.FEMALE

        return gender

class Person():
    def __init__(self, n: Gender, g: str, r: list[str]):
        if type(n) != str:
            raise TypeError("Type of provided value for 'n' must be type 'str' not {}".format(type(n)))
        if type(g) != Gender:
            raise TypeError("Type of provided value for 'g' must be type 'Gender' not {}".format(type(n)))
        if type(r) != list:
            raise TypeError("Type of provided value for 'r' must be type 'list[str]' not {}".format(type(p2)))
        else:
            # validate that all of the elements in the r list are of type str
            for x in r:
                if type(x) != str:
                    raise TypeError("Type of provided value for 'r' must be type 'list[str]' found an element with an invalid type of {}".format(type(x)))

        self.name = n
        self.gender = g
        self.responses = r

    def __str__(self):
        return "{} {} {}".format(self.name, self.gender, self.responses)

    # compare the person's answers with someone else's
    def compare(self, p) -> int:
        match_score: int = 0

        if type(p) != Person:
            raise TypeError("Type of provided value for 'p' must be type 'Person' not {}".format(type(n)))

        # make sure the both people have the same amount of responses before comparing
        # this makes it so that we never get an index error
        if len(self.responses) == len(p.responses):
            # compare self.responses to p.responses
            # adding 1 to the match_score for each matching response
            for i in range(len(self.responses)):
                if self.responses[i] == p.responses[i]:
                    match_score = match_score + 1

        return match_score

class Match():
    def __init__(self, p1: str, p2: str, match_score: int):
        if type(p1) != str:
            raise TypeError("Type of provided value for 'p1' must be type 'str' not {}".format(type(p1)))
        if type(p2) != str:
            raise TypeError("Type of provided value for 'p2' must be type 'str' not {}".format(type(p2)))
        if type(match_score) != int:
            raise TypeError("Type of provided value for 'match_score' must be type 'int' not {}".format(type(match_score)))

        self.p1 = p1
        self.p2 = p2
        self.match_score = match_score

    def __str__(self):
        p2_name = self.p2

        # special formatting for people who didnt get a match
        if len(p2_name) == 0:
            p2_name = "nobody :("

        return "{} & {}".format(self.p1, p2_name)

class Survey():
    def __init__(self, people: list[Person]):
        self.guys: list[Person] = []
        self.girls: list[Person] = []

        if type(people) != list:
            raise TypeError("Type of provided value for 'people' must be type 'list[Person]' not {}".format(type(p2)))
        else:
            # validate that all of the elements in the people list are of type Person
            for p in people:
                if type(p) != Person:
                    raise TypeError("Type of provided value for 'people' must be type 'list[Person]' found an element with an invalid type of {}".format(type(p)))

        for p in people:
            if p.gender == Gender.MALE:
                self.guys.append(p)
            elif p.gender == Gender.FEMALE:
                self.girls.append(p)
            else:
                print(p)
                raise ValueError("A person with an unexpected gender was provided ({}, {}). \
                 LoveMatch only currently supports binary gender matching".format(p.name, p.gender))

    @staticmethod
    def parse_csv(filename: str):
        survey: Survey = None

        if type(filename) != str:
            raise TypeError("Type of provided value for 'filename' must be type 'str' not {}".format(type(n)))

        people: list[Person] = []

        file_content: list[list[str]] = []

        # open the file
        with open(filename) as f:
            # wrap the file in a csv dialect reader
            csv_reader = csv.reader(f)

            # read the file content into a list of csv line lists
            for line in csv_reader:
                file_content.append(line)

        # iterate over the file contents
        # skipping the first line so that we ignore the csv header
        for line in file_content[1:]:
            if len(line) >= 2:
                # parse the gender string to an enum value
                gender = Gender.from_string(line[2])

                # a person has to have at least a name and a gender
                p = Person(line[1], gender, line[3:])

                people.append(p)

        survey = Survey(people)

        return survey

    def matches(self) -> list[Match]:
        matches: list[Match] = []

        # copy the girls list so that we can edit it without changing the class state
        girls = self.girls

        for p1 in self.guys:
            # for keeping track of the couple with the highest match score
            best_match: Match = None
            # for keeping track of the matched girl index after looping
            match_index: int = 0

            # loop over the girls to match them with guys
            for j in range(len(girls)):
                p2 = girls[j]

                highest_match_score: int = 0

                if best_match != None:
                    highest_match_score = best_match.match_score

                match_score = p1.compare(p2)

                if match_score > highest_match_score:
                    best_match = Match(p1.name, p2.name, match_score)
                    match_index = j

            # if there is no match it is because there is more girls than guys
            # add the extra guy to the matches list without a match
            if best_match == None:
                best_match = Match(p1.name, "", 0)

            matches.append(best_match)
            # slice the match girl out of the list so that they dont get matched again
            girls = girls[0:match_index] + girls[match_index + 1:len(girls)]

        # iterate over the rest of the girls to resolve any unmatched people
        for g in girls:
            extra_match = Match(g.name, "", 0)

            matches.append(extra_match)

        return matches

if __name__ == "__main__":
    err_string: str = ""
    filename: str = ""

    if len(sys.argv) >= 2:
        filename = sys.argv[1]
    else:
        err_string = "A file has to be supplied. Please provide one as a command line argument"

    if len(err_string) == 0:
        survey: Survey = Survey.parse_csv(filename)

        matches = survey.matches()

        print("Matches:\n")

        for m in matches:
            print(m)


    else:
        print(err_string)
