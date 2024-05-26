### running with

`sbatch -J botbatch ~/Workspace/_tmp/chat/bots.sbatch 35`

array

```bash
#SBATCH --array=1-50
#SBATCH --ntasks=1
```

vs taks + srun

```bash
#SBATCH --ntasks=50
#SBATCH --nodes=5
```

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
