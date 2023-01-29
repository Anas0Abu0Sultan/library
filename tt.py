
import os
import csv

# global variables
books_file = "booksInfo.txt"
borrowed_file = "borrowedInfo.txt"

# function to print all books in the library
def print_books():
  with open(books_file, "r") as f:
    reader = csv.reader(f)
    for row in reader:
      serial = row[0]
      title = row[1]
      authors = row[2]
      price = row[3]
      available = row[4]
      borrowed = row[5]
      total = int(available) + int(borrowed)
      print(f"Serial: {serial}, Title: {title}, Authors: {authors}, Price: {price}, Total Copies: {total}")

# function to search for a book by title or author
def search_book(query):
  query = query.lower()
  with open(books_file, "r") as f:
    reader = csv.reader(f)
    for row in reader:
      serial = row[0]
      title = row[1]
      authors = row[2]
      price = row[3]
      available = row[4]
      borrowed = row[5]
      total = int(available) + int(borrowed)
      if query in title.lower() or query in authors.lower():
        print(f"Serial: {serial}\n, Title: {title}\n, Authors: {authors}\n, Price: {price}\n, Total Copies: {total}")
        return
  print("No book found with the given title or author.")

# function to add a new book
def add_new_book():
    # Prompt the user to enter the serial number for the new book
    serial_number = input("Enter the serial number for the new book: ")
    # Validate that the serial number is 5 digits long and does not match any serial numbers of books already in the library
    if not serial_number.isdigit() or len(serial_number) != 5:
        print("Error: serial number must be a 5-digit number")
        return
    with open("booksInfo.txt", "r") as f:
        for line in f:
            fields = line.strip().split(",")
            if fields[0] == serial_number:
                print("Error: a book with this serial number already exists in the library")
                return
    # Prompt the user to enter the title of the new book
    title = input("Enter the title of the new book: ")
    # Validate that the title is not an empty string
    if not title:
        print("Error: title cannot be an empty string")
        return
    # Prompt the user to enter the names of the authors of the new book, separated by colons
    authors = input("Enter the names of the authors of the new book, separated by colons: ")
    # Validate that at least one author name is entered
    if not authors:
        print("Error: at least one author name must be entered")
        return
    # Prompt the user to enter the price of the new book
    price = input("Enter the price of the new book: ")
    # Validate that the price is a positive float
    try:
        price = float(price)
        if price <= 0:
            raise ValueError
    except ValueError:
        print("Error: price must be a positive float")
        return
    # Prompt the user to enter the number of available copies of the new book
    copies = input("Enter the number of available copies of the new book: ")
    # Validate that the number of copies is a positive integer
    try:
        copies = int(copies)
        if copies <= 0:
            raise ValueError
    except ValueError:
        print("Error: number of copies must be a positive integer")
        return
    # Add a new record to the "booksInfo.txt" file with the following information: serial number, title, authors, price, number of available copies, and number of borrowed copies (which should be 0 for a new book)
    with open("booksInfo.txt", "a") as f:
        f.write(f"{serial_number},{title},{authors},{price},{copies},0\n")
    # Display a message indicating that the new book has been added successfully
    print("Successfully added new book to the library")
# function to remove a book
def remove_book(serial):
  # check if book exists
  with open(books_file, "r") as f:
    reader = csv.reader(f)
    for row in reader:
      if row[0] == serial:
        # check if book has borrowed copies
        if int(row[5]) > 0:
          print("Error: cannot remove book with borrowed copies.")
          return
        # book can be removed, so display book information and confirm with user
        title = row[1]
        authors = row[2]
        price = row[3]
        available = row[4]
        borrowed = row[5]
        total = int(available) + int(borrowed)
        print(f"Serial: {serial}, Title: {title}, Authors: {authors}, Price: {price}, Total Copies: {total}")
        confirm = input("Are you sure you want to remove this book? (Y/N) ").lower()
        if confirm == "y":
          # remove book from booksInfo.txt
          with open(books_file, "r") as f_read:
            lines = f_read.readlines()
          with open(books_file, "w") as f_write:
            for line in lines:
              if line.strip("\n") != ",".join(row):
                f_write.write(line)
          print("Book removed successfully.")
        else:
          print("Book not removed.")
        return
  print("Error: invalid or non-existing serial number.")

