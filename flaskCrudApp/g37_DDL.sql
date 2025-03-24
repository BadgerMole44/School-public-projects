-- cs340 Group 37 Project

-- Prep for Commit
SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT=0;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Stores;
DROP TABLE IF EXISTS Rewards_customers;
DROP TABLE IF EXISTS Sales_transactions;
DROP TABLE IF EXISTS Stores_products_details;
DROP TABLE IF EXISTS Sales_transactions_details;

-- -----------------------------------------------------
-- Products table Creation and Insertion
-- -----------------------------------------------------
CREATE OR REPLACE TABLE Products (
  productId INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(145) NOT NULL,
  model VARCHAR(145) NOT NULL,
  description VARCHAR(250) NULL,
  PRIMARY KEY (productId),
  UNIQUE INDEX name_model_UNIQUE (name ASC, model ASC)
);
INSERT INTO Products (name, model, description)
VALUES
('Hammer', 'Ab12', '16oz hammer'),
('Nails', 'z2Tf5', '100 pack'),
('Pressure treated wood', '4ty7U', '2 by 4'),
('Cordless drill', 'wN53I2', NULL),
('Deck Screws', 'qqW345', '50 pack');

-- -----------------------------------------------------
-- Stores table Creation and Insertion
-- -----------------------------------------------------
CREATE OR REPLACE TABLE  Stores (
  storeId INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(145) NOT NULL,
  city VARCHAR(145) NOT NULL,
  state VARCHAR(145) NOT NULL,
  streetAddress VARCHAR(250) NOT NULL,
  PRIMARY KEY (storeId),
  UNIQUE INDEX city_state_streetAddress_UNIQUE (city ASC, state ASC, streetAddress ASC)
);
INSERT INTO Stores(name, city, state, streetAddress)
VALUES
('Big Hardware Depot', 'Corvallis', 'OR', '123 main st.'),
('Big Hardware Best', 'Pittsburgh', 'PA', '34 hill rd.'),
('Big Hardware Super', 'New York', 'NY', '987 245th st.');

-- -----------------------------------------------------
-- Products table Creation and Insertion
-- -----------------------------------------------------
CREATE OR REPLACE TABLE Rewards_customers (
  rewardCustomerId INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(145) NOT NULL,
  phone VARCHAR(20) NOT NULL,
  email VARCHAR(45) NULL,
  address VARCHAR(250) NULL,
  points INT UNSIGNED NOT NULL,
  PRIMARY KEY (rewardCustomerId),
  UNIQUE INDEX phone_UNIQUE (phone ASC),
  UNIQUE INDEX email_UNIQUE (email ASC)
);
INSERT INTO Rewards_customers (name, phone, email, address, points)
VALUES
('Phil', '(723)804-3345', 'phillyphil@mail.com', NULL, 10000),
('Jayleen', '(727)574-7732', NULL, NULL, 200),
('Morris', '(123)678-2345', NULL, NULL, 225);

-- -----------------------------------------------------
-- Sales_transactions table Creation and Insertion
-- -----------------------------------------------------
CREATE OR REPLACE TABLE Sales_transactions (
  saleTransactionId INT NOT NULL AUTO_INCREMENT,
  storeId INT DEFAULT NULL,
  date DATE NOT NULL,
  rewardCustomerId INT NULL,
  total DECIMAL(10,2) NOT NULL,
  pointsApplied INT UNSIGNED NOT NULL DEFAULT 0,
  finalAmount DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (saleTransactionId),
  INDEX fk_sales_rewards_customers1_idx (rewardCustomerId ASC) VISIBLE,
  INDEX fk_Sales_transactions_Stores1_idx (storeId ASC) VISIBLE,
  CONSTRAINT fk_sales_rewards_customers1
    FOREIGN KEY (rewardCustomerId)
    REFERENCES Rewards_customers (rewardCustomerId)
    ON DELETE SET NULL
    ON UPDATE NO ACTION,
  CONSTRAINT fk_Sales_transactions_Stores1
    FOREIGN KEY (storeId)
    REFERENCES Stores (storeId)
    ON DELETE SET NULL
    ON UPDATE NO ACTION
);
INSERT INTO Sales_transactions(storeId, date, rewardCustomerId, total, pointsApplied, finalAmount)
VALUES
(1, '2024-10-20', NULL, 188.94, 0,  188.94),
(1, '2024-10-20',    1, 124.98, 0,  124.98),
(2, '2024-10-21', NULL, 136.89, 0,  136.89),
(3, '2024-10-21',    2, 32.99, 200, 30.99);

-- -----------------------------------------------------
-- Stores_products_details table Creation and Insertion
-- -----------------------------------------------------
CREATE OR REPLACE TABLE Stores_products_details (
  storeProductDetailId INT NOT NULL AUTO_INCREMENT,
  storeId INT NOT NULL,
  productId INT NOT NULL,
  count INT UNSIGNED NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (storeProductDetailId),
  INDEX fk_Stores_products_details_Products1_idx (productId ASC) VISIBLE,
  INDEX fk_Stores_products_details_Stores1_idx (storeId ASC) VISIBLE,
  CONSTRAINT fk_Stores_products_details_Products1
    FOREIGN KEY (productId)
    REFERENCES Products (productId)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT fk_Stores_products_details_Stores1
    FOREIGN KEY (storeId)
    REFERENCES Stores (storeId)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  UNIQUE (storeId, productId)     -- Ensure no duplicates. 
);
INSERT INTO Stores_products_details (storeId, productId, count, price)
VALUES
(1, 1, 45, 24.99),
(1, 2, 70, 29.99),
(1, 4, 20, 99.99),
(2, 1, 55, 21.99),
(2, 3, 100, 9.99),
(3, 1, 20, 32.99),
(1, 5, 60, 36.99),
(3, 5, 30, 44.99);

-- -----------------------------------------------------
-- Sales_transactions_details table Creation and Insertion
-- -----------------------------------------------------
CREATE OR REPLACE TABLE Sales_transactions_details (
  saleTransactionDetailId INT NOT NULL AUTO_INCREMENT,
  saleTransactionId INT NOT NULL,
  productId INT DEFAULT NULL,
  quantity INT NOT NULL,
  total DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (saleTransactionDetailId),
  INDEX fk_Sales_items_Sales_transactions1_idx (saleTransactionId ASC) VISIBLE,
  INDEX fk_Sales_items_Products1_idx (productId ASC) VISIBLE,
  CONSTRAINT fk_Sales_items_Sales_transactions1
    FOREIGN KEY (saleTransactionId)
    REFERENCES Sales_transactions (saleTransactionId)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_Sales_items_Products1
    FOREIGN KEY (productId)
    REFERENCES Products (productId)
    ON DELETE SET NULL
    ON UPDATE NO ACTION
);
INSERT INTO Sales_transactions_details (saleTransactionId, productId, quantity, total)
VALUES
(1, 1, 1,  24.99),
(1, 2, 3,  89.97),
(1, 5, 2,  73.98),
(2, 4, 1,  99.99),
(3, 5, 1,  36.99),
(4, 1, 1,  32.99),
(2, 1, 1,  24.99),
(3, 3, 10, 99.90);

SET FOREIGN_KEY_CHECKS=1;
COMMIT;