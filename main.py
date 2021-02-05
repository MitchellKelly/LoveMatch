import sys

from survey import survey

if __name__ == "__main__":
    err_string: str = ""
    filename: str = ""

    if len(sys.argv) >= 2:
        filename = sys.argv[1]
    else:
        err_string = "A file has to be supplied. Please provide one as a command line argument"

    if len(err_string) == 0:
        s: survey.Survey = survey.Survey.parse_csv(filename)

        matches = s.matches()

        print("Matches:\n")

        for m in matches:
            print(m)
    else:
        print(err_string)
