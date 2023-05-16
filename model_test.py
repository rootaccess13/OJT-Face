import yaml

# Create a list of labels
labels = [1]*200 + [2]*200 + [3]*200

# Save the labels to a YAML file
with open('labels.yml', 'w') as f:
    yaml.dump(labels, f)
