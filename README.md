## How to run locally

- start server `python3 ~/Workspace/py/chat/srv.py --port 8989`
- start alice `python3 ~/Workspace/py/chat/cli.py --port 8989 alice`
- start bob `python3 ~/Workspace/py/chat/cli.py --port 8989 bob`

## How to run in SLURM cluster

Reserve a node to host the srv

`srun --job-name=srvchat --time=05:00:00 --partition=besteffort --qos=besteffort --ntasks=1 --cpus-per-task=1 --mem=512M --pty bash -l`

Then, once inside of it run

```bash
PORT=$(python3 -c 'import socket; s=socket.socket(); s.bind(("", 0)); print(s.getsockname()[1]); s.close()')
echo "Starting srv on port $PORT"
scontrol update JobId="$SLURM_JOB_ID" Comment="$PORT"
$HOME/miniconda3/envs/testing/bin/python3 $HOME/Workspace/_tmp/slurm-chat/srv.py --port $PORT
```

Now, run the parallel bots with

`sbatch -J botbatch ~/Workspace/_tmp/slurm-chat/bots.sbatch 10`




## Array vs ntasks

- If you use array: the (sub)jobs may start at different times
- If you use tasks: they're gonna start all at the same time

At the end, it all comes down to this: if your job is embarrassingly parallel,
you can use array (or even ntasks), else, you should use ntasks. 

### array

* You cannot set `--array` greater than 50
* In `normal` QoS only 30 (sub)jobs will run in parallel. If you set `--array` 
  to 50, then it will run 30 processes, and then 20.
* If you run with `--array=1-50` and set sbatch bots to produce 10 msgs you will get:
    - First 30 parallel processes, and then 20 parallel procesess
    - 50 log files in total (one for each bot)
    - 10 msgs * 50 = 500 msgs
    - slurm will distribute all array-jobs ("subjobs") into different nodes
* If you set `--array=1-2` and `--nodes=2` you will get:
    - 4 processes running
    - 2 subjobs (e.g., `3607061_1` + `3607061_2`) but running in two different
      node lists (e.g., `node[15-16]` + `node[18-19]`)
* If you set `--array=1-50` and `--nodes=2` you will get:
    - 60 processes running in parallel (n=60 in srv)
    - First 30+30=60, and then 20+20=40 parallel processes
    - (50 subjobs) * (2 nodes each) * (10 msgs each) = 1000 msgs
* If you set `--array=1-50` and `--nodes=2` but **without** `srun`, you will get:
    - First 30 then 20 parallel processes.
    - I.e., for each subjob, one node is wasted doing nothing.
    - (30+20 subjobs) * (10 msgs each) = 500 msgs
* If you set `--mail-type=END` you will get only one email. E.g.,
  `Slurm Array Summary Job_id=3607247_* (3607247) Name=botbatch Ended, COMPLETED`

In summary:
  - Always use `srun`
  - For each array-job/sub-job * for each node: run the command of `srun`
  - `srun` will distribute one instance of the cmd for each node assigned to the
    (sub)job.

Example:

```bash
#SBATCH --nodes=2
#SBATCH --array=1-50
```

vs taks + **srun**

```bash
#SBATCH --ntasks=50
#SBATCH --nodes=5
srun CMD
```

## array

in my cluster, for anything bigger than 50 in `#SBATCH --array=1-50` it will
return `sbatch: error: QOSMaxSubmitJobPerUserLimit`

### array vs ntasks

https://stackoverflow.com/questions/53423544/slurm-question-array-job-vs-srun-in-a-sbatch

this is how array jobs are shown:

```bash
    JOBID     NAME          START_TIME    STATE NODES NODELIST(REASON)
3604086_0 botbatch 2024-05-26T01:07:47  RUNNING     1 node05
3604086_4 botbatch 2024-05-26T01:07:47  RUNNING     1 node05
3604086_5 botbatch 2024-05-26T01:07:47  RUNNING     1 node05
3604086_6 botbatch 2024-05-26T01:07:47  RUNNING     1 node05
3604086_7 botbatch 2024-05-26T01:07:47  RUNNING     1 node16
3604086_8 botbatch 2024-05-26T01:07:47  RUNNING     1 node16
3604086_9 botbatch 2024-05-26T01:07:47  RUNNING     1 node16
3604086_1 botbatch 2024-05-26T01:07:47  RUNNING     1 node16
3604086_1 botbatch 2024-05-26T01:07:47  RUNNING     1 node16
3604086_1 botbatch 2024-05-26T01:07:47  RUNNING     1 node16
3604086_1 botbatch 2024-05-26T01:07:47  RUNNING     1 node15
3604086_1 botbatch 2024-05-26T01:07:47  RUNNING     1 node15
3604086_1 botbatch 2024-05-26T01:07:47  RUNNING     1 node15
```

