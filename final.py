import time
import threading
import getpass
import os
from dotenv import load_dotenv
from colorama import Fore, Style, init

# Initialize colorama for colored CLI output
init(autoreset=True)
load_dotenv()

# Global variables
all_orders = []
all_driver = []
all_customers = []
all_hotels = []

orders_done = []
orders_initiated = []
orders_dispatched = []
orders_accepted = []
orders_rejected = []
canceled_orders = []
speed = 5


# Utility Functions
def remove_item_from_list(item, list):
    star = None
    for i in range(len(list)):
        if list[i] == item:
            star = i
    if star is not None:
        list.pop(star)
        return 1
    return 0


def distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** (1 / 2)


# Classes
class Hotel:
    def __init__(self, name, location, menu):
        self.name = name
        self.location = location
        self.menu = menu

    def __repr__(self):
        return f"{Fore.CYAN}Hotel({self.name}, location={self.location})"


class DeliveryBoy:
    def __init__(self, name, status, location):
        self.name = name
        self.status = status
        self.location = location

    def __repr__(self):
        return f"{Fore.GREEN}{Style.BRIGHT}Driver({self.name}, status={self.status}, location={self.location})"


class Order:
    def __init__(self, dish, customer, hotel, type, fees):
        self.dish = dish
        self.customer = customer
        self.type = type
        self.status = "initiated"
        self.hotel = hotel
        self.driver = None
        self.fees = fees

    def __repr__(self):
        status_color = {
            "initiated": Fore.YELLOW,
            "accepted": Fore.GREEN,
            "dispatched": Fore.BLUE,
            "delivered": Fore.MAGENTA,
            "canceled": Fore.RED,
            "rejected": Fore.RED,
        }
        return (
            f"{status_color.get(self.status, Fore.WHITE)}Order(dish={self.dish}, type={self.type}, "
            f"hotel={self.hotel.name}, customer={self.customer}, status={self.status}, driver={self.driver}, fees={self.fees})"
        )


class Customer:
    def __init__(self, location):
        self.location = location  # [latitude, longitude]

    def __repr__(self):
        return f"{Fore.LIGHTBLUE_EX}Customer(location=[{self.location[0]}, {self.location[1]}])"


# Functions to Create Entities
def create_delivery_boy(name, location):
    new_boy = DeliveryBoy(name, "inactive", location)
    all_driver.append(new_boy)
    return new_boy


def create_customer(location):
    new_customer = Customer(location)
    all_customers.append(new_customer)
    return new_customer


def create_hotel(location, name, menu):
    new_hotel = Hotel(name, location, menu)
    all_hotels.append(new_hotel)
    return new_hotel


# Sample Data Creation (Default Entities)
create_customer([0, 5])
create_customer([6, 7])

create_hotel(
    [12, 16],
    "default hotel 1",
    {
        "starters": [
            {"name": "paneer tikka", "price": 100},
            {"name": "spring roll", "price": 100},
            {"name": "dry manchurian", "price": 100},
        ],
        "main course": [
            {"name": "dal", "price": 100},
            {"name": "naan", "price": 100},
            {"name": "paneer mumtaj", "price": 100},
        ],
        "beverages": [
            {"name": "cold coffee", "price": 100},
            {"name": "tea", "price": 100},
        ],
    },
)

create_hotel(
    [-12, 8],
    "default hotel 2",
    {
        "starters": [
            {"name": "paneer tikka", "price": 100},
            {"name": "spring roll", "price": 100},
            {"name": "dry manchurian", "price": 100},
        ],
        "main course": [
            {"name": "dal", "price": 100},
            {"name": "naan", "price": 100},
            {"name": "paneer mumtaj", "price": 100},
        ],
        "beverages": [
            {"name": "cold coffee", "price": 100},
            {"name": "tea", "price": 100},
        ],
    },
)

create_hotel(
    [2, 6],
    "default hotel 3",
    {
        "starters": [
            {"name": "paneer tikka", "price": 100},
            {"name": "spring roll", "price": 100},
            {"name": "dry manchurian", "price": 100},
        ],
        "main course": [
            {"name": "dal", "price": 100},
            {"name": "naan", "price": 100},
            {"name": "paneer mumtaj", "price": 100},
        ],
        "beverages": [
            {"name": "cold coffee", "price": 100},
            {"name": "tea", "price": 100},
        ],
    },
)



