PRAGMA foreign_keys = ON;
drop trigger if exists check_number_of_bid;
create trigger check_number_of_bid
after insert on Bid
for each row
begin
update Items set Number_of_Bids = 1 + Number_of_Bids where Items.ItemID = new.ItemID;
end;
