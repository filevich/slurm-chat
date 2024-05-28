import json

def parse_log(logfile:str) -> list[object]:
    res = []
    with open(logfile, "r") as f:
        for line in f.readlines():
            try:
                data = json.loads(line)
                if data.get("type", "?") == "IN":
                    res += [data]
            except:
                pass
    return res


array50nodes1 = parse_log("logs/array50-nodes1-100m.log")
array25nodes2 = parse_log("logs/array25-nodes2-100m.log")
nodes5tasks50 = parse_log("logs/nodes5-tasks50-100m.log")
array0nodes5tasks50 = parse_log("logs/array0-nodes5-tasks50-100m.log")

import matplotlib.pyplot as plt

# Create a figure and axis
fig, ax = plt.subplots(1,2, figsize=(12, 5))

def plot(log, args={}):
    x = [task["delta"] for task in log]
    t = [task["total"] for task in log] # messages
    n = [task["n"] for task in log] # simultaneous clients
    ax[0].plot(x, t, **args)
    ax[1].plot(x, n, **args)

plot(array50nodes1, {"label": "array=50, nodes=1", "linewidth":1, "color": "green"})
plot(array25nodes2, {"label": "array=25, nodes=2", "linewidth":1, "color": "blue"})
plot(nodes5tasks50, {"label": "tasks=50, nodes=5", "linewidth":1, "color": "orange"})
plot(array0nodes5tasks50, {"label": "array=0, tasks=50, nodes=5", "linewidth":1, "color": "red"})

# Set labels and title

# messages
ax[0].set_xlabel('delta (secs)')
ax[0].set_ylabel('total messages')
ax[0].set_title('Total messages received over time')
ax[0].legend()

# 
ax[1].set_xlabel('delta (secs)')
ax[1].set_ylabel('simultaneous clients')
ax[1].set_title('Total simultaneous clients over time')
ax[1].legend()

# Show the plot
plt.tight_layout()
plt.show()