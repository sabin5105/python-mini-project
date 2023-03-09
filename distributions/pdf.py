import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

X = np.array(np.random.randint(1, 10, 10))
density = np.random.rand(1, 10)
density = density / density.sum()   # integral = 1
PDF = np.random.choice(X, p=density[0], size=(100))
print(PDF)

sns.displot(PDF, kind="kde")
plt.show()