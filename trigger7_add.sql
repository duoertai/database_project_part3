PRAGMA foreign_keys = ON;
drop trigger if exists new_current_time;
create trigger new_current_time
after insert on CurrentTime
for each row
when new.Time < (select max(Time) from CurrentTime)
begin
select raise(rollback, 'cannot insert past time');
end;