create_delivery_boy("default delivery boy 1", [0, 0])
create_delivery_boy("default delivery boy 2", [10, 0])

def nearest_driver_founder(driver_list,order):
    selected_driver = None
    best_distance = float('inf')

    # Try to find the best inactive driver
    for driver in driver_list:
        if driver.status == "inactive":
            dist = distance(order.hotel.location, driver.location) + distance(order.hotel.location, order.customer.location)
            if dist < best_distance:
                best_distance = dist
                selected_driver = driver
    
    return selected_driver


def get_valid_input(prompt, valid_options, validation_func=None):
    """Generic function to validate user input against allowed options"""
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_options:
            return user_input
        print(f"{Fore.RED}Invalid input! Please choose from: {', '.join(valid_options)}")

def get_valid_index(prompt, max_index):
    """Validate numerical indices within range"""
    while True:
        try:
            index = int(input(prompt)) - 1
            if 0 <= index < max_index:
                return index
            print(f"{Fore.RED}Index must be between 1 and {max_index}")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number")

# Modified exercise_as_customer function
def exercise_as_customer(customer):
    while True:
        choice = get_valid_input(
            f"\n{Fore.LIGHTCYAN_EX}Customer Powers:\n"
            f"{Fore.YELLOW}1) Place order\n{Fore.YELLOW}2) View status\n{Fore.YELLOW}3) Cancel order\n{Fore.YELLOW}4) Change cutomers location\n{Fore.YELLOW}5) Change user type\n"
            f"{Fore.YELLOW}Choose option (1-5): ",

            {'1', '2', '3', '4', '5'}
        )

        if choice == '1':
            # Hotel selection with validation
            print(f"\n{Fore.LIGHTCYAN_EX}Available hotels:")
            for i, hotel in enumerate(all_hotels, 1):
                print(f"{i}) {hotel}")
            
            hotel_index = get_valid_index(f"{Fore.YELLOW}Select hotel (1-{len(all_hotels)}): ", len(all_hotels))
            selected_hotel = all_hotels[hotel_index]

            # Dish selection with validation
            print(f"\n{Fore.LIGHTCYAN_EX}Menu:")
            valid_dishes = []
            for cat, items in selected_hotel.menu.items():
                print(f"{cat.capitalize()}:")
                for i, item in enumerate(items, 1):
                    print(f"  {i}) {item['name']} - ₹{item['price']}")
                    valid_dishes.append(item['name'].lower())
            dish=None
            while True:
                dish = input(f"{Fore.YELLOW}Select dish: ").lower()
                if dish in valid_dishes:
                    break
                print(f"{Fore.RED}Invalid dish! Please choose from the menu")

            # Order type validation
            order_type = get_valid_input(
                f"{Fore.YELLOW}Order type (normal/premium): ",
                {'normal', 'premium'}
            )


            #getting fees
            map_of_dishes=[]
            for key in list(selected_hotel.menu.keys()):
                
                map_of_dishes=map_of_dishes+selected_hotel.menu[key]
            fees=None
            for dish_ in map_of_dishes:
                if(dish_["name"].lower()==dish):
                    fees=dish_["price"]
                    


            # Create and store order
            new_order = Order(dish, customer, selected_hotel, order_type,fees)
            
            
            (all_orders.insert(0, new_order) if order_type == 'premium' 
            else all_orders.append(new_order))
            (orders_initiated.insert(0, new_order) if order_type == 'premium' 
             else orders_initiated.append(new_order))
            
            print(f"{Fore.GREEN}{Style.BRIGHT}Order initiated successfully!")

        elif choice == '2':
            # View order status with validation
            if len(cust_orders:=[o for o in all_orders if o.customer == customer])==0:
                print(f"{Fore.YELLOW}No orders found")
                continue
            
            print(f"\n{Fore.LIGHTCYAN_EX}Your orders:")
            for i, order in enumerate(cust_orders, 1):
                print(f"{i}) {order}")
            
            order_idx = get_valid_index(f"{Fore.YELLOW}Select order (1-{len(cust_orders)}): ", len(cust_orders))
            print(f"{Fore.CYAN}Status: {cust_orders[order_idx].status}")

        elif choice == '3':
            # Cancel order with validation
            cancel_orders = [o for o in all_orders if (o.customer == customer and (o.status=="accepted" or o.status=="initiated"))]
            if len(cancel_orders)==0:
                print(f"{Fore.YELLOW}No cancelable orders")
                continue
            
            print(f"\n{Fore.LIGHTCYAN_EX}Cancelable orders:")
            for i, order in enumerate(cancel_orders, 1):
                print(f"{i}) {order}")
            
            order_idx = get_valid_index(f"{Fore.YELLOW}Select order to cancel (1-{len(cancel_orders)}): ", len(cancel_orders))
            canceled_order = cancel_orders[order_idx]
            canceled_order.status = "canceled"
            if canceled_order in orders_accepted:
                orders_accepted.remove(canceled_order)
            elif canceled_order in orders_initiated:
                orders_initiated.remove(canceled_order)
            canceled_orders.append(canceled_order)
            print(f"{Fore.GREEN}{Style.BRIGHT}Order canceled successfully!")
        
        if choice=="4":
            while True:
                try:
                    x=int(input(f"{Fore.YELLOW}Enter new X coordinate: "))
                    break  
                except ValueError:
                    print(f"{Fore.RED}X coordinate must be a number\n")
            while True:
                try:
                    y=int(input(f"{Fore.YELLOW}Enter new Y coordinate: "))
                    break  
                except ValueError:
                    print(f"{Fore.RED}Y coordinate must be a number\n")
            customer.location=[x,y]
            print(f"{Fore.GREEN}{Style.BRIGHT}Customers location is changed")
        
        elif choice=="5":
            break 
        # if get_valid_input(f"\n{Fore.YELLOW}Continue as customer? (y/n): ", {'y', 'n'}) == 'n':
        #     break

