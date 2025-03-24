--------------------------------------------------------------------------
-- CRUD for Rewards page 
--------------------------------------------------------------------------
--INSERTs a new person into the Rewards_customers table
INSERT INTO `Rewards_customers` (`name`, `phone`, `email`, `address`, `points`)
    VALUES(:name, :phone,:email, :address, :points),

--SELECTS a Person from the Rewards_customers table
SELECT name, phone, email, address, points
    FROM Rewards_customers
    WHERE rewardCustomerId = :rewardCustomerId;

--UPDATEs a person from Rewards_customers table using RewardsID 
UPDATE Rewards_customers
    SET name = :newCustomerName, phone = :newPhone, email = :newEmail, address = :newAddress, points = :newPoints
    WHERE rewardCustomerId = :rewardCustomerId;

--DELETEs a person from Rewards_customers table using RewardsID 
DELETE Rewards_customers
    WHERE rewardCustomerId = :rewardCustomerId;
--------------------------------------------------------------------------
-- End of CRUD for Rewards page 
--------------------------------------------------------------------------

--------------------------------------------------------------------------
-- CRUD for Transaction page 
--------------------------------------------------------------------------
-- INSERT a new transaction
INSERT INTO `Sales_transactions`(`storeId`, `date`, `rewardCustomerId`, `total`, `pointsApplied`, `finalAmount`)
    VALUES(:storeId, :date, :rewardCustomerId, :total, :pointsApplied, :finalAmount);

-- SELECTs a transaction
SELECT Sales_transactions.saleTransactionId, Stores.name as storeName, date, Rewards_customers.name as rewardCustomerName, 
total, pointsApplied, finalAmount
    FROM Sales_transactions
        INNER JOIN Stores ON Sales_transactions.storeId = Stores.storeId
        INNER JOIN Rewards_customers ON Sales_transactions.rewardCustomerId =Rewards_customers.rewardCustomerId
    WHERE saleTransactionId = :saleTransactionId;

-- SELECTS all transactions
SELECT Sales_transactions.saleTransactionId, Stores.name as storeName, date, Rewards_customers.name as rewardCustomerName, total, pointsApplied, finalAmount
    FROM Sales_transactions
        INNER JOIN Stores ON Sales_transactions.storeId = Stores.storeId
        LEFT JOIN Rewards_customers ON Sales_transactions.rewardCustomerId =Rewards_customers.rewardCustomerId
--------------------------------------------------------------------------
-- End of CRUD for Transaction page 
--------------------------------------------------------------------------

--------------------------------------------------------------------------
-- CRUD for transaction_details page 
--------------------------------------------------------------------------
-- INSERT a new transaction_detail
INSERT INTO `Sales_transactions_details` (`saleTransactionId`, `productId`, `quantity`, `total`)
    VALUES(:saleTransactionId, :productId, :quantity, :total);

-- SELECTs a transaction_detail
SELECT * FROM Sales_transactions_details
    WHERE saleTransactionDetailId = :saleTransactionDetailId;

-- SELECTs all transaction details
SELECT Sales_transactions_details.saleTransactionDetailId, Sales_transactions_details.saleTransactionId, Products.name as productName, Sales_transactions_details.quantity, Sales_transactions_details.total
    FROM Sales_transactions_details
        INNER JOIN Products ON Sales_transactions_details.productId = Products.productId;
--------------------------------------------------------------------------
-- End of CRUD for transaction_details page 
--------------------------------------------------------------------------

--------------------------------------------------------------------------
-- CRUD for Products page 
--------------------------------------------------------------------------
--INSERTs a new product into the Products table
INSERT INTO Products (name, model, description)
    VALUES (:nameInput, :modelInput, :descriptionInput);

--SELECTS all products from the Products table
SELECT Products.productId, Products.name, Products.model, Products.description
    FROM Products;

--SELECTS a product from the Products table
SELECT Products.productId, Products.name, Products.model, Products.description
    FROM Products
    WHERE  Products.productId = :productId;

--SELECTS All product productIds, names, and models from the Products table for dropdown search
SELECT Products.productId, Products.name, Products.model
    FROM Products;
--------------------------------------------------------------------------
-- End of CRUD for Products page 
--------------------------------------------------------------------------

--------------------------------------------------------------------------
-- CRUD for Stores page 
--------------------------------------------------------------------------
--INSERTs a new store into the Stores table
INSERT INTO Stores (name, city, street, streetAddress)
    VALUES (:nameInput, :cityInput, :streetInput, streetAddressInput);

--SELECTS all stores from the Stores table
SELECT Stores.storeId, Stores.name, Stores.city, Stores.state, Stores.streetAddress
    FROM Stores;

--SELECTS a store from the Stores table
SELECT Stores.storeId, Stores.name, Stores.city, Stores.state, Stores.streetAddress
    FROM Stores
    WHERE  Stores.storeId = :storeId;

--SELECTS All store storeIds, names, and states, and citys from the Stores table for dropdown search
SELECT Stores.storeId, Stores.name, Stores.city, Stores.state
    FROM Stores;
--------------------------------------------------------------------------
-- End of CRUD for Stores page 
--------------------------------------------------------------------------

--------------------------------------------------------------------------
-- CRUD for Stores_products_details page 
--------------------------------------------------------------------------
--INSERTs a new store_product_detail instance into the Stores_products_details table
INSERT INTO stores_products_details (storeId, productId, count, price)
    VALUES (storeIdInput, productIdInput, countInput, priceInput);

--SELECTS all store_product_detail instances from the Stores_products_details table
SELECT Stores_products_details.storeProductDetailId, Stores.name AS storeName, Products.name AS productName, Stores_products_details.count, Stores_products_details.price
    FROM Stores_products_details
        INNER JOIN Stores ON Stores_products_details.storeId = Stores.storeId
        INNER JOIN Products ON Stores_products_details.productId = Products.productId;

--SELECTS a store_product_detail_instance from the Stores_products_details table using the FKs store and product ID
SELECT Stores_products_details.storeProductDetailId, Stores.name AS storeName, Products.name AS productName, Stores_products_details.count, Stores_products_details.price
    FROM Stores_products_details
        INNER JOIN Stores ON storeName = Stores.storeId
        INNER JOIN Products ON productName = Products.productId
    WHERE 
        Stores_products_details.storeId = :storeId
        Stores_products_details.productId = :productId;

--SELECTS all storeProductDetailIds, storeIds, and productIds from the Stores_products_details table dropdown
SELECT Stores_products_details.storeProductDetailId, Stores.name AS storeName, Products.name AS productName
    FROM Stores_products_details
        INNER JOIN Stores ON storeName = Stores.storeId
        INNER JOIN Products ON productName = Products.productId;

--UPDATEs a store_product_detail_instance from the Stores_products_details table using storeId and productId
UPDATE Stores_products_details
    SET 
        Stores_products_details.storeProductDetailId = :storeProductDetailIdInput,
        Stores_products_details.storeId =: storeIdInput,
        Stores_products_details.productId =: productIdInput,
        Stores_products_details.count = :countInput,
        Stores_products_details.price = :priceInput
    WHERE Stores_products_details.storeProductDetailId = :storeProductDetailIdFromUpdatePage;

--DELETEs a store_product_detail_instance from the Stores_products_details table using storeId and productId
DELETE 
    FROM Stores_products_details
    WHERE Stores_products_details.storeProductDetailId = :storeProductDetailIdFromDeletePage;
--------------------------------------------------------------------------
-- End of CRUD for Stores_products_details page 
--------------------------------------------------------------------------