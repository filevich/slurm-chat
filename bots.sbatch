#!/bin/bash

# run as `sbatch -J botbatch ~/Workspace/_tmp/slurm-chat/bots.sbatch NUM_MSGS`

#SBATCH --job-name=defaultname
#SBATCH --array=1-20
#SBATCH --nodes=3
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=128M
#SBATCH --time=0-00:4:00
#SBATCH --partition=normal 
#SBATCH --qos=normal
#SBATCH --output=/clusteruy/home/juan.filevich/batches/out/chat/%x.%j.out
#SBATCH --error=/clusteruy/home/juan.filevich/batches/out/chat/%x.%j.out
#SBATCH --mail-type=NONE # options: NONE, BEGIN, END, FAIL, REQUEUE, ALL
#SBATCH --mail-user=juan.filevich@fing.edu.uy 

# every (sub)job will execute this from here
# all (sub)job will share the same args ${@}

hr (){
printf '%*s\n' 80 | tr ' ' '-'
}

# dump args
printf "starts: $(date)\n"
echo "args: ${@}"
hr

bot_name="bot_${SLURM_ARRAY_JOB_ID}_${SLURM_JOB_ID}_${SLURM_ARRAY_TASK_ID}"

# get master ip:port from the "job" which:
#   1. is run by me
#   2. its name is srvchat
#   3. the master-job stored in the `Comment` field, the port it will be using...
output=$(squeue -u $(whoami) --name=srvchat --states=R -h -o "%k:%N")
P=$(echo $output | awk -F: '{print $1}')
N=$(echo $output | awk -F: '{print $2}')

# alternatively, you could just do something like:
# N=${1:-"node03.datos.cluster.uy"}
# P=${2:-"52850"}

# srun will run this cmd `nodes` times in parallel
srun $HOME/miniconda3/envs/testing/bin/python \
  $HOME/Workspace/_tmp/chat/bot.py \
  --host ${N} \
  --port ${P} \
  -n ${1} \
  ${bot_name}

hr
printf "done: $(date)\n"
