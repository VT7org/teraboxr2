#!/bin/bash

# File to store PIDs
PID_FILE="bot_pids.txt"

# Function to clean up and stop the bots
cleanup() {
    echo "ᴋɪʟʟɪɴɢ ᴛʜᴇ ᴛᴇʀᴀʙᴏx ʙᴏᴛ..."
    if [ -f "$PID_FILE" ]; then
        while read -r pid; do
            if ps -p $pid > /dev/null; then
                kill $pid
                echo "ɢɪᴠᴇɴ ʀᴇsᴛ ᴛᴏ sᴘᴀᴄᴇ-x ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ᴡɪᴛʜ ᴘɪᴅ $pid"
            fi
        done < "$PID_FILE"
        rm "$PID_FILE"
    fi
    exit 0
}

# Trap Ctrl+C (SIGINT) to run cleanup
trap cleanup SIGINT

# Start main.py and autodel.py in the background
echo "ɪɴɪᴛɪᴀʟɪᴢɪɴɢ  sᴘᴀᴄᴇ-x ᴅᴏᴡɴʟᴏᴀᴅᴇʀ..."
python3 main.py > main.log 2>&1 &
MAIN_PID=$!
echo $MAIN_PID >> "$PID_FILE"
echo "sᴘᴀᴄᴇ-x ᴅᴏᴡɴʟᴏᴀᴅᴇʀ sᴛʀᴛᴇᴅ ᴡɪᴛʜ ᴘɪᴅ $MAIN_PID"

echo "Sᴛᴀʀᴛɪɴɢ ᴀᴜᴛᴏ ᴅᴇʟᴛɪᴏɴ ʜᴀɴᴅʟᴇʀ..."
python3 autodel.py > autodel.log 2>&1 &
AUTODEL_PID=$!
echo $AUTODEL_PID >> "$PID_FILE"
echo "ᴀᴜᴛᴏ ᴅᴇʟᴇᴛɪᴏɴ ʜᴀɴᴅʟᴇʀ sᴛᴀʀᴛᴇᴅ ᴡɪᴛʜ ᴘɪᴅ $AUTODEL_PID"

# Wait for both processes to finish
wait $MAIN_PID
wait $AUTODEL_PID
