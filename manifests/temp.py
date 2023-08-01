import json

with open("netflix_manifest.json") as file:
    json_dict = json.load(file)

segment_dur = int(json_dict["segment_duration_ms"])
bitrates = list(json_dict["bitrates_kbps"])

segment_sizes = [br * segment_dur  for br in bitrates]
json_dict["segment_sizes_bits"] = segment_sizes

print(segment_sizes)
