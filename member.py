# import libraries
import pickle as pkl

dict = {}

# initialize a users database
with open('database/users.pkl', 'wb') as f:
    pkl.dump(dict, f)