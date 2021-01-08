import sys
import os
import copy
import json
import defines

RECORDED_FEATURES_DIR = defines.RECORDED_FEATURES_DIR


def format_print(features_obj):
    for feature in features_obj:
        print(feature)
        for stat in features_obj[feature]["stats"]:
            val = features_obj[feature]["stats"][stat]
            sys.stdout.write(f" {stat}:")
            if type(val) == list:
                for e in val:
                    e = round(e, 2)
                    sys.stdout.write(f"{e} ")
            else:
                val = round(val, 2)
                sys.stdout.write(f"{val}")
        print()


def get_user_obj(target_filepath):
    if not os.path.isfile(target_filepath):
        user_file = open(target_filepath, "w")
        json.dump({}, user_file)
        user_file.close()
    return json.load(open(target_filepath, "r"))


def create_json(features_obj, session):
    if not os.path.isdir(RECORDED_FEATURES_DIR):
        sys.stdout.write(f"Unable to output \"{session.id}\" features for user \"{session.user}\"\n")
        return

    subset_features_obj = {}
    for feature in defines.FEATURES:
        subset_features_obj[feature] = copy.deepcopy(features_obj[feature]["stats"])

    target_filepath = f"{RECORDED_FEATURES_DIR}/{session.user}.json"

    output_obj = get_user_obj(target_filepath)
    output_obj[session.id] = copy.deepcopy(subset_features_obj)

    outfile = open(target_filepath, "w")
    json.dump(output_obj, outfile, indent=2)