# Apply similar validation patterns to:
# - exercise_as_admin()
# - exercise_as_hotel_manager()
# - main()

def exercise_as_admin():
    while True:
        print(f"\n{Fore.LIGHTCYAN_EX}Admin Powers:")
        print(f"{Fore.YELLOW}1) {Fore.RESET}View all orders")
        print(f"{Fore.YELLOW}2) {Fore.RESET}Add a new delivery boy")
        print(f"{Fore.YELLOW}3) {Fore.RESET}Add a new hotel")
        print(f"{Fore.YELLOW}4) {Fore.RESET}Add a new customer")
        print(f"{Fore.YELLOW}5) {Fore.RESET}View all hotels")
        print(f"{Fore.YELLOW}6) {Fore.RESET}View all delivery boys")
        print(f"{Fore.YELLOW}7) {Fore.RESET}View all orders (detailed)")
        print(f"{Fore.YELLOW}8) {Fore.RESET}Change user type")
        power = get_valid_input(
            f"\n{Fore.YELLOW}Which power do you want to exercise? (Enter 1-8): ", {'1', '2', '3', '4', '5', '6', '7', '8'}
        )

        if power == "1":
            print(f"\n{Fore.LIGHTCYAN_EX}All Orders:")
            for i, order in enumerate(all_orders, start=1):
                print(f"{i}) {order}")

        elif power == "2":
            name = input("Enter the name of the delivery boy: ").strip()
            x = int(input("Enter the initial X coordinate of the delivery boy: "))
            y = int(input("Enter the initial Y coordinate of the delivery boy: "))
            create_delivery_boy(name, [x, y])
            print(f"{Fore.GREEN}{Style.BRIGHT}Delivery boy {Fore.YELLOW}'{name}' {Fore.GREEN}{Style.BRIGHT}created successfully!")

        elif power == "3":
            x = int(input("Enter the X coordinate for the hotel: "))
            y = int(input("Enter the Y coordinate for the hotel: "))
            hotel_name = input("Enter the name of the hotel: ").strip()
            menu = {}
            categories = int(input("Enter the number of food categories you want to add: "))
            for _ in range(categories):
                category_name = input("Enter food category name: ").lower()
                num_items = int(input(f"Enter the number of items in '{category_name}' category: "))
                menu[category_name] = []
                for _ in range(num_items):
                    dish_name = input("Enter dish name: ")
                    price = float(input("Enter price of this dish: "))
                    menu[category_name].append({"name": dish_name, "price": price})
            create_hotel([x, y], hotel_name, menu)
            print(f"{Fore.GREEN}{Style.BRIGHT}Hotel {Fore.YELLOW}'{hotel_name}' {Fore.GREEN}{Style.BRIGHT}created successfully!")

        elif power == "4":
            x = int(input("Enter X coordinate for customer: "))
            y = int(input("Enter Y coordinate for customer: "))
            create_customer([x, y])
            print(f"{Fore.GREEN}{Style.BRIGHT}Customer created successfully at location ({x}, {y})!")

        elif power == "5":
            print(f"\n{Fore.LIGHTCYAN_EX}All Hotels:")
            for i, hotel in enumerate(all_hotels, start=1):
                print(f"{i}) {hotel}")

        elif power == "6":
            print(f"\n{Fore.LIGHTCYAN_EX}All Delivery Boys:")
            for i, driver in enumerate(all_driver, start=1):
                print(f"{i}) {driver}")

        elif power == "7":
            print(f"\n{Fore.LIGHTCYAN_EX}All Orders (Detailed):")
            for i, order in enumerate(all_orders, start=1):
                print(f"{i}) {order}")

        elif power == "8":
            break


