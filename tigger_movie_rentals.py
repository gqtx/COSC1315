"""
Author: Gabriel Hart
Date Started: 04/22/25
Description: Script to track and manage Tigger Movie Rentals' inventory
"""



# Module imports
import os
import time



# Constant definitions
MENU_COMMANDS = ("List    | \tList all movies in the inventory.", "Add     | \tAdd a movie to the inventory.", "Delete  | \tDelete a movie from the inventory.", "Exit    | \tQuit program.")
MENU_VALID_INPUT = MENU_COMMANDS + ("list", "add", "del", "delete", "exit", "1", "2", "3", "4")
YES_OPTIONS = ("yes", "y", "1")
NO_OPTIONS = ("no", "n", "0")
DB_FILE = "movies.txt"



# Variable definitions
session_movies_added = 0
session_movies_deleted = 0



def movie_file_check(file):
	"""
    Checks if a file exists and creates an empty file if it doesn't.

    Args:
        file (str): The path to the file to check.

    Returns:
        None.  The function creates the file if it doesn't exist but
        does not return the file object.

    Raises:
        Exception: If an error occurs during file creation, the
            exception is caught, an error message is printed to
            stderr, and the exception is not re-raised.
    """
	if not os.path.exists(file):
		try:
			with open(file, "w"):
				pass
		except Exception as e:
			print(f"An error occurred while creating necessary database file: {e}")
			input("Press enter to continue...")



def get_movie_total():
	"""Gets the total number of movies in the inventory.

    Reads the movie titles from 'movies.txt' and counts them.

    Returns:
        int: The total number of movies in the inventory.
             Returns 0 if the file is empty.
    """
	try:
		with open("movies.txt", "r") as movie_list:
			movies = movie_list.read()
			movie_count = len(movies.strip().split("\n"))
			if(movies == [''] or movies == ""):#checks if movie list is empty, returns 0 if so
				return 0
			else:
				return movie_count
	except Exception as e:
		print(f"An unexpected error occurred: {e}")
		return



def repair_database():
	"""Repairs the movie database file.

    Reads the 'movies.txt' file, removes empty lines, and writes the cleaned
    data back to the file.  Handles file operations using a temporary file
    to ensure data integrity.
    """
	fixed_database = []
	with open("movies.txt", "r") as infile, open("temp_movies.txt", "w") as outfile:
		for line in infile:
			if(line == "\n"):
				pass
			else:
				fixed_database.append(line.strip())
		fixed_database = "\n".join(fixed_database)
		outfile.write(fixed_database + "\n")
	os.remove("movies.txt")
	os.rename("temp_movies.txt", "movies.txt")
	display_movies()



def clear_screen():
	"""Clear the terminal screen.

    Uses the appropriate system command depending on the OS.
    """
	os.system('cls' if os.name == 'nt' else 'clear')



def display_movies():
	"""Display all movies currently in 'movies.txt'.

    Each movie is listed with a number, title, and year.
    """
	line_counter = 1
	if(get_movie_total() != 0):
		try:
			with open("movies.txt", "r") as movie_list:
				for line in movie_list:
					split_line = line.split("|")
					print(f"{line_counter}. {split_line[0]} ({split_line[1].strip()}) ")
					line_counter += 1
		except Exception:
			repair_database()
	else:
		print("No movies currently available.\n")



def list_stats():
	"""Display statistics of the session and current inventory.

    Displays the current number of movies in the inventory, the number of movies added during the session,
    and the number of movies deleted during the session.
    """
	print("Here are the statistics from your session:\n")
	print(f"Movies currently in inventory:\t{get_movie_total()}")
	print(f"Movies added this session:\t{session_movies_added}")
	print(f"Movies deleted this session:\t{session_movies_deleted}")



def list_command():
	"""Handle the 'list' command.

    Clears the screen, displays current movies, and waits for user input to continue.
    """
	clear_screen()
	print("Current Movies:\n")
	display_movies()
	input("Press enter to continue...")



def add_command():
	"""Handle the 'add' command.

    Prompts the user to input a movie title and year. 
    Saves the movie to 'movies.txt' and updates session counter.
    """
	clear_screen()

	add_movie_title = input("Enter the movie you would like to add [Press enter to cancel]: ")

	if(add_movie_title == ""):
		print("Cancelled")
		input("Press enter to continue...")
		return

	add_movie_year = input(f"Enter the year \"{add_movie_title}\" is from [Press enter to cancel]: ")

	if(add_movie_year == ""):
		print("Cancelled")
		input("Press enter to continue...")
		return

	add_movie_formatted = f"{add_movie_title}|{add_movie_year}\n"

	with open("movies.txt", "a") as movie_list:
		movie_list.write(f"{add_movie_formatted}")

	print(f"Added \"{add_movie_title} ({add_movie_year})\" to the list")
	input("Press enter to continue...")
	
	global session_movies_added #wrap up by incrementing the movies added counter
	session_movies_added += 1



