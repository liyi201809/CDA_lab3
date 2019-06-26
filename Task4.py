from loaddata import load_data
import csv
from matplotlib import pyplot
import pandas as pd

dataset = load_data('capture20110811.pcap.netflow.labeled')

dataset_botnet = dataset[dataset['Label']=='Botnet']
ip_to_analyse = dataset_botnet.iloc[0]['src_ip']

all_data_ip_to_analyse = dataset[dataset['src_ip']==ip_to_analyse]
botnet_data_ip_to_analyze = dataset_botnet[dataset_botnet['src_ip']==ip_to_analyse]

features = ['Prot', 'Packets']


def get_markov_chain(feature, data):
    transition_counts = {
    }

    # print(data.size)
    # print(ngram_length)


    old_state = None
    for state in data[feature]:
        # print(state)
        # ngram = str(data[feature][i])
        # for j in range(i, i+ngram_length):
        #     ngram += '{}, '.format(data.at[j, data[feature]])

        if old_state is not None:
            # print(old_state)
            if old_state not in transition_counts:
                transition_counts[old_state] = {'total': 0}
            if state not in transition_counts[old_state]:
                transition_counts[old_state][state] = 0
            transition_counts[old_state][state] += 1
            transition_counts[old_state]['total'] += 1
        old_state = state

    result = {}
    for in_state, out_states in transition_counts.items():
        result[in_state] = {}
        for out_state, amount in out_states.items():
            if out_state=='total':
                result[in_state]['total'] = transition_counts[in_state]['total']
                continue
            result[in_state][out_state] = amount /transition_counts[in_state]['total']

    return result

def get_markov_distance(markov, markov2):
    # warning, does not use an actual distance. as the distance form a to b != distance b to a

    distance = 0

    for from_state, to_states in markov.items():
        if from_state not in markov2:
            continue
        for to_state, amount in to_states.items():
            if to_state not in markov2[from_state]:
                distance += amount
                continue
            if to_state == 'total':
                continue
            # print("fromState: {}, toState: {}".format(from_state, to_state))
            distance += amount - markov2[from_state][to_state]

    return distance


def match_markov_chain(feature, data, data2):
    markov = get_markov_chain(feature, data)
    markov2 = get_markov_chain(feature, data2)
    return get_markov_distance(markov, markov2)

#match the markov chain and store results, also show the botnet markov chain
print(get_markov_chain(features[1], dataset_botnet))
types = ['LEGITIMATE', 'Botnet', 'Background']
n_per_type = 100


with open('dataset.csv', 'w', newline='') as csvfile:
    fieldnames = ['ip_address', 'label', 'distance']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for type in types:
        ip_addresses = dataset[dataset['Label'] == type]['src_ip'].unique()[:n_per_type]
        for ip_address in ip_addresses:
            ip_data = dataset[dataset['src_ip']==ip_address]
            label = ip_data.iloc[0]['Label']

            writer.writerow({'ip_address': ip_address, 'label': label, 'distance': match_markov_chain(features[1], botnet_data_ip_to_analyze, ip_data)})

# make the plots and get the accuracies
df = pd.read_csv('dataset.csv')


df = df.sort_values('label').reset_index(drop=True)
print(df)

labels = ['LEGITIMATE', 'Botnet', 'Background']
colors = ['green', 'red', 'yellow']
for label, color in zip(labels, colors):
    pyplot.plot(df[df['label']==label]['distance'], color = color, label=label)
pyplot.legend()
pyplot.show()


pred_df = df[df['distance']<3.5]
print(pred_df[pred_df['label']=='Botnet'].size)
print(df[df['label']=='Botnet'].size)
TP = pred_df[pred_df['label']=='Botnet'].size/df[df['label']=='Botnet'].size
FP_background = pred_df[pred_df['label']=='Background'].size/df[df['label']=='Background'].size
FP_legitimate = pred_df[pred_df['label']=='LEGITIMATE'].size/df[df['label']=='LEGITIMATE'].size

print('found an accuracy of {}, with false legitimate positives {} and background FP: {}'.format(TP, FP_legitimate, FP_background))