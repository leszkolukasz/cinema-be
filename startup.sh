if [ ! -f /app/done.txt ]; then
    bash /app/init.sh
    touch /app/done.txt
fi

uvicorn main:app --host=0.0.0.0 --reload