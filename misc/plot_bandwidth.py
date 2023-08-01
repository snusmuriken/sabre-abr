from matplotlib import pyplot as plt
import numpy as np
import os
import json

def plot_trace_file(trace_file):
    with open(trace_file) as json_file:
        json_content = json.load(json_file)
        a = np.array([d["bandwidth_kbps"] for d in json_content])
        
        plt.plot(a)
        plt.title(trace_file)
        plt.show()

if __name__ == "__main__":
    for trace_file in [f"./traces/{f}" for f in os.listdir("./traces")]:
        if "json" in trace_file and "trace_length" not in trace_file:
            plot_trace_file(trace_file)
