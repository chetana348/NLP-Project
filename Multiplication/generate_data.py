import data
from torch.utils.data import DataLoader

if __name__ == "__main__":
    loader = DataLoader(data.ExpressionDataset(100000), batch_size=1)
    for sample in loader:
        print(sample[0])
