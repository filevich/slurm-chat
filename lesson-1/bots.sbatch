#!/bin/bash

# when using standard args launch it as:
# `sbatch -J botbatch ~/Workspace/_tmp/slurm-chat/lesson-1/bots.sbatch <NUM_MSGS>`

# when using standard env vars launch it as:
# `NUM_MSGS=100 sbatch -J botbatch --export=ALL ~/Workspace/_tmp/slurm-chat/lesson-1/bots.sbatch`

# if you want to use an array-job instead remove the `--ntasks` param and add 
# something like
# --array=1-20 # array sub jobs
# --nodes=3
# instead

#SBATCH --job-name=defaultname
#SBATCH --nodes=5 # nodes to use in total, per job or subjob
#SBATCH --ntasks=50 # when doing `srun` launch `ntaks` parallel jobs across `nodes`
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=128M
#SBATCH --time=0-00:25:00
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

echo $FOO

NUM_MSGS=${1}
BOT_NAME="bot_${SLURM_ARRAY_JOB_ID}_${SLURM_JOB_ID}_${SLURM_ARRAY_TASK_ID}"

# get master ip:port from the "job" which:
#   1. is run by me
#   2. its name is srvchat
#   3. the master-job stored in the `Comment` field, the port it will be using...
output=$(squeue -u $(whoami) --name=srvchat --states=R -h -o "%k:%N")
PORT=$(echo $output | awk -F: '{print $1}')
HOST=$(echo $output | awk -F: '{print $2}')

# alternatively, you could just env vars or standard args, like this:
# HOST=${1:-"node03.datos.cluster.uy"}
# PORT=${2:-"52850"}

# srun will run this cmd `nodes` times in parallel
srun $HOME/miniconda3/envs/testing/bin/python \
  $HOME/Workspace/_tmp/slurm-chat/lesson-1/bot.py \
  --host ${HOST} \
  --port ${PORT} \
  -n ${NUM_MSGS} \
  ${BOT_NAME}

hr
printf "done: $(date)\n"
