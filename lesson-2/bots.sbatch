#!/bin/bash

# when using standard args launch it as:
# `sbatch -J botbatch ~/Workspace/_tmp/slurm-chat/lesson-1/bots.sbatch <num_msgs>`

# when using standard env vars launch it as:
# `num_msgs=100 sbatch -J botbatch --export=ALL ~/Workspace/_tmp/slurm-chat/lesson-1/bots.sbatch`

# if you want to use an array-job instead remove the `--ntasks` param and add 
# something like
# --array=1-20 # array sub jobs
# --nodes=3
# instead

#SBATCH --job-name=defaultname
#SBATCH --nodes=5 # nodes to use in total, per job or subjob
#SBATCH --ntasks=10 # when doing `srun` launch `ntaks` parallel jobs across `nodes`
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=128M
#SBATCH --time=0-00:10:00
#SBATCH --partition=besteffort 
#SBATCH --qos=besteffort
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

# get master ip:port from the "job" which:
#   1. is run by me
#   2. its name is srvs
#   3. the master-job stored in the `Comment` field, the port it will be using...
srvs=$(squeue -u $(whoami) --name=srvs --states=R -h -o "%N:%k" | paste -sd ",")
num_msgs=${1}
bot_name="bot_${SLURM_ARRAY_JOB_ID}_${SLURM_JOB_ID}_${SLURM_ARRAY_TASK_ID}"
task_log=$HOME/batches/out/chat/%x.%j_%t.out

echo "using: srv:${srvs} nummsgs:${num_msgs} botname:${bot_name} logs:${task_log}"

# alternatively, you could just env vars or standard args, like this:
# HOST=${1:-"node03.datos.cluster.uy"}
# PORT=${2:-"52850"}

# srun will run this cmd `nodes` times in parallel
srun -l --output=$task_log --error=$task_log \
  $HOME/miniconda3/envs/testing/bin/python -u \
  $HOME/Workspace/_tmp/slurm-chat/lesson-2/multi_bot.py \
  --servers ${srvs} \
  --num_msgs ${num_msgs} \
  ${bot_name}

hr
printf "done: $(date)\n"
