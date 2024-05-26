#!/bin/bash

#SBATCH --job-name=defaultname
#SBATCH --ntasks=50
#SBATCH --nodes=5
#SBATCH --cpus-per-task=1
#SBATCH --mem=128M
#SBATCH --time=0-00:10:00 
#SBATCH --partition=normal 
#SBATCH --qos=normal 
#SBATCH --output=/clusteruy/home/juan.filevich/batches/out/chat/%x.%j.out
#SBATCH --error=/clusteruy/home/juan.filevich/batches/out/chat/%x.%j.out
#SBATCH --mail-type=NONE
#SBATCH --mail-user=juan.filevich@fing.edu.uy 

# run as `sbatch -J job_name ~/batches/scripts/chat/bots.sbatch arg1 arg2 arg3`
# change `mail-type` for [NONE, BEGIN, END, FAIL, REQUEUE, ALL]

hr (){
printf '%*s\n' 80 | tr ' ' '-'
}

# dump args
echo "args: ${@}"
printf "start $(date)\n"
hr

random_string=$(openssl rand -base64 2)
# bot_name="bot_${random_string}_${SLURM_ARRAY_TASK_ID}"
bot_name="bot_${random_string}_${SLURM_JOB_ID}"

# run
N=node02.datos.cluster.uy
P=57471
random_string=$(openssl rand -base64 12)
srun $HOME/miniconda3/envs/testing/bin/python $HOME/Workspace/_tmp/chat/bot.py --host ${N} --port ${P} -n ${1} ${bot_name}

hr
printf "done $(date)\n"
