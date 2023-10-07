## main.py
from plagiarism_checker import PlagiarismChecker


def main():
    # Create an instance of the PlagiarismChecker class
    checker = PlagiarismChecker()

    # Get the input string from the user
    input_string = input("Enter the input string: ")

    # Check plagiarism in the input string
    percentage = checker.check_plagiarism(input_string)

    # Print the percentage of original content
    print(f"The percentage of original content is: {percentage}%")


if __name__ == "__main__":
    main()
