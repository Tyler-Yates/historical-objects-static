from processor.books.books import process_books_input
from processor.medals.medals import process_medals_input
from processor.plates.plates import process_plats_input


def main():
    print("Processing books...")
    process_books_input()

    print("\nProcessing medals....")
    process_medals_input()

    print("\nProcessing plates....")
    process_plats_input()


if __name__ == '__main__':
    main()
