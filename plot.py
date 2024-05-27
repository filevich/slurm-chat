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

import matplotlib.pyplot as plt

# Create a figure and axis
fig, ax = plt.subplots(1,2, figsize=(12, 5))

def plot(log, name):
    # messages
    x = [task["delta"] for task in log]
    t = [task["total"] for task in log] # messages
    n = [task["n"] for task in log] # simultaneous clients
    ax[0].plot(x, t, label=name)
    ax[1].plot(x, n, label=name)

plot(array50nodes1, "array=50, nodes=1")
plot(array25nodes2, "array=25, nodes=2")

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