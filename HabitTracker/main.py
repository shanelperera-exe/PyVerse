import os
import time
import socket
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Force IPv4 in WSL to prevent DNS name resolution timeouts
orig_getaddrinfo = socket.getaddrinfo
def getaddrinfo_ipv4(host, port, family=0, type=0, proto=0, flags=0):
    try:
        return orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
    except socket.gaierror:
        time.sleep(0.5)
        return orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
socket.getaddrinfo = getaddrinfo_ipv4

PIXELA_ENDPOINT = "https://pixe.la/v1/users"
USERNAME = os.environ.get("PIXELA_USERNAME", "shanelperera")
TOKEN = os.environ.get("PIXELA_TOKEN")

if not TOKEN:
    print("\n❌ Error: PIXELA_TOKEN is not set.")
    print("Please add your token to HabitTracker/.env:")
    print("  PIXELA_TOKEN=your_token_here")
    exit(1)

HEADERS = {
    "X-USER-TOKEN": TOKEN,
    "User-Agent": "Mozilla/5.0"
}

def main():
    print("\n" * 26)
    print("""\n██╗  ██╗ █████╗ ██████╗ ██████╗ ██╗████████╗    ████████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗ 
██║  ██║██╔══██╗██╔══██╗██╔══██╗██║╚══██╔══╝    ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
███████║███████║██████╔╝██████╔╝██║   ██║          ██║   ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝
██╔══██║██╔══██║██╔══██╗██╔══██╗██║   ██║          ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
██║  ██║██║  ██║██████╔╝██████╔╝██║   ██║          ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚═╝   ╚═╝          ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝""")
    print("-" * 105)
    print("\033[1;32;40mMotivation gets you started, Habit keeps you going!\033[0m\n")
    print("Welcome to Habit Tracker!\n")

    print("This application requires a Pixela account. More info: \033[1;34mhttps://pixe.la\033[0m")
    print("Don't have a Pixela account? \033[1;34m[C] Create Account!\033[0m\n")
    print("\033[1;31m[1]\033[0m Create a habit")
    print("\033[1;31m[2]\033[0m Add data to a habit")
    print("\033[1;31m[3]\033[0m Update data of a habit")
    print("\033[1;31m[4]\033[0m Delete data from a habit")
    print("\033[1;31m[5]\033[0m View current habits")

    valid_options = ["1", "2", "3", "4", "5", 'c']
    while True:
        user_input = input("\nSelect an option:").strip().lower()
        if user_input not in valid_options:
            print("Invalid input. Try again.")
            continue
        else:
            break

    match user_input:
        case 'c':
            create_account()
        case "1":
            create_habit()
        case "2":
            graph_id = select_graph()
            if graph_id:
                add_data(graph_id)
        case "3":
            graph_id = select_graph()
            if graph_id:
                update_data(graph_id)
        case "4":
            graph_id = select_graph()
            if graph_id:
                delete_data(graph_id)
        case "5":
            view_graphs()

def create_account():
    user_params = {
        "token": TOKEN,
        "username": USERNAME,
        "agreeTermsOfService": "yes",
        "notMinor": "yes"
    }

    while True:
        try:
            # Creating Pixela account
            response = requests.post(url=PIXELA_ENDPOINT, json=user_params, timeout=10)
            response.raise_for_status()

            # Success message
            print("Account created successfully!")
            print(response.text)
            break  # Exit the loop on success

        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 503:
                print("Pixela service is unavailable. Please try again later.")
            else:
                print(f"HTTP error occurred: {http_err}")
            retry = input("Would you like to retry? (Y/N): ").strip().lower()
            if retry != 'y':
                print("Exiting account creation.")
                break

        except Exception as e:
            print(f"An error occurred: {e}")
            retry = input("Would you like to retry? (Y/N): ").strip().lower()
            if retry != 'y':
                print("Exiting account creation.")
                break

