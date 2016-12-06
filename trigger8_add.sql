PRAGMA foreign_keys = ON;
drop trigger if exists bid_at_current_time;
create trigger bid_at_current_time
after insert on Bid
for each row
when new.Time <> (select max(Time) from CurrentTime)
begin
select raise(rollback, 'new bid must be placed at current time');
end;