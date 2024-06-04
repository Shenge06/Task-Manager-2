import datetime


# Function to load user data from 'user.txt' file into a dictionary
def load_user_data():
    """Load user data from the 'user.txt' file into a dictionary."""
    user_data = {}
    try:
        with open('user.txt', 'r') as user_file:
            # Read each line in the file, split by ', ', and store in the dictionary
            for line in user_file:
                username, password = line.strip().split(', ')
                user_data[username] = password
    except FileNotFoundError:
        print("Error: User file not found.")

    return user_data

# Function to save user data to the 'user.txt' file
def save_user_data(user_data):
    """Save user data to the 'user.txt' file."""
    with open('user.txt', 'w') as user_file:
        # Write each username and password pair to the file
        for username, password in user_data.items():
            user_file.write(f"{username}, {password}\n")

# Function to print details of a task
def print_task_details(task_info):
    """Print task details."""
    if len(task_info) >= 6: 
        print("\nAssigned to:", task_info[0]) 
        print("Title:", task_info[1])
        print("Description:", task_info[2]) 
        print("Due Date:", task_info[3]) 
        print("Date Created:", task_info[4]) 
        print("Status:", task_info[5]) 
    else: 
        print("Invalid task data. Unable to print details.") 

# Function to register a new user
def reg_user(user_data, admin_username='admin'):
    """Register a new user."""
    while True:
        new_username = input("Enter a new username: ")
        new_password = input("Enter a new password: ")
        confirm_password = input("Confirm your password: ")

        if new_password == confirm_password:
            if new_username not in user_data:
                # Add the new user to the user_data dictionary and save to file
                user_data[new_username] = new_password
                save_user_data(user_data)
                print("Registration successful!")
                break
            else:
                print("Username already exists. Please try a different username.")
        else:
            print("Passwords do not match. Registration failed.")

    return user_data