# function to borrow a book
def borrow_book(serial_number,borrower_id):


  # Open booksInfo.txt and search for record with matching serial number
  with open("booksInfo.txt", "r") as f:
    for line in f:
      record = line.strip().split(",")
      if record[0] == serial_number:
        # Check if there are any available copies in the library
        if int(record[4]) == 0:
          print("Sorry, all copies of this book are currently borrowed.")
          return

  # Open borrowedInfo.txt and check if user has already borrowed 3 books or a copy of the same book
  with open("borrowedInfo.txt", "r") as f:
    books_borrowed = 0
    same_book_borrowed = False
    for line in f:
      record = line.strip().split(",")
      if record[1] == borrower_id:
        books_borrowed += 1
        if record[0] == serial_number:
          same_book_borrowed = True
    if books_borrowed == 3:
      print("Sorry, you have already borrowed the maximum number of books.")
      return
    if same_book_borrowed:
      print("Sorry, you have already borrowed a copy of this book.")
      return

  # Add new record to borrowedInfo.txt
  with open("borrowedInfo.txt", "a") as f:
    f.write(f"{serial_number},{borrower_id}\n")

  # Modify record in booksInfo.txt
  with open("booksInfo.txt", "r") as f:
    lines = f.readlines()
  with open("booksInfo.txt", "w") as f:
    for line in lines:
      record = line.strip().split(",")
      if record[0] == serial_number:
        record[4] = str(int(record[4]) - 1)
        record[5] = str(int(record[5]) + 1)
        f.write(",".join(record) + "\n")
      else:
        f.write(line)

  print("Book borrowed successfully!")
# function to return a book
def return_book(serial_number, borrower_id):
  # Open the borrowedInfo.txt file and search for a matching record
  with open("borrowedInfo.txt", "r") as borrowed_file:
    borrowed_records = borrowed_file.readlines()
  matching_record = None
  for record in borrowed_records:
    fields = record.strip().split(",")
    if fields[0] == serial_number and fields[1] == borrower_id:
      matching_record = record
      break

  # If a matching record is found, remove it from the borrowedInfo.txt file
  if matching_record is not None:
    borrowed_records.remove(matching_record)
    with open("borrowedInfo.txt", "w") as borrowed_file:
      borrowed_file.writelines(borrowed_records)
  else:
    print("No matching record found in borrowedInfo.txt")
    return

  # Open the booksInfo.txt file and search for a matching record
  with open("booksInfo.txt", "r") as books_file:
    books_records = books_file.readlines()
  matching_record = None
  for record in books_records:
    fields = record.strip().split(",")
    if fields[0] == serial_number:
      matching_record = record
      break

  # If a matching record is found, update the number of available copies and borrowed copies
  if matching_record is not None:
    fields = matching_record.strip().split(",")
    fields[4] = str(int(fields[4]) + 1)  # Increment the number of available copies
    fields[5] = str(int(fields[5]) - 1)  # Decrement the number of borrowed copies
    updated_record = ",".join(fields)
    books_records[books_records.index(matching_record)] = updated_record
    with open("booksInfo.txt", "w") as books_file:
      books_file.writelines(books_records)
    print("Book returned successfully")
  else:
    print("No matching record found in booksInfo.txt")


while True:
        # display menu
        print("\nLibrary Management System")
        print("===============================")
        print("1. Print books info")
        print("2. Search a book")
        print("3. Add a new book")
        print("4. Remove a book")
        print("5. Borrow a book")
        print("6. Return a book")
        print("7. Exit")
        print("===============================")
        choice = input("Enter your choice: ")

        # act on user's choice
        if choice == "1":
            print_books()
        elif choice == '2':
            x = input("search by title or search by author name")
            search_book(x)
        elif choice == "3":
            add_new_book()
        elif choice == "4":
            serial = input("Enter serial number: ")
            remove_book(serial)
        elif choice == "5":
            serial = input("Enter serial number: ")
            user_id = input("Enter user id: ")
            borrow_book(serial, user_id)
        elif choice == "6":
            serial = input("Enter serial number: ")
            user_id = input("Enter user id: ")
            return_book(serial, user_id)
        elif choice == "7":
            break
        else:
            print("Invalid choice.")
