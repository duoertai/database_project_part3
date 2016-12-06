PRAGMA foreign_keys = ON;
drop trigger if exists bid_amount_higher_than_previous;
create trigger bid_amount_higher_than_previous
after insert on Bid
for each row
when exists(select * from Bid as b1, Bid as b2 where b1.Time > b2.Time and b1.Amount <= b2.Amount and b1.ItemID = b2.ItemID)
begin
select raise(rollback, 'new bid must be higher than preivous');
end;
