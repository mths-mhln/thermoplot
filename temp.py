import pickle
import numpy as np

with open("data_test_fluid_new.pkl", "rb") as f:
    data_dict_orig = pickle.load(f)
with open("data_test_fluid.pkl", "rb") as f:
    data_dict = pickle.load(f)

print(data_dict_orig)
print(data_dict)

# compare two dicts
for key in data_dict_orig.keys():
    if key not in data_dict:
        print(f"Key {key} is missing in data_dict")
        continue
    for subkey in data_dict_orig[key].keys():
        if subkey not in data_dict[key]:
            print(f"Subkey {subkey} is missing in data_dict[{key}]")
            continue
        if not np.allclose(data_dict_orig[key][subkey], data_dict[key][subkey]):
            print(f"Values for {key}[{subkey}] are not close")
            # if mismatching values are nan, then its fine
            mismatches_nan = np.isnan(data_dict_orig[key][subkey]) | np.isnan(data_dict[key][subkey])
            if np.any(mismatches_nan):
                print(f"Some mismatching values for {key}[{subkey}] are nan, which is acceptable")
                continue
            # show mismatching values
            mismatches = np.where(~np.isclose(data_dict_orig[key][subkey], data_dict[key][subkey]))
            print(f"Mismatching values for {key}[{subkey}]:")
            for idx in zip(*mismatches):
                print(f"  Index {idx}: {data_dict_orig[key][subkey][idx]} vs {data_dict[key][subkey][idx]}")