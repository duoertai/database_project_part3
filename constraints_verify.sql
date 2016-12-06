/*
constraint 2
*/

SELECT Item_Seller.SellerID
FROM Item_Seller
WHERE Item_Seller.SellerID not in (SELECT UserID FROM Users);

SELECT Bid.BidderID
FROM Bid, Users
WHERE BidderID not in (SELECT UserID FROM Users);

/*
constraint 4
*/


SELECT b.ItemID
FROM (SELECT distinct(ItemID) from Bid) as b
WHERE b.ItemID NOT IN (SELECT distinct(ItemID) FROM Items);


/*
constraint 5
*/


SELECT distinct(Item_Category.ItemID)
FROM Item_Category, Items
WHERE Item_Category.ItemID not in (SELECT ItemID FROM Items);


