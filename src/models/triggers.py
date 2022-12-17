from sqlalchemy import DDL

validate_seat_func = DDL("""
    CREATE OR REPLACE FUNCTION  validate_seat_func()
        RETURNS TRIGGER
        LANGUAGE PLPGSQL
        AS
    $$
    DECLARE
    max_seat INT;
    BEGIN
       max_seat := (SELECT rooms.length * rooms.width - 1 FROM (SELECT * FROM screenings WHERE id = NEW.screening_id) as screenings, rooms WHERE screenings.room_id = rooms.id);
       IF NEW.seat > max_seat THEN
           RAISE EXCEPTION \'incorrect seat number\';
       END IF;

       RETURN NEW;
    END;
    $$
    """
)

validate_seat_trigger = DDL(
    "CREATE TRIGGER validate_seat_trigger "
    "AFTER UPDATE OR INSERT "
    "ON reservations "
    "FOR EACH ROW "
    "EXECUTE PROCEDURE validate_seat_func(); "
)