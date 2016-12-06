PRAGMA foreign_keys = ON;
drop trigger if exists bid_during_valid_time;
create trigger bid_during_valid_time
after insert on Bid
for each row
when new.Time < (select Started from Items where Items.ItemID = new.ItemID) or new.Time > (select Ends from Items where Items.ItemID = new.ItemID)
begin
select raise(rollback, 'bid time invalid');
end;