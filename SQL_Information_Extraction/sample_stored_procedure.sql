DELIMITER //

CREATE PROCEDURE GetCustomerOrders(
    IN customerId INT,
    IN startDate DATE,
    IN endDate DATE
)
BEGIN
    SELECT o.order_id, o.order_date, o.total_amount
    FROM orders o
    WHERE o.customer_id = customerId
      AND o.order_date BETWEEN startDate AND endDate
    ORDER BY o.order_date DESC;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE UpdateProductStock(
    IN productId INT,
    IN quantityChange INT,
    OUT newStock INT
)
BEGIN
    UPDATE products
    SET stock_quantity = stock_quantity + quantityChange
    WHERE product_id = productId;

    SELECT stock_quantity INTO newStock
    FROM products
    WHERE product_id = productId;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE AddNewEmployee(
    IN firstName VARCHAR(50),
    IN lastName VARCHAR(50),
    IN department VARCHAR(50),
    IN salary DECIMAL(10,2)
)
BEGIN
    INSERT INTO employees (first_name, last_name, department, salary, hire_date)
    VALUES (firstName, lastName, department, salary, CURDATE());
END //

DELIMITER ;
