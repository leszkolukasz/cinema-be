from sqlalchemy import DDL

validate_seat_func = DDL(
    """
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
           RAISE EXCEPTION 'incorrect seat number';
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


validate_reservation_time_func = DDL(
    """
    CREATE OR REPLACE FUNCTION  validate_reservation_time_func()
        RETURNS TRIGGER
        LANGUAGE PLPGSQL
        AS
    $$
    DECLARE
        screening screenings%%ROWTYPE;
        movie movies%%ROWTYPE;
    BEGIN
        SELECT * INTO screening FROM screenings WHERE screening.id = NEW.screening_id;
        SELECT * INTO movie FROM movies WHERE movies.id = screening.movie_id;

        IF EXISTS (SELECT * FROM (SELECT * FROM screenings WHERE screenings.room_id = screening.room_id) screenings JOIN movies ON screenings.movie_id = movies.id WHERE LEAST(screenings.start_time + movies.length * interval '1 second', screening.start_time + movie.length * interval '1 second') >= GREATEST(screenings.start_time, screening.start_time)) THEN
            RAISE EXCEPTION 'reservations overlap';
        END IF;

       RETURN NEW;
    END;
    $$
    """
)

validate_reservation_time_trigger = DDL(
    "CREATE TRIGGER validate_reservation_time_trigger "
    "AFTER UPDATE OR INSERT "
    "ON reservations "
    "FOR EACH ROW "
    "EXECUTE PROCEDURE validate_reservation_time_func(); "
)
