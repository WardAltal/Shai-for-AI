def calculate_total_sales(book_price, quantity_sold):
    """
    This function calculates the total sales.
    Parameters:
    - book_price (float): The price of a single book.
    - quantity_sold (int): The number of books sold.

    Returns:
    - total_sales (float): The total sales amount.
    """
    total_sales = book_price * quantity_sold  # Multiply price by quantity
    return total_sales  # Return the result

print("Welcome to the Bookstore Sales Calculator!")

price = float(input("Enter the price of a single book: "))

quantity = int(input("Enter the number of books sold: "))

total = calculate_total_sales(price, quantity)

print(f"Total sales for today: ${total:.2f}")
