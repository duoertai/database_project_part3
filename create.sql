
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Items;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Item_Category;
DROP TABLE IF EXISTS Item_Seller;
DROP TABLE IF EXISTS Bid;
DROP TABLE IF EXISTS CurrentTime;

CREATE TABLE Users
(

UserID varchar(1000) NOT NULL,
Rating int NOT NULL,
Location varchar(1000),
Country varchar(200),
PRIMARY KEY (UserID)

);

CREATE TABLE Categories
(

Category varchar(1000) NOT NULL,
PRIMARY KEY (Category)

);

CREATE TABLE Items
(

ItemID int NOT NULL,
Name varchar(1000) NOT NULL,
Started timestamp NOT NULL,
Ends timestamp NOT NULL,
Currently float NOT NULL,
First_Bid float NOT NULL,
Buy_Price float,
Number_of_Bids int NOT NULL,
Description text,
PRIMARY KEY (ItemID),
CHECK (Ends > Started)

);


CREATE TABLE  Item_Category
(

ItemID int NOT NULL,
Category varchar(1000) NOT NULL,
PRIMARY KEY (ItemID, Category),
FOREIGN KEY (ItemID) REFERENCES Items(ItemID),
FOREIGN KEY (Category) REFERENCES Categories(Category)

);

CREATE TABLE Item_Seller
(

ItemID int NOT NULL,
SellerID varchar(1000) NOT NULL,
PRIMARY KEY(ItemID),
FOREIGN KEY (ItemID) REFERENCES Items(ItemID),
FOREIGN KEY (SellerID) REFERENCES Users(UserID)

);

CREATE TABLE Bid
(

BidderID varchar(1000) NOT NULL,
ItemID int NOT NULL,
Time timestamp NOT NULL,
Amount float NOT NULL,
PRIMARY KEY (ItemID, Time),
UNIQUE (BidderID, Amount),
FOREIGN KEY (BidderID) REFERENCES Users(UserID),
FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
);

CREATE TABLE CurrentTime(

Time timestamp NOT NULL,
PRIMARY KEY (Time)

);

INSERT INTO CurrentTime VALUES (datetime('2001-12-20 00:00:01'));

