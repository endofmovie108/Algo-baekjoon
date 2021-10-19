import heapq

test_list = [[1, "test", "Sdf"], [0, "what"] ]
# heapq.heappush(test_list, [1, "test", "Sdf"])
# heapq.heappush(test_list, [0, "what"])
heapq.heapify(test_list)
print(test_list)