def delete_command():
	"""Handle the 'del' command.

    Allows the user to delete a movie by selecting its number from the list.
    Confirms before deletion and handles invalid inputs.
    """
	clear_screen()

	if(get_movie_total() == 0):
		display_movies()
		input("Press enter to continue...")
		return

	print("Which movie would you like to remove?") #display list of movies and ask which one the user wants to remove
	display_movies()
	movie_to_delete = input("Enter the number of the movie you would like to delete [Press enter to cancel]: ")

	while(movie_to_delete.isdigit() == False and movie_to_delete != ""): #validates that the user inputted a number
		movie_to_delete = input("Invalid input, please enter a number [Press enter to cancel]: ")
	
	if(movie_to_delete == ""): # if user hits enter, cancel and return
		print("Cancelled")
		input("Press enter to continue...")
		return

	movie_to_delete = int(movie_to_delete) #if user input isn't blank and is a number, convert to int

	try: #checks if the selection is a valid option on the list. if not, handle error and restart
		movie_buffer = ""
		with open("movies.txt", "r") as movie_list:
			movie_buffer = movie_list.read().strip().split("\n") #reads current movies.txt file to a buffer
		deleted_movie_title = movie_buffer[movie_to_delete - 1].split("|")[0] #get title of the movie user wants to delete

	except IndexError: #handles the error if user enters a value not in the range of rows of movies.txt
		print(f"Error. No movie matching \"{movie_to_delete}\". Please select a valid option.")
		input("Press enter to continue...")
		delete_command()
		return #returns after finishing the recursive call so that the rest of the first call doesn't run

	user_confirmation = input(f"Are you sure you want to remove \"{deleted_movie_title}\"? [Y]es/[N]o\n") #ask for user confirmation
	while(user_confirmation.lower() not in YES_OPTIONS and user_confirmation.lower() not in NO_OPTIONS): #validate answer
		user_confirmation = input("Error. Please type yes or no: ")

	if(user_confirmation.lower() in YES_OPTIONS): #if user confirms, remove the selected movie by popping it from the list
		print(f"Removing \"{deleted_movie_title}\" from the catalog...")
		movie_buffer.pop(movie_to_delete - 1)
		movie_buffer_string = "\n".join(movie_buffer) #converts the movie buffer into a string so it can be written
		with open("movies.txt", "w") as movie_list:
			movie_list.write(movie_buffer_string + "\n") #writes the changes to movies.txt
		global session_movies_deleted
		session_movies_deleted += 1 #increment session deleted counter
		input("Press enter to continue...")

	elif(user_confirmation.lower() in NO_OPTIONS): #if user says no, do this
		try_again = input("Cancelling. Would you like to select a different movie for deletion? [Y]es/[N]o\n")#ask if they want to select different movie
		while(try_again.lower() not in YES_OPTIONS and try_again.lower() not in NO_OPTIONS):#validate response
			try_again = input("Error. Please type yes or no: ")

		if(try_again.lower() in YES_OPTIONS):#if they want to pick a different one, start at top of function
			delete_command()
		elif(try_again.lower() in NO_OPTIONS):#if they don't, return to main menu
			print("Cancelled")
			input("Press enter to continue...")
			return



def exit_command():
	"""Exit the program and display session statistics.

    Displays a thank you message and the statistics of the session before exiting.
    This function also clears the screen and introduces a delay before closing.
    """
	print("Exiting...")
	time.sleep(2)
	clear_screen()
	print("Thank you for using Tigger Movie Rentals' inventory management software!\n")
	list_stats()
	print("\nHave a great day :)")



user_selection = ""
def display_menu(clearterm=True):
	"""Display the main menu and prompt user for command.

    Args:
        clearterm (bool): Whether to clear the terminal before displaying menu.
            Defaults to True.
    """
	if clearterm:
		clear_screen()

	#show available commands from MENU_COMMANDS tuple
	print("Available commands: ")
	counter = 1
	for x in MENU_COMMANDS:
		print(f"{counter}. {x}")
		counter += 1

	#ask for user to input command
	global user_selection
	user_selection = input("\nPlease enter the name or number of a command: ").lower()

	while(user_selection not in MENU_VALID_INPUT): #confirms that user entered a valid option
		user_selection = input("Error: invalid entry. Please enter one of the available commands: ")

	#check if user command is valid and call corresponding function
	if user_selection in ("list", "1"):
		list_command()
	elif user_selection in ("add", "2"):
		add_command()
	elif user_selection in ("del", "delete", "3"):
		delete_command()
	elif user_selection in ("exit", "4"):
		return



def main():
	"""Main entry point of the program.

    Runs the menu loop until the user chooses to exit. Displays session stats at the end.
    """
	movie_file_check(DB_FILE)
	clear_screen()
	first_run = True
	while user_selection not in ("exit", "4"):
		if(first_run == True): #display welcome message on the first iteration
			print("Welcome to the Tigger Movie Rentals Inventory Manager!\n")
			display_menu(False)
		else:
			display_menu()
		first_run = False #set first run to False after first iteration

	#after exiting main loop, list total movie count, movies added, and movies deleted
	exit_command()



# Main function call
if(__name__ == "__main__"):
	main()




