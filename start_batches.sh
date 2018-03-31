#!/usr/bin/env bash
#
# Setup a tmux session called 'droc-batches'.
# The session has multiple windows; the number is set as a parameter to the script.
# Each window starts a batch of run.py.

if [ $# -eq 0 ]; then
    echo 'Error: number of batches is required.'
    echo 'Usage: ./start_in_tmux num_batches'
    echo '    where num_batches is the number of batches to divide the work into.'
    exit 1
fi

session="droc-batches"
num_batches=$1
echo "starting $num_batches batches..."

# Start up tmux
# tmux start-server

# Create the session
# Name the first window '0'
echo 'starting batch 0...'
tmux new-session -d -s $session -n 'batch 0'
tmux send-keys "python run.py -v --prep --of $num_batches --batch 0" C-m

# # Add a window
# tmux send-keys "echo 'yo yo yo'" C-m

if [ $num_batches != "1" ]; then
    for (( i=1; i<$num_batches; i++))
    do
        echo "starting batch $i..."
        tmux new-window -t $session -n "batch $i"
        tmux send-keys "python run.py -v --prep --of $num_batches --batch $i" C-m
    done
fi

tmux select-window -t $session:0

echo 'done. to attach to session, run'
echo
echo "tmux attach -t $session"
echo
