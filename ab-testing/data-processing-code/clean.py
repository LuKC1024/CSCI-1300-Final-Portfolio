import csv
import re

# 1. Load data

table = []
with open('./../data/myfilteredlog.csv') as csvfile:
    for row in csv.reader(csvfile, delimiter=',', quotechar='|'):
        timestamp, _, _, version, start, end, elem, session = row
        table.append({
            "session": session,
            "version": version,
            "elem": elem,
            "start": start,
            "end": end
        })

users_to_actions = {r["session"]: [] for r in table}
for r in table:
    session = r["session"]
    version = r["version"]
    elem = r["elem"]
    start = r["start"]
    end = r["end"]
    assert version in list("ABC")
    if version == "C" and end == "0":
        assert elem == "0"
        users_to_actions[session].append({
            "kind": "checkout",
            "time": int(start)
        })
    elif version in list("AB") and end == "0":
        assert elem == "0"
        users_to_actions[session].append({
            "kind": "pageload",
            "version": version,
            "time": int(start)
        })
    elif version in list("AB"):
        assert elem.startswith("mp")
        users_to_actions[session].append({
            "kind": "interaction",
            "version": version,
            "start_time": int(start),
            "end_time": int(end)
        })
    else:
        assert False

# 2. Filter ill-formed sessions


def startswith_pageload(actions):
    return actions[0]["kind"] == "pageload"


def some_interaction(actions):
    for a in actions:
        if a["kind"] == "interaction":
            return True
    return False


def single_version(actions):
    versions = set([
        act["version"] for act in actions
        if act["kind"] in ["pageload", "interaction"]])
    if "A" in versions and "B" in versions:
        return None
    else:
        assert len(versions) == 1
        return list(versions)[0]


users_to_actions = {
    u: acts
    for (u, acts) in users_to_actions.items()
    if some_interaction(acts)
    and startswith_pageload(acts)
    and single_version(acts)}

print("session count after filtering:", len(users_to_actions))

# 3. extract versions, time to complete, and return

users = list(users_to_actions.keys())

users_to_version = {
    u: single_version(acts) for (u, acts) in users_to_actions.items()
}

def start_time(act):
    if act["kind"] == "interaction":
        return act["start_time"]
    else:
        return act["time"]


def end_time(act):
    if act["kind"] == "interaction":
        return act["end_time"]
    else:
        return act["time"]


users_to_time_to_completion = {}
for (u, acts) in users_to_actions.items():
    start = start_time(acts[0])
    end = end_time(acts[-1])
    assert end > start
    users_to_time_to_completion[u] = end - start


def is_returned(acts):
    for act in acts[:-1]:
        if act["kind"] == "checkout":
            return True
    return False


users_to_return = {}
for (u, acts) in users_to_actions.items():
    users_to_return[u] = is_returned(acts)

# 4. Display data

output_table_header = ['session_id', 'version', 'return', 'time_to_completion']
output_table = []
for u in users:
    output_table.append((u, users_to_version[u], users_to_return[u], users_to_time_to_completion[u]))
output_table.sort(key=lambda r: r[3])
output_table.sort(key=lambda r: r[2])
output_table.sort(key=lambda r: r[1])

print(','.join(output_table_header))
for r in output_table:
    print(','.join(map(str, r)))