#!/bin/bash

#SBATCH --job-name=defaultname
#SBATCH --array=1-2
#SBATCH --nodes=1 # nodes to use in total, per job or subjob
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=256M
#SBATCH --time=0-01:00:00
#SBATCH --partition=besteffort 
#SBATCH --qos=besteffort
#SBATCH --output=/clusteruy/home/juan.filevich/batches/out/chat/%x.%j.out
#SBATCH --error=/clusteruy/home/juan.filevich/batches/out/chat/%x.%j.out
#SBATCH --mail-type=NONE # options: NONE, BEGIN, END, FAIL, REQUEUE, ALL
#SBATCH --mail-user=juan.filevich@fing.edu.uy 

hr (){
printf '%*s\n' 80 | tr ' ' '-'
}

# dump args
printf "starts: $(date)\n"
echo "args: ${@}"
hr

PORT=$(python3 -c 'import socket; s=socket.socket(); s.bind(("", 0)); print(s.getsockname()[1]); s.close()')
echo "Starting srv on port $PORT at host $(hostname)"
scontrol update JobId="${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}" Comment="$PORT"

$HOME/miniconda3/envs/testing/bin/python3 -u \
  $HOME/Workspace/_tmp/slurm-chat/lesson-1/srv.py \
  --port $PORT

hr
printf "done: $(date)\n"
