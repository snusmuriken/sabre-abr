import json
import subprocess
import os
import sys
import time

SABRE_DIR = "/home/jonathan/prg/ex/sabre"
TRACES_DIR = SABRE_DIR + "/traces"
LENGTH_JSON_FILE = TRACES_DIR + "/trace_length_seconds.json"
MANIFEST_FILE = SABRE_DIR + "/manifests/green_abr_manifest.json"
ABR = "throughput"
TEMP_TRACES_DIR = "./temp_traces"

def split_traces_file(video_len_s, split_traces_list, traces):
    """
    Splits a file's traces and adds them in place to a total split list.
    """
    timer = 0
    cur_split = []

    # Note: if the last split is not of sufficient length it will not be added.
    for trace in traces:
        if timer <= video_len_s + 5:
            cur_split.append(trace)
            timer += trace["duration_ms"] / 1000
        else:
            split_traces_list.append(cur_split)
            timer = 0
            cur_split = []

def split_trace_files(video_len_s, output_dir):
    """
    Splits the trace files into larger 
    """
    # Go through the concatenated trace files and split them up
    for trace_file in os.listdir(TRACES_DIR):
        split_traces_list = []
        
        with open(f"{TRACES_DIR}/{trace_file}", "r") as file:
            traces = json.load(file)

        # In some trace files there are large periods of no bandwidth. 
        # This make sabre hang. Remove to avoid this.
        traces = [d for d in traces if d["bandwidth_kbps"] > 0]
        
        # Append the traces to the current split until the total 
        # length of the split is longer than the video length. 
        # Then append the split and reset the timer
        split_traces_file(video_len_s, split_traces_list, traces)
        
        # Create a temporary trace file for each list
        print(trace_file)   # TODO: Något går fel med längden på dessa

        for i, traces_list in enumerate(split_traces_list):
            i += 1
            #print(f"----------\n{len(traces_list)}")
            #print(f"{sum([trace['duration_ms'] for trace in traces_list])}\n----------")
            #l.append(sum([trace['duration_ms'] for trace in traces_list]))

            with open(f"{TEMP_TRACES_DIR}/{trace_file[:-5]}_{str(i).zfill(3)}.json", "w") as new_file:
                json.dump(traces_list, new_file, indent = 4)


def run_python_script(script_file, args):
    cmd = ["python", script_file] + args
    subprocess.call(cmd)

def run_sabre(script_file, video_length_s, fixed_len=False, traces_dir = TRACES_DIR, manifest_file = MANIFEST_FILE, output_dir = None):
    """
    Runs Sabre with the given video length, traces, manifest file and output directory.
    
    Params:
        - script_file (str): Path to the sabre.py file
        - video_len_s (dict OR int): Either:
            (a) A directory with keys = trace files and values = video length OR
            (b) A fixed value in seconds
        - fixed_len (bool): True if video_len_s is int, False if dict
        - traces_dir (str): Path to the directory that contains the traces (and only the traces) (default = TRACES_DIR)
        - manifest_file (str): Path to the manifest file (default = MANIFEST_FILE)
        - output_dir (str): Optional path for log output
    """
    for trace_file in sorted(os.listdir(traces_dir)):
        if fixed_len:
            length_seconds = str(video_length_s)
        else:
            length_seconds = str(video_length_s[trace_file])
        args = ["-n", traces_dir + "/" + trace_file, "-m", manifest_file, "-ml", length_seconds, "-a", ABR]
        if output_dir != None: args.extend(["-o", output_dir])
        print(f'Running Sabre for {trace_file} with "{" ".join(["python", script_file] + args)}"')
        
        run_python_script(script_file, args)

def run_sabre_with_length_file():
    script_file = SABRE_DIR + "src/sabre.py"

    with open(LENGTH_JSON_FILE) as lenfile:
        len_data = json.load(lenfile)

    run_sabre(script_file, len_data)

def main():
    if len(sys.argv) > 1:
        video_len_s = int(sys.argv[1])
        output_dir = sys.argv[2]
    
    try:
        print("Splitting trace files into temporary dir.")
        # Create a temporary directory for the split trace files
        os.mkdir(TEMP_TRACES_DIR)
        split_trace_files(video_len_s, TEMP_TRACES_DIR)
        
        run_sabre("src/sabre.py", video_len_s, fixed_len=True, traces_dir=TEMP_TRACES_DIR, output_dir=output_dir)
        print("Done.")

        print("Removing temp trace dir.")
        for file in os.listdir(TEMP_TRACES_DIR): os.remove(f"{TEMP_TRACES_DIR}/{file}")
        os.rmdir(TEMP_TRACES_DIR)
        
    except Exception as e:
        for file in os.listdir(TEMP_TRACES_DIR): os.remove(f"{TEMP_TRACES_DIR}/{file}")
        os.rmdir(TEMP_TRACES_DIR)
        raise e

if __name__ == "__main__":
    #print(sys.argv[1])
    main()