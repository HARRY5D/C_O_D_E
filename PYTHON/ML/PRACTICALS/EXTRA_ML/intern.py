import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn

print("Setup successful!")
print("NumPy version:", np.__version__)
print("Pandas version:", pd.__version__)
print("Scikit-learn version:", sklearn.__version__)


# Simple plot to test Matplotlib
plt.plot([1, 2, 3], [4, 5, 6])
plt.title("Test Plot")
plt.savefig("test_plot.png")
plt.show()
plt.close()