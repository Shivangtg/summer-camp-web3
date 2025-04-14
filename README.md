# 🛵 Food Delivery CLI Simulator

A Python-based Command Line Interface (CLI) program that simulates a food delivery system similar to Swiggy. It models real-world entities like delivery personnel, hotel managers, customers, and a central admin. The program uses multithreading to simulate real-time order delivery operations.

---

## 🚀 Features

- **Object-Oriented Design**
  - Classes represent real-world roles:
    - `DeliveryBoy`
    - `SwiggyAdmin`
    - `HotelManager`
    - `Customer`

- **Multithreading with `threading` Library**
  - Each order is processed in a separate thread.
  - New threads are spawned **only when a delivery boy is available**, mimicking realistic delivery constraints.

- **Colored Output using `colorama`**
  - Enhances CLI readability and user interaction with color-coded messages.

---

## ⚙️ Functionalities

- Create and manage:
  - Delivery boys
  - Hotels
  - Customers
- Simulate:
  - Food order placement
  - Delivery timing using threads
  - Availability of delivery personnel
- Track:
  - Active and completed deliveries
  - Idle and busy delivery boys
  - Hotel and customer details

---

## 📦 Tech Stack

- **Language**: Python
- **Libraries**:
  - [`threading`](https://docs.python.org/3/library/threading.html) - for concurrency and simulating real-time deliveries
  - [`colorama`](https://pypi.org/project/colorama/) - for colored terminal output

