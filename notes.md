## About cluster.uy architecture

On its website, cluster.uy shows this info:

```
node            CPU_type        cores ‡ mem_node gpu_node        disk `/scratch`
node[01-14][17] Xeon Gold 6138  40      128 GB   NVIDIA P100     300 GB SSD
node[15][16]    Xeon Gold 6138  40      128 GB   NVIDIA A100     300 GB SSD
node[26-28]     Xeon Gold 6138  40      128 GB   -               300 GB SSD
node[18-22]     Xeon Gold 6138  40      128 GB   NVIDIA P100 x 2 300 GB SSD
node23          Xeon Gold 6138  40      128 GB   NVIDIA P100 x 3 300 GB SSD
node[24-25]     Xeon Gold 6138  40      512 GB   -               300 GB SSD
node31          AMD EPYC  7642  96      256 GB   -               150 GB SSD
```

‡ That information is kind of misleading. E.g., Xeon Gold 6138 has 20 physical
cores, and 40 (physical) threads, but only if Hyper-Threading is enabled.
In theory, cluster.uy DOES NOT has HT enabled (to the date), so the actual 
number of cores per cpu should be half for each of them. Same for AMD Epyc 7642 
which in reality it only has 48 physical cores.

Notice: Max possible memory requested for a single job is 125 GiB, 503 GiB or 
251 GiB.

And thus,

```
number_nodes * cpus_per_node = total_cpus
((14-1+1)+1) *      (20)     = 300
(2)          *      (20)     = 40
(28-26+1)    *      (20)     = 60
(22-18+1)    *      (20)     = 100
(1)          *      (20)     = 20
(25-24+1)    *      (20)     = 40
(1)          *      (96)     = 48
-------------                  -------
29 nodes                       608 = (1216 / 2) cpus
```


### Usage

- You can list all nodes and its status with `sinfo -Nel`

- Or inspect a single node with `scontrol show node <node_name>`

On cluster.uy's official Telegram channel it shows this info:

```
alloc       6 nodes (240 CPUs)
drain       1 nodes (40 CPUs)
idle        6 nodes (296 CPUs)
mix        16 nodes (728 CPUs)
Total      29 nodes (1304 CPUs) 👈 which is bigger than 1216 🤷‍♂️
```

- As of today, (Mat 26th, 2024) the cluster usage is at 80% for cpus, and 79% 
  for gpus.

- These are the today's top 10 single user cpu-hours consumption in the last 24h:
  `34944, 11237, 10680, 10248, 9780, 9542, 7368, 5400, 5040, 2433`

- I.e., `1456, 468, 445, 427, 407, 397, 307, 225, 210, 101` cores used per hour.


### Comparison

- Noam Brown used 600 nodes, each equipped with 28 cores, over a period of 40 
  days to train Libratus. That is, `600 nodes * 28 cores * 40 days * 24 hours = 16M core-hours`.
  I.e., `16800` cores per hour.

- The system where Pluribus was trained used `(n nodes * c cores) * d days * 24 hours = 12.4k core-hours`.
  where `n*c = 64`, so we can derive that it was trained for about 8 days.
  I.e., `64` cores per hour.

- ReBeL used 7.5k core-hours, only one single machine for training and up to 
  128 machines with 8 GPUs each for data generation (i.e., self-play).




## VSCODE

```bash
PASSWORD=1234
PORT=$(python -c 'import socket; s=socket.socket(); s.bind(("", 0)); print(s.getsockname()[1]); s.close()')
echo "running on: $(hostname):${PORT}"
echo "tunel: 'ssh -L ${PORT}:$(hostname):${PORT} $(whoami)@cluster.uy'"
singularity exec --bind "$HOME/.local:/home/coder/.local" --bind "$HOME/.config:/home/coder/.config" --bind "$PWD:/home/coder/project" --env "DOCKER_USER=$USER" --env "PASSWORD=$PASSWORD" code-server_latest.sif /bin/bash -c "code-server --bind-addr 0.0.0.0:$PORT --auth password --disable-telemetry"
```

ssh tunnel

```
ssh -L 33584:node05.datos.cluster.uy:33584 juan.filevich@cluster.uy
```

then access `localhost:33584` in your browser