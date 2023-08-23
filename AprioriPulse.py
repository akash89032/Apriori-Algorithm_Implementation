import numpy as np
from collections import Counter

def load_transactions(file_path):
    transactions = []
    items_order = set()  # Using a set for faster membership checks
    items_dict = {}  # Dictionary for item indexing
    index = 1  # Starting index for items 
    with open(file_path, 'r') as file:
        for line in file:
            transaction_data = line.strip().split(',')
            unique_items = list(np.unique(transaction_data))
            transaction_id = unique_items[0]
            item_list = unique_items[1:]
            transactions.append([transaction_id, item_list])
            
            for item in item_list:
                if item not in items_order:
                    items_order.add(item)
                    items_dict[item] = index
                    index += 1
    
    items_order = sorted(items_order)
    return transactions, items_order, items_dict

def generate_item_counts(init_items, transactions_data):#c1
    item_counts = Counter()
    
    for item in init_items:
        for transaction in transactions_data:
            if item in transaction[1]:
                item_counts[item] += 1
    
    return item_counts

def generate_frequent_itemsets(candidate_counts, min_support):#l1
    frequent_itemsets = Counter()
    
    for item, count in candidate_counts.items():
        if count >= min_support:
            itemset = frozenset([item])
            frequent_itemsets[itemset] = count
    
    return frequent_itemsets

def generate_candidate_sets_of_length(prev_frequent_itemsets, length):
    candidates = set()
    prev_frequent_list = list(prev_frequent_itemsets)
    
    for i in range(len(prev_frequent_list)):
        for j in range(i + 1, len(prev_frequent_list)):
            new_candidate = prev_frequent_list[i].union(prev_frequent_list[j])
            if len(new_candidate) == length:
                candidates.add(new_candidate)
    
    return candidates

def generate_candidates_and_frequent(transactions_data, min_support, prev_frequent_itemsets, length):
    candidate_counts = Counter()
    
    for itemset in prev_frequent_itemsets:
        for transaction in transactions_data:
            transaction_items = set(transaction[1])
            if itemset.issubset(transaction_items):
                candidate_counts[itemset] += 1
    
    frequent_itemsets = Counter()
    for itemset, count in candidate_counts.items():
        if count >= min_support:
            frequent_itemsets[itemset] = count
    
    return candidate_counts, frequent_itemsets

def main():
    min_support = 2
    transactions_data, initial_items,items_dict = load_transactions('data.txt')
    candidates_1 = generate_item_counts(initial_items, transactions_data)
    frequent_1 = generate_frequent_itemsets(candidates_1, min_support)
    
    print("Candidates 1:")
    for item in candidates_1:
        print(f"[{item}]: {candidates_1[item]}")
    print()
    
    print("Frequent 1:")
    for item_set in frequent_1:
        print(f"{list(item_set)}: {frequent_1[item_set]}")
    print()
    
    prev_frequent_sets = frequent_1
    candidate_length = 1
    for count in range(2, 1000):
        new_candidates = generate_candidate_sets_of_length(prev_frequent_sets, count)
        new_candidates_list = list(new_candidates)
        candidates, frequent_sets = generate_candidates_and_frequent(transactions_data, min_support, new_candidates_list, count)
        
        print(f"Candidates {count}:")
        for item_set in candidates:
            print(f"{list(item_set)}: {candidates[item_set]}")
        print()
        
        print(f"Frequent {count}:")
        for item_set in frequent_sets:
            print(f"{list(item_set)}: {frequent_sets[item_set]}")
        print()
        
        if len(frequent_sets) == 0:
            break
        prev_frequent_sets = frequent_sets
        candidate_length = count
    
    print("Result:")
    print(f"Frequent {candidate_length}:")
    for item_set in prev_frequent_sets:
        res=list(item_set)
        res.sort(key=lambda x: items_dict[x])
        print(f"{res}: {prev_frequent_sets[item_set]}")
    print()

if __name__ == "__main__":
    main()