def create_habit():
    graph_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs"

    while True:
        try:
            # Prompt user for graph details
            graph_id = input("Enter a unique Graph ID: ").strip()
            graph_name = input("Enter a name for the habit (graph): ").strip()
            unit = input("Enter the unit for measurement (e.g., Km, hours, pages): ").strip()
            data_type = input("Enter the type of data (int or float): ").strip()
            color = input("Enter a color (choose from `shibafu`, `momiji`, `sora`, `ichou`, `ajisai`, `kuro`): ").strip()

            # Validate inputs
            if data_type not in ["int", "float"]:
                print("Invalid data type. Please enter 'int' or 'float'.")
                continue

            graph_config = {
                "id": graph_id,
                "name": graph_name,
                "unit": unit,
                "type": data_type,
                "color": color
            }

            headers = HEADERS

            # Creating the graph
            response = requests.post(url=graph_endpoint, json=graph_config, headers=headers, timeout=10)
            response.raise_for_status()

            print("Graph created successfully!")
            print(f"Graph ID: {graph_id}")
        
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 503:
                print("Pixela service is unavailable. Please try again later.")
            else:
                print(f"HTTP error occurred: {http_err}")
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
        finally:
            # Prompt user for next action
            action = input("\nWhat would you like to do next?\n"
                           "[1] Create another habit\n"
                           "[2] Return to the main menu\n"
                           "[3] Exit\n"
                           "Select an option: ").strip()
            if action == "1":
                continue
            elif action == "2":
                main()  # Return to the main menu
                break
            elif action == "3":
                print("Exiting the application. Goodbye!")
                exit()
            else:
                print("Invalid input. Returning to the main menu.")
                main()
                break

def add_data(graph_id):
    pixel_creation_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{graph_id}"

    while True:
        try:
            date = input("Enter the date (YYYYMMDD) for the data (or press Enter for today): ").strip()
            if not date:
                date = datetime.now().strftime("%Y%m%d")

            quantity = input("Enter the quantity for this date: ").strip()

            # Validate quantity input
            if not quantity.replace('.', '', 1).isdigit():  # Check if the quantity is a valid number (int or float)
                print("Invalid quantity. Please enter a valid number.")
                continue

            pixel_data = {
                "date": date,
                "quantity": quantity
            }

            headers = HEADERS

            # Adding data
            response = requests.post(url=pixel_creation_endpoint, json=pixel_data, headers=headers, timeout=10)
            response.raise_for_status()

            print("Data added successfully!")
            print(response.text)
        
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 503:
                print("Pixela service is unavailable. Please try again later.")
            else:
                print(f"HTTP error occurred: {http_err}")
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
        finally:
            # Prompt user for next action
            action = input("\nWhat would you like to do next?\n"
                           "[1] Add data to another date\n"
                           "[2] Return to the main menu\n"
                           "[3] Exit\n"
                           "Select an option: ").strip()
            if action == "1":
                continue
            elif action == "2":
                main()  # Return to the main menu
                break
            elif action == "3":
                print("Exiting the application. Goodbye!")
                exit()
            else:
                print("Invalid input. Returning to the main menu.")
                main()
                break

