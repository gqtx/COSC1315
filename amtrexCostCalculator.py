"""
Author: Gabriel Hart
Date Written: 3/29/2025
Description:
Gets user input on how many items are available to be bought, then
asks user to pick a combination of items to add to the cart. Finally,
calculates the total cost of all selected items in cart. Written for a
fake company called "Amtrex".
"""
# Import time for waiting
import time

# Defining a function to clear the terminal screen
import os
def clearScreen():
	os.system('cls' if os.name == 'nt' else 'clear')

# Welcome screen
clearScreen()
print("Welcome to the Amtrex Budget Calculator!")

# Get user input for maximum amount of items able to be purchased
maxItems = int(input("\nPlease enter the maximum number of items that can be purchased: "))
clearScreen()

# Declaring variables needed for while loop functionality
selectedItems = int(0)
remainingItems = maxItems - selectedItems
removedItems = int(0)

# Declaring cost of items
scissorCost = 6.49
tapeCost = 3.99
paperCost = 7.99

# Declaring variables for amount of items in cart
scissorCount = 0
tapeCount = 0
paperCount = 0

# Defines a function to show the menu screen
def displayMenu():
	clearScreen()
	print("Amtrex Budget Calculator")
	print("Items available to purchase:")
	print(f"You have {remainingItems} items left in your budget of {maxItems} items\n")
	print(f"Scissors\tCost: ${scissorCost}\tCurrent amount: {scissorCount}")
	print(f"Tape\t	Cost: ${tapeCost}\tCurrent amount: {tapeCount}")
	print(f"Paper\t 	Cost: ${paperCost}\tCurrent amount: {paperCount}")

# Main loop that offers item selection
while selectedItems <= maxItems:
	# If the maximum number of items is selected, exit the loop
	if selectedItems == maxItems:
		displayMenu()
		print("\nMaximum number of items reached. Calculating total cost...")
		time.sleep(2)
		input("[Press enter to continue]")
		break

	# Display the main menu
	displayMenu()
	print("\nWhich items would you like to add?\n")
	addedItem = input("Please enter the type of item you would like to add [Or press enter to finish]: ")
	itemType = addedItem.lower()
	parsedItem = ""
	quantityItem = 0

	# Determines what item type was selected and asks the user how many they want to add
	if itemType == "scissors": #if scissors are selected, ask how many and update counter
		parsedItem = "pairs of scissors"
		quantityItem = int(input("How many pairs of scissors would you like to add? "))
		print(f"\nAdded {quantityItem} {parsedItem} to your cart.")
		scissorCount += quantityItem

	elif itemType == "paper": #if paper is selected, ask how many and update counters
		parsedItem = "reams of paper"
		quantityItem = int(input("How many reams of paper would you like to add? "))
		print(f"\nAdded {quantityItem} {parsedItem} to your cart.")
		paperCount += quantityItem

	elif itemType == "tape": #if tape is selected, ask how many and update counters
		parsedItem = "rolls of tape"
		quantityItem = int(input("How many rolls of tape would you like to add? "))
		print(f"\nAdded {quantityItem} {parsedItem} to your cart.")
		tapeCount += quantityItem

	elif itemType == "": #if user presses enter, exit the loop
		clearScreen()
		print("Calculating totals...")
		time.sleep(3)
		break

	else: #if an invalid type is given, repeat loop
		print("Error. Invalid item type. Please try again.")

	# Update counters of the remaining items available to choose and total amount of items selected	
	selectedItems += quantityItem
	remainingItems -= quantityItem
	# Print an update on amount of items then wait for user to press enter
	input(f"\n\nYou have selected {selectedItems} out of {maxItems} total items available with your budget.\n[Press enter to continue]")

	# If too many items are selected, ask which ones to remove
	if selectedItems > maxItems:

		# Define loop variables for removing excess items from the total
		excessItems = selectedItems - maxItems
		removedItems = ""

		while True: # loop runs until broken by correctly entering a type of item with sufficient excess to remove

			# Displays a screen that asks which type of item the user wants to remove
			clearScreen()
			print(f"Too many items in cart. Please select {excessItems} items to be removed.\n\n")
			print(f"Paper count: {paperCount}")
			print(f"Tape count: {tapeCount}")
			print(f"Scissors count: {scissorCount}")
			removedItems = input("Which type of item would you like to remove? ").lower()

			if removedItems=="scissors" or removedItems=="paper" or removedItems=="tape": # determines if the input is a valid item type
				
				if removedItems == "scissors": #if selected item is scissors, remove the excess from it
					if scissorCount >= excessItems: #makes sure there is enough excess to be able to remove
						scissorCount -= excessItems
						selectedItems -= excessItems
						print(f"Removing {excessItems} {removedItems} from your cart.")
						input("[Press enter to continue]")
						remainingItems = 0
						break
					else: #if there aren't enough items to remove, run loop again
						print("\nNot enough scissors to remove. Please select a different item.")
						input("[Press enter to continue]")

				if removedItems == "paper": #if selected item is paper, remove the excess from it
					if paperCount >= excessItems: #makes sure there is enough excess to be able to remove
						paperCount -= excessItems
						selectedItems -= excessItems
						print(f"Removing {excessItems} {removedItems} from your cart.")
						input("[Press enter to continue]")
						remainingItems = 0
						break
					else: #if there aren't enough items to remove, run loop again
						print("\nNot enough reams of paper to remove. Plase select a different item.")
						input("[Press enter to continue]")

				if removedItems == "tape": #if selected item is tape, remove the excess from it
					if tapeCount >= excessItems: #makes sure there is enough excess to be able to remove
						tapeCount -= excessItems
						selectedItems -= excessItems
						print(f"Removing {excessItems} {removedItems} from your cart.")
						input("[Press enter to continue]")
						remainingItems = 0
						break
					else: #if there aren't enough items to remove, run loop again
						print("\nNot enough rolls of tape to remove. Please select a different item.")
						input("[Press enter to continue]")

			else: #if the input isn't "paper", "scissors", or "tape", run the loop again
				print("Invalid selection. Please try again.")
				input("[Press enter to continue]")

# Calculate the total cost of each category of items
scissorSum = scissorCount * scissorCost
tapeSum = tapeCount * tapeCost
paperSum = paperCount * paperCost


# Calculate the total sum of all items together
totalCost = scissorSum + tapeSum + paperSum

# Final output screen displaying breakdown of all chosen items
clearScreen()
print("Price breakdown:\n")
print(f"Scissors:\tQuantity: {scissorCount}\tCost per pair: ${scissorCost:.2f}\tCombined cost of all pairs of scissors: ${scissorSum:.2f}")
print(f"Tape:\t 	Quantity: {tapeCount}\tCost per roll: ${tapeCost:.2f}\tCombined cost of all rolls of tape: \t${tapeSum:.2f}")
print(f"Paper:\t 	Quantity: {paperCount}\tCost per ream: ${paperCost:.2f}\tCombined cost of all reams of paper: \t${paperSum:.2f}")
print(f"\nTotal number of materials: {selectedItems}")
print(f"Total cost of all materials: ${totalCost:.2f}")
input("\n[Press enter to exit...]")
clearScreen()