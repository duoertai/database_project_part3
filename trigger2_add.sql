PRAGMA foreign_keys = ON;
drop trigger if exists check_bidder_seller;
create trigger check_bidder_seller
after insert on Bid
for each row
when new.BidderID in (select distinct(SellerID) from Item_Seller where new.ItemID = Item_Seller.ItemID)
begin
select raise(rollback, 'seller cannot bid on his own item');
end;
