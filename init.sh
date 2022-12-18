export PYTHONPATH=.

sleep 10

python3 ./initializer/populate_movies.py
python3 ./initializer/populate_users.py
python3 ./initializer/populate_cinemas.py
python3 ./initializer/populate_rooms.py
python3 ./initializer/populate_reviews.py
python3 ./initializer/populate_screenings.py
python3 ./initializer/populate_reservations.py