# from a list of topics create a csv with the following format:
# topic, week, distribution
# distributions from a date adds up to 1
import numpy as np
import numpy.random

topics = ["Amlo te amo", "El avión", "covid", "vacuna", "pemex"]
weeks = [i for i in range(1, 20 + 1)]

distributions = []
for date in weeks:
    distribution = []
    for topic in topics:
        distribution.append(np.random.random())
    distribution = np.array(distribution)
    distribution = distribution / np.sum(distribution)
    distributions.append(distribution)

with open("data.csv", "w") as f:
    f.write("topic,date,distribution\n")
    for i in range(len(weeks)):
        for j in range(len(topics)):
            f.write(f"{topics[j]},{weeks[i]},{distributions[i][j]}\n")
