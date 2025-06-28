#!/bin/bash

shift
cmd="$@"

# try connect to mysql
for i in {1..30}; do
    if python scripts/check_mysql.py; then
      echo "MySQL is ready!"
      exec $cmd
      exit 0
    fi
    
    echo "MySQL not ready yet - attempt $i/30"
    sleep 2
done

echo "Failed to connect to MySQL after 30 attempts"
exit 1