def exercise_as_hotel_manager(hotel):
    linked_hotel = hotel

    while True:
        print(f"\n{Fore.LIGHTCYAN_EX}Hotel Manager Menu ({linked_hotel.name}):")
        print(f"{Fore.YELLOW}1) {Fore.RESET}Approve an order")
        print(f"{Fore.YELLOW}2) {Fore.RESET}Reject an order")
        print(f"{Fore.YELLOW}3) {Fore.RESET}View associated orders")
        print(f"{Fore.YELLOW}4) {Fore.RESET}Change user type")
        power = get_valid_input(
            f"\n{Fore.YELLOW}Which power do you want to exercise? (Enter 1/2/3/4): ", {'1', '2', '3', '4'}
        )

        order_list = [order for order in all_orders if order.hotel == linked_hotel]

        if power == "1":  # Approve an Order
            orders_to_approve = [order for order in order_list if order.status == "initiated"]

            if not orders_to_approve:
                print(f"\n{Fore.RED}No orders are available for approval.")
                continue

            print(f"\n{Fore.LIGHTCYAN_EX}Orders Available for Approval:")
            for i, order in enumerate(orders_to_approve, start=1):
                print(f"{i}) {order}")

            order_index = get_valid_index(
                f"\n{Fore.YELLOW}Select an order to approve (index starts from 1): ", len(orders_to_approve)
            )
            
            selected_order = orders_to_approve[order_index]
            selected_order.status = "accepted"

            if selected_order.type == "premium":
                orders_accepted.insert(0, selected_order)
            else:
                orders_accepted.append(selected_order)

            remove_item_from_list(selected_order, orders_initiated)
            
            print(f"\n{Fore.GREEN}{Style.BRIGHT}Order approved successfully!")

        elif power == "2":  # Reject an Order
            orders_to_reject = [order for order in order_list if order.status == "initiated"]

            if not orders_to_reject:
                print(f"\n{Fore.RED}No orders are available for rejection.")
                continue

            print(f"\n{Fore.LIGHTCYAN_EX}Orders Available for Rejection:")
            for i, order in enumerate(orders_to_reject, start=1):
                print(f"{i}) {order}")

            order_index = get_valid_index(
                f"\n{Fore.YELLOW}Select an order to reject (index starts from 1): ", len(orders_to_reject)
            )
            
            selected_order = orders_to_reject[order_index]
            selected_order.status = "rejected"

            orders_rejected.append(selected_order)
            
            remove_item_from_list(selected_order, orders_initiated)
            
            print(f"\n{Fore.GREEN}{Style.BRIGHT}Order rejected successfully!")

        elif power == "3":  # View Associated Orders
            associated_orders = [
                order for order in all_orders if order.hotel == linked_hotel and order.status != "canceled"
            ]

            if not associated_orders:
                print(f"\n{Fore.RED}No associated orders found.")
                continue

            print(f"\n{Fore.LIGHTCYAN_EX}Associated Orders:")
            
            for i, order in enumerate(associated_orders, start=1):
                status_color = {
                    "initiated": Fore.YELLOW,
                    "accepted": Fore.GREEN,
                    "dispatched": Fore.BLUE,
                    "delivered": Fore.MAGENTA,
                    "rejected": Fore.RED,
                }
                
                colorized_status = status_color.get(order.status, Fore.WHITE)
                
                print(
                    f"{i}) Dish: {order.dish}, Customer: {order.customer}, "
                    f"Status: {colorized_status}{order.status}{Style.RESET_ALL}"
                )
        elif power=="4":
            break
        

