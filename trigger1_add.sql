PRAGMA foreign_keys = ON;
drop trigger if exists check_current_price;
create trigger check_current_price
after insert on Bid
for each row
begin
update Items set Currently = new.Amount where Items.ItemID = new.ItemID;
end;