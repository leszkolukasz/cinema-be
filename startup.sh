if [ -f /docker-tmp/set-up ]; then
    bash /app/init.sh
    rm /docker-tmp/set-up
fi

uvicorn main:app --host=0.0.0.0 --reload