import pickle


with open("hardmob.pkl", "rb") as f:
    a = pickle.load(f)
    print(a)