# Function to add a new task
def add_task(user_data):
    """Add a new task."""
    task_username = input("Enter the username of the person the task is assigned to ('b' to go back, 'e' to exit): ")

    if task_username.lower() == 'b':
        return
    elif task_username.lower() == 'e':
        print('Goodbye!!!')
        exit()

    # Check if the user exists
    if task_username not in user_data:
        print("User not found. Please register the user first.")
        return

    # Prompt user for task details and handle date input validation
    task_title = input("Enter the title of the task: ")
    task_description = input("Enter the description of the task: ")

    while True:
        try:
            task_due_date = input("Enter the due date of the task (YYYY-MM-DD): ")
            datetime.datetime.strptime(task_due_date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    # Get the current date and time
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    try:
        # Append the new task to the 'tasks.txt' file
        with open('tasks.txt', 'a', newline='') as task_file:
            task_file.write("{}, {}, {}, {}, {}, {}\n".format(task_username, task_title, task_description, task_due_date, current_date, "No"))
            task_file.write('\n') # Add a newline character
    except FileNotFoundError:
        print("Error: Tasks file not found.")
    except Exception as e:
        print(f"Error: {e}")

    print("Task added successfully!")

    # Ask the user if they want to mark the task as complete
    while True:
        completion_input = input("Do you want to mark the task as complete? (Enter 'Yes' or 'No'): ").lower()
        if completion_input in ['yes', 'no']:
            break
        else:
            print("Invalid input. Please enter 'Yes' or 'No'.")

    if completion_input == 'yes':
        mark_as_complete(task_username, task_title)

# Function to mark a task as complete
def mark_as_complete(username, title):
    """Mark a task as complete."""
    # Check if the task exists
    task_found = False
    tasks = []  # to store tasks temporarily
    with open('tasks.txt', 'r') as task_file:
        for line in task_file:
            task_data = line.strip().split(', ')
            if task_data[0] == username and task_data[1] == title:
                task_found = True
                tasks.append("{}, {}, {}, {}, {}, {}\n".format(task_data[0], task_data[1], task_data[2], task_data[3], task_data[4], "Yes"))
            else:
                tasks.append(line)

    if not task_found:
        print("Task not found.")
        return

    # Update tasks.txt with the modified task list
    with open('tasks.txt', 'w') as task_file:
        task_file.writelines(tasks)

    print("Task marked as complete successfully!")

    # Reload tasks after marking a task as complete
    tasks = load_tasks()

# Function to load tasks from the 'tasks.txt' file
def load_tasks():
    """Load tasks from the 'tasks.txt' file."""
    try:
        with open('tasks.txt', 'r') as task_file:
            tasks = task_file.readlines()
        return tasks
    except FileNotFoundError:
        print("Error: Tasks file not found.")
        return []

# Modify the view_mine function to use the updated mark_as_complete function
def view_mine(username_input, tasks):
    """View tasks assigned to the logged-in user."""
    if tasks:
        for i, task in enumerate(tasks, start=1):
            task_info = task.strip().split(', ')
            if task_info[0] == username_input:
                print(f"{i}.", end=" ")
                print_task_details(task_info)

        print(f"{i + 1}. Return to the main menu")
        task_choice = int(input("Choose a task number (-1 to return): "))
        
        if task_choice == -1:
            return tasks
        elif 1 <= task_choice <= i:
            task_info = tasks[task_choice - 1].strip().split(', ')
            edit_or_mark = input("Do you want to (e)dit or (m)ark the task as complete? ").lower()
            if edit_or_mark == 'e' and task_info[5] == 'No':
                # Edit task details if the task is not marked as complete
                new_username = input("Enter the new username: ")
                new_due_date = input("Enter the new due date (YYYY-MM-DD): ")
                task_info[0] = new_username
                task_info[3] = new_due_date
                with open('tasks.txt', 'w') as task_file:
                    task_file.writelines(tasks)
                print("Task edited successfully!")
            elif edit_or_mark == 'm' and task_info[5] == 'No':
                # Mark the task as complete if it is not already marked
                mark_as_complete(task_info[0], task_info[1])
                # Reload tasks after marking a task as complete
                tasks = load_tasks()
            elif task_info[5] == 'Yes':
                print("Task is already marked as complete and cannot be edited or marked.")
            else:
                print("Invalid choice.")
        elif task_choice == i + 1:
            return tasks
        else:
            print("Invalid task number.")
    else:
        print("No tasks found for this user.")

    return tasks


# Function to view all tasks
def view_all():
    """View all tasks."""
    try:
        with open('tasks.txt', 'r') as task_file:
            tasks = task_file.readlines()

            if tasks:
                for task in tasks:
                    task_info = task.strip().split(', ')
                    print_task_details(task_info)
            else:
                print("No tasks found.")
    except FileNotFoundError:
        print("Error: Tasks file not found.")


# Function to view tasks assigned to the logged-in user
def view_mine(username_input, tasks):
    """View tasks assigned to the logged-in user."""
    if tasks:
        for i, task in enumerate(tasks, start=1):
            task_info = task.strip().split(', ')
            if task_info[0] == username_input:
                print(f"{i}.", end=" ")
                print_task_details(task_info)

        print(f"{i + 1}. Return to the main menu")
        task_choice = int(input("Choose a task number (-1 to return): "))
        
        if task_choice == -1:
            return tasks
        elif 1 <= task_choice <= i:
            task_info = tasks[task_choice - 1].strip().split(', ')
            edit_or_mark = input("Do you want to (e)dit or (m)ark the task as complete? ").lower()
            if edit_or_mark == 'e' and task_info[5] == 'No':
                # Edit task details if the task is not marked as complete
                new_username = input("Enter the new username: ")
                new_due_date = input("Enter the new due date (YYYY-MM-DD): ")
                task_info[0] = new_username
                task_info[3] = new_due_date
                with open('tasks.txt', 'w') as task_file:
                    task_file.writelines(tasks)
                print("Task edited successfully!")
            elif edit_or_mark == 'm' and task_info[5] == 'No':
                # Mark the task as complete if it is not already marked
                mark_as_complete(task_info[0], task_info[1])
            elif task_info[5] == 'Yes':
                print("Task is already marked as complete and cannot be edited or marked.")
            else:
                print("Invalid choice.")
        elif task_choice == i + 1:
            return tasks
        else:
            print("Invalid task number.")
    else:
        print("No tasks found for this user.")

    return tasks

# Function to generate reports and save them to 'task_overview.txt' and 'user_overview.txt'
def generate_reports():
    """Generate reports and save them to 'task_overview.txt' and 'user_overview.txt'."""
    try:
        # Task overview
        with open('tasks.txt', 'r') as task_file:
            tasks = task_file.readlines()
            total_tasks = len(tasks)
            completed_tasks = sum(len(task.strip().split(', ')) >= 6 and task.strip().split(', ')[5] == 'Yes' for task in tasks)
            uncompleted_tasks = total_tasks - completed_tasks
            overdue_tasks = 0

            for task in tasks:
                task_info = task.strip().split(', ')
                if len(task_info) >= 6:
                    due_date_str = task_info[3]

                    try:
                        due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d")
                    except ValueError:
                        try:
                            due_date = datetime.datetime.strptime(due_date_str, "%d %b %Y")
                        except ValueError:
                            continue

                    if due_date < datetime.datetime.now() and task_info[5] == 'No':
                        overdue_tasks += 1

            incomplete_percentage = (uncompleted_tasks / total_tasks) * 100 if total_tasks > 0 else 0
            overdue_percentage = (overdue_tasks / uncompleted_tasks) * 100 if uncompleted_tasks > 0 else 0

        with open('task_overview.txt', 'w') as task_overview_file:
            task_overview_file.write(f"Total tasks: {total_tasks}\n")
            task_overview_file.write(f"Completed tasks: {completed_tasks}\n")
            task_overview_file.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
            task_overview_file.write(f"Overdue tasks: {overdue_tasks}\n")
            task_overview_file.write(f"Percentage of incomplete tasks: {incomplete_percentage:.2f}%\n")
            task_overview_file.write(f"Percentage of overdue tasks: {overdue_percentage:.2f}%\n")

        # User overview
        with open('user.txt', 'r') as user_file:
            users = user_file.readlines()
            total_users = len(users)
            # Add user-related calculations 

        with open('user_overview.txt', 'w') as user_overview_file:
            user_overview_file.write(f"Total users: {total_users}\n")
            # Add user-related information 

        print("Reports generated successfully!")

    except FileNotFoundError as e:
        print(f"Error: {e.filename} not found.")


# Function to display statistics
def display_statistics():
    """Display statistics of tasks."""
    try:
        with open('task_overview.txt', 'r') as task_overview_file:
            # Read and print the content of the task overview file
            task_overview = task_overview_file.read()
            print(task_overview)
    except FileNotFoundError:
        print("Error: Task overview file not found.")

# Main program

# Load user data
user_data = load_user_data()

while True:
    # Prompt the user for login credentials
    username_input = input("Enter your username: ")
    password_input = input("Enter your password: ")

    # Check if the entered username and password are valid
    if username_input in user_data and password_input == user_data[username_input]:
        print("Login successful! Welcome, " + username_input + "!")
        
        # Load tasks
        try:
            with open('tasks.txt', 'r') as task_file:
                tasks = task_file.readlines()
        except FileNotFoundError:
            tasks = []

        # Process the user's choice based on their role
        if username_input == "admin":
            while True:
                # Display the admin menu and prompt for choice
                menu = input('''Select one of the following options:
                    r - register a user
                    a - add task
                    va - view all tasks
                    vm - view my tasks
                    g - generate reports
                    s - display statistics
                    e - exit
                    : ''').lower()

                # Process admin menu options
                if menu == 'r':
                    user_data = reg_user(user_data)
                elif menu == 'a':
                    add_task(user_data)
                elif menu == 'va':
                    view_all()
                elif menu == 'vm':
                    tasks = view_mine(username_input, tasks)
                elif menu == 'g':
                    generate_reports()
                elif menu == 's':
                    display_statistics()
                elif menu == 'e':
                    print('Goodbye!!!')
                    exit()
                else:
                    print("You have entered an invalid input. Please try again.")
        else:
            while True:
                # Display the user menu and prompt for choice
                menu = input('''Select one of the following options:
                    a - add task
                    va - view all tasks
                    vm - view my tasks
                    g - generate reports
                    e - exit
                    : ''').lower()

                # Process user menu options
                if menu == 'a':
                    add_task(user_data)
                elif menu == 'va':
                    view_all()
                elif menu == 'vm':
                    tasks = view_mine(username_input, tasks)
                elif menu == 'g':
                    generate_reports()
                elif menu == 'e':
                    print('Goodbye!!!')
                    exit()
                else:
                    print("You have entered an invalid input. Please try again.")
    else:
        print("Invalid username or password. Please try again.")



        
