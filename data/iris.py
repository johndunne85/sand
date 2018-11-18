import numpy as np
import pandas as pd
from torch.utils.data.dataset import Dataset

label_idx = {'loss': 1, 'win': 2, }

class IrisDataset(Dataset):

    def __init__(self, data):
        self.data = data

    def __getitem__(self, index):
        item = self.data.iloc[index].values

        return (item[0:10].astype(np.float32), item[10].astype(np.int))

    def __len__(self):
        return self.data.shape[0]

def get_datasets(iris_file):

    labels = {'class': label_idx}
    data = pd.read_csv(iris_file)
    data.replace(labels, inplace=True)

    train_df = data.sample()
    test_df = data.loc[~data.index.isin(train_df.index), :]

    return IrisDataset(train_df), IrisDataset(test_df)