Notice that:

```bash
[juan.filevich@login chat]$ scontrol show config | grep -E 'MaxArraySize|MaxJobCount'
MaxArraySize            = 1001
MaxJobCount             = 1000000
```

Yet, for `#SBATCH --array=1-50` we get 

```bash
[juan.filevich@login chat]$ squeue --format="%.9i %.9P %.40j %.8u %.22S %.8T %.10M %.9l %.6D %R" -u juan.filevich
    JOBID PARTITION     NAME          START_TIME    STATE NODES NODELIST(REASON)
3604366_[    normal botbatch                 N/A  PENDING     1 (QOSMaxJobsPerUserLimit)
3604366_0    normal botbatch 2024-05-26T02:33:11  RUNNING     1 node08
3604366_1    normal botbatch 2024-05-26T02:33:11  RUNNING     1 node16
3604366_2    normal botbatch 2024-05-26T02:33:11  RUNNING     1 node19
3604366_2    normal botbatch 2024-05-26T02:33:11  RUNNING     1 node19
  3603995 besteffor  srvchat 2024-05-26T00:41:58  RUNNING     1 node02
```

While on the server we got `We are officially CLOSE at 0:07:00.853182!`

If we see the `[n=?]` output from the server, we see that `n` never goes beyond
30.

## Tasks

**If you use tasks don't forget of placing before your commands `srun` !!!!**

NOW if we use 50 tasks like this:

```bash
#SBATCH --ntasks=50
#SBATCH --cpus-per-task=1
```

we will get:

```bash
[juan.filevich@login chat]$ squeue --format="%.9i %.9P %.40j %.8u %.22S %.8T %.10M %.9l %.6D %R" -u juan.filevich
   JOBID PARTITION     NAME          START_TIME    STATE NODES NODELIST(REASON)
 3604309    normal botbatch                 N/A  PENDING     1 (QOSMaxCpuPerNode)
 3603995 besteffor  srvchat 2024-05-26T00:41:58  RUNNING     1 node02
```

But if we add `#SBATCH --nodes=5` like this:

```bash
#SBATCH --ntasks=50
#SBATCH --nodes=5
#SBATCH --cpus-per-task=1
```

Now, on the server we got:

`[IN][n=50] bot_5ps=_3604987: 3/35`

And

`We are officially CLOSE at 0:03:52.207930!`
`We are officially CLOSE after 0:03:16.000293 with 70 msgs!`

Those 50 task will be distributed across 5 nodes:

```bash
[juan.filevich@login chat]$ squeue --format="%.9i %.9P %.40j %.8u %.22S %.8T %.10M %.9l %.6D %R" -u juan.filevich
    JOBID PARTITION     NAME          START_TIME    STATE NODES NODELIST(REASON)
  3604345    normal botbatch 2024-05-26T02:20:16  RUNNING     5 node[18-22]
  3603995 besteffor  srvchat 2024-05-26T00:41:58  RUNNING     1 node02
```

ntasks will be shown like this instead:

```bash
    JOBID PARTITION     NAME          START_TIME    STATE NODES NODELIST(REASON)
  3604277    normal botbatch 2024-05-26T01:55:36  RUNNING     1 node27
  3603995 besteffor  srvchat 2024-05-26T00:41:58  RUNNING     1 node02
```

if we check for logs we get only one:

```bash
(testing) [juan.filevich@login chat]$ ls
botbatch.3604289.out
```

which merges everyhing:
NOTICE: it won't show the prints/logs in the log file until all taks are done.

```
args: 5
--------------------------------------------------------------------------------
Connected to the server!
bot_LJo=_3604291: 1/5
bot_LJo=_3604291: 2/5
bot_LJo=_3604291: 3/5
bot_LJo=_3604291: 4/5

Disconnected from the server
Connected to the server!
bot_LJo=_3604291: 1/5
bot_LJo=_3604291: 2/5
bot_LJo=_3604291: 3/5
bot_LJo=_3604291: 4/5
bot_LJo=_3604291: 5/5

Disconnected from the server
--------------------------------------------------------------------------------
done Sun May 26 02:04:06 -03 2024
```