def update_data(graph_id):
    pixel_creation_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{graph_id}"

    while True:
        try:
            date = input("Enter the date (YYYYMMDD) to update: ").strip()
            quantity = input("Enter the new quantity for this date: ").strip()

            # Validate quantity input
            if not quantity.replace('.', '', 1).isdigit():  # Check if the quantity is a valid number
                print("Invalid quantity. Please enter a valid number.")
                continue

            update_pixel_endpoint = f"{pixel_creation_endpoint}/{date}"
            updated_pixel_data = {
                "quantity": quantity
            }

            headers = HEADERS

            # Updating data
            response = requests.put(url=update_pixel_endpoint, json=updated_pixel_data, headers=headers, timeout=10)
            response.raise_for_status()

            print("Data updated successfully!")
            print(response.text)

        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 503:
                print("Pixela service is unavailable. Please try again later.")
            else:
                print(f"HTTP error occurred: {http_err}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        finally:
            # Prompt user for next action
            action = input("\nWhat would you like to do next?\n"
                           "[1] Update another date\n"
                           "[2] Return to the main menu\n"
                           "[3] Exit\n"
                           "Select an option: ").strip()
            if action == "1":
                continue
            elif action == "2":
                main()  # Return to the main menu
                break
            elif action == "3":
                print("Exiting the application. Goodbye!")
                exit()
            else:
                print("Invalid input. Returning to the main menu.")
                main()
                break

def delete_data(graph_id):
    pixel_creation_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{graph_id}"

    while True:
        try:
            date = input("Enter the date (YYYYMMDD) to delete: ").strip()

            delete_pixel_endpoint = f"{pixel_creation_endpoint}/{date}"

            headers = HEADERS

            # Deleting data
            response = requests.delete(url=delete_pixel_endpoint, headers=headers, timeout=10)
            response.raise_for_status()

            print("Data deleted successfully!")
            print(response.text)

        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 503:
                print("Pixela service is unavailable. Please try again later.")
            else:
                print(f"HTTP error occurred: {http_err}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        finally:
            # Prompt user for next action
            action = input("\nWhat would you like to do next?\n"
                           "[1] Delete data from another date\n"
                           "[2] Return to the main menu\n"
                           "[3] Exit\n"
                           "Select an option: ").strip()
            if action == "1":
                continue
            elif action == "2":
                main()  # Return to the main menu
                break
            elif action == "3":
                print("Exiting the application. Goodbye!")
                exit()
            else:
                print("Invalid input. Returning to the main menu.")
                main()
                break

def view_graphs():
    graph_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs"

    while True:
        try:
            headers = HEADERS

            # Fetching graphs
            response = requests.get(url=graph_endpoint, headers=headers, timeout=10)
            response.raise_for_status()

            graphs = response.json()  # Parsing response as JSON
            print("\nYour Current Graphs:")
            if "graphs" in graphs and graphs["graphs"]:
                for graph in graphs["graphs"]:
                    graph_link = f"https://pixe.la/v1/users/{USERNAME}/graphs/{graph['id']}.html"
                    print(f"Graph ID: {graph['id']}, Name: {graph['name']}, Unit: {graph['unit']}, Color: {graph['color']}")
                    print(f"View Graph: \033[1;34m{graph_link}\033[0m\n")
            else:
                print("No graphs found! Create one first.")
            break  # Exit the loop on success

        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 503:
                print("Pixela service is unavailable. Please try again later.")
            else:
                print(f"HTTP error occurred: {http_err}")
            retry = input("Would you like to retry? (Y/N): ").strip().lower()
            if retry != 'y':
                print("Exiting view graphs operation.")
                break

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            retry = input("Would you like to retry? (Y/N): ").strip().lower()
            if retry != 'y':
                print("Exiting view graphs operation.")
                break

def select_graph():
    graph_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs"

    headers = HEADERS

    # Fetching the list of graphs
    response = requests.get(url=graph_endpoint, headers=headers, timeout=10)
    response.raise_for_status()
    graphs = response.json()

    if "graphs" not in graphs or len(graphs["graphs"]) == 0:
        print("No graphs available. Create a graph first.")
        return None

    print("\nAvailable Graphs:")
    for graph in graphs["graphs"]:
        print(f"Graph ID: {graph['id']}, Name: {graph['name']}, Unit: {graph['unit']}, Color: {graph['color']}")

    while True:
        selected_graph_id = input("\nEnter the Graph ID to use: ").strip()
        if any(graph["id"] == selected_graph_id for graph in graphs["graphs"]):
            print(f"Selected Graph ID: {selected_graph_id}")
            return selected_graph_id
        else:
            print("Invalid Graph ID. Please try again.")

if __name__ == "__main__":
    main()
