import os
import sys
import json

def concat_traces(logs_path, new_filename):
    traces_list = []
    for filename in [fn for fn in os.listdir(logs_path)]:
        with open(f"{logs_path}/{filename}") as file:
            json_content = json.load(file)
            traces_list.extend(json_content)

    with open(new_filename, "w") as new_file:
        json.dump(traces_list, new_file, indent=4)

def stream_length_seconds_from_trace_file(trace_filename):
    with open(trace_filename) as json_file:
        traces_json = json.load(json_file)
    
    return int(sum([d["duration_ms"] for d in traces_json]) / 1000)

if __name__ == "__main__":
    """
    superdir = "/home/jonathan/prg/ex/sabre/example/"
    dir = "tomm19"
    for subdir in [d for d in os.listdir(superdir + dir) if os.path.isdir(f"{superdir}{dir}/{d}")]:
        new_filename = f"{dir}_{subdir}_traces.json"
        logs_path = f"{superdir}{dir}/{subdir}"

        concat_traces(logs_path, new_filename)
    """

    """
    json_output = {}

    example_dir = "./example"
    for dir in ["mmsys18", "tomm19"]:
        for subdir in os.listdir(example_dir + "/" + dir):
            if "." in subdir: pass
            else:
                new_dir = "./bitrates/" + dir + "/" + subdir
                if not os.path.exists:
                    os.mkdir(new_dir)

                l = [f for f in os.listdir(f"{example_dir}/{dir}/{subdir}") if ".json" in f]
                for trace_filename in l:
                    length = stream_length_seconds_from_trace_file(f"{example_dir}/{dir}/{subdir}/{trace_filename}")
                    json_output[f"{example_dir}/{dir}/{subdir}/{trace_filename}"] = length
                    print(length)

    with open("trace_length_seconds.json", "w") as new_file:
        json.dump(json_output, new_file, indent=4)
    """

    with open("traces/trace_length_seconds.json", "r") as file:
        content = json.load(file)
        sum3G = 0
        sum4G = 0
        for key in dict(content).keys():
            if "3G" in key or "sd" in key: sum3G += content[key]
            else: sum4G += content[key]

        print(sum3G/3600)
        print(sum4G/3600)


