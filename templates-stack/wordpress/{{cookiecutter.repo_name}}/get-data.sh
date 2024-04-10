#!/bin/bash

source .env

# Check if $LOCAL_WP_ROOT_DIR exists, if not, create it
if [ ! -d "$LOCAL_WP_ROOT_DIR" ]; then
    mkdir -p "$LOCAL_WP_ROOT_DIR"
fi
# Same for data dir
if [ ! -d "data" ]; then
    mkdir -p "data"
fi


### Strategy A: mirror -- takes long; use backup archive if available
# lftp -u "$FTP_READ_USERNAME,$FTP_READ_PASSWORD" "$FTP_HOST" \
# mirror -c --only-newer --parallel=4 -e --verbose "$PROD_WP_ROOT_DIR" "$LOCAL_WP_ROOT_DIR"


### Strategy B: use backup archive
# Step 1: Get a listing of the remote directory
rm -f tmp.txt
lftp -u "$FTP_READ_USERNAME,$FTP_READ_PASSWORD" "$FTP_HOST" <<EOF
cd "$PROD_BACKUP_DIR"
lcd data/
nlist */*.gz > tmp.txt
bye
EOF

# Step 2: Find the latest dumps by sorting entries
# File names should start, e.g., with date in form of YYYYMMDD
sort -o data/tmp.txt -t '_' -k 1,1 -k 2,2 data/tmp.txt
files=$(grep "$PROD_WP_ROOT_DIR" data/tmp.txt | tail -1)
db=$(grep "$PROD_DB_NAME" data/tmp.txt | tail -1)

# Step 3: Download the latest files
rm -f "data/$(basename "$files")" "data/$(basename "$db")"
lftp -u "$FTP_READ_USERNAME,$FTP_READ_PASSWORD" "$FTP_HOST" <<EOF
cd "$PROD_BACKUP_DIR"
lcd data/
get "$files"
get "$db"
bye
EOF

# Unzip
rm -rf "wordpress/*"
gunzip -c "data/$(basename "$files")" | tar -x -C "wordpress/"
rm -f "data/$PROD_DB_NAME.sql"
gunzip -f "data/$(basename "$db")" -c > "data/$PROD_DB_NAME.sql"