def meta_thread(order,associated_driver,associated_event):
    def func():
        while not associated_event.is_set():
            time.sleep(distance(associated_driver.location,order.hotel.location)/speed)
            order.status="dispatched"
            orders_accepted.remove(order)
            orders_dispatched.append(order)
            time.sleep(distance(order.customer.location,order.hotel.location)/speed)
            order.status="dilivered"
            orders_dispatched.remove(order)
            orders_done.append(order)
            associated_driver.status="inactive"
            order.fees=order.fees+distance(order.customer.location,order.hotel.location)*(0.05)
            associated_event.set()
    return func




def bg_thread():
    """Background thread to handle driver assignment."""
    while True:
        vele_drivers = [driver for driver in all_driver if driver.status == "inactive"]
        orders_to_check = [order for order in orders_accepted if order.driver==None ]
        if len(vele_drivers) > 0:
            orders_to_dispatch = orders_to_check[: len(vele_drivers)] if len(orders_to_check)>len(vele_drivers) else orders_to_check
            for order in orders_to_dispatch:
                #stopping thread mechanism
                assosiated_event=threading.Event()
                
                associated_driver = nearest_driver_founder(vele_drivers, order)
                if associated_driver!=None:
                    vele_drivers.remove(associated_driver)
                    order.driver=associated_driver
                    associated_driver.status="active"
                    threading.Thread(target=meta_thread(order,associated_driver,assosiated_event), daemon=True).start()
                    continue
                break
        # except Exception as e:
        #     print(f"{Fore.RED}Error in background thread: {e}")

def main():
    """Main function to handle CLI-based interactions."""
    print(f"{Fore.LIGHTCYAN_EX}Welcome to Swiggy CLI!")
    print(f"{Fore.LIGHTCYAN_EX}Basic commands are as follows:")
    print(
        f"{Fore.YELLOW}1) {Fore.CYAN}C {Fore.RESET}- Act as a Customer\n"
        f"{Fore.YELLOW}2) {Fore.CYAN}A {Fore.RESET}- Act as an Admin\n"
        f"{Fore.YELLOW}3) {Fore.CYAN}H {Fore.RESET}- Act as a Hotel Manager\n"
    )

    # Start the background thread for driver assignment
    threading.Thread(target=bg_thread, daemon=True).start()

    try:
        while True:
            # Prompt user to choose a role
            controls = get_valid_input(
                f"\n{Fore.LIGHTCYAN_EX}What do you want to be? {Fore.YELLOW}(C/A/H): ", 
                {'c', 'a', 'h'}
            ).upper()

            if controls == "A":  # Admin Role
                password = getpass.getpass(f"{Fore.LIGHTCYAN_EX}Enter your password: ")
                if password == os.getenv("password"):
                    print(f"{Fore.GREEN}{Style.BRIGHT}Access granted!")
                    exercise_as_admin()
                else:
                    print(f"{Fore.RED}Incorrect password. Access denied.")

            elif controls == "C":  # Customer Role
                if not all_customers:
                    print(f"\n{Fore.RED}No customers available. Please add customers first.")
                    continue

                print(f"\n{Fore.LIGHTCYAN_EX}These are all our current customers:")
                for i, customer in enumerate(all_customers, start=1):
                    print(f"{i}) {customer}")

                customer_index = get_valid_index(
                    f"\n{Fore.YELLOW}Select your customer index (starting from 1): ", 
                    len(all_customers)
                )
                exercise_as_customer(all_customers[customer_index])

            elif controls == "H":  # Hotel Manager Role
                if not all_hotels:
                    print(f"\n{Fore.RED}No hotels available. Please add hotels first.")
                    continue

                print(f"\n{Fore.LIGHTCYAN_EX}These are all our current associated hotels:")
                for i, hotel in enumerate(all_hotels, start=1):
                    print(f"{i}) {hotel}")

                hotel_index = get_valid_index(
                    f"\n{Fore.YELLOW}Select your hotel index (starting from 1): ", 
                    len(all_hotels)
                )
                exercise_as_hotel_manager(all_hotels[hotel_index])

    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C
        print(f"\n{Fore.RED}Exiting... Goodbye!")

if __name__ == "__main__":
    main()

