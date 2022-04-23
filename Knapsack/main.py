import random

# Tạo Input từ hàm Random
def Random(N):
    randomlist = []
    for i in range(0,N):
        n = random.randint(50,100)
        randomlist.append(n)
    return randomlist


# Sử dụng hàm đệ qui để tạo Output
def knapSack_Recursion(W, wt, val, n): 
    # Base Case 
    if n == 0 or W == 0: 
        return 0 
    if (wt[n-1] > W): 
        return knapSack_Recursion(W, wt, val, n-1) 
    else: 
        return max(val[n-1] + knapSack_Recursion(W-wt[n-1], wt, val, n-1), knapSack_Recursion(W, wt, val, n-1)) 


# Knapsack bottom up
def knapSack_BottomUp(W, wt, val, n): 
    R = [[0 for x in range(W + 1)] for x in range(n + 1)] 
    for i in range(n + 1): 
        for w in range(W + 1):
            # Base Case 
            if i == 0 or w == 0: 
                R[i][w] = 0
            elif wt[i-1] <= w: 
                R[i][w] = max(val[i-1] + R[i-1][w-wt[i-1]], R[i-1][w]) 
            else: 
                R[i][w] = R[i-1][w] 
    return R[n][W]
  

# Knapsack trace back
def knapSack_Traceback(W, wt, val, n): 
    R = [[0 for x in range(W + 1)] for x in range(n + 1)] 
    for i in range(n + 1): 
        for w in range(W + 1):
            if i == 0 or w == 0: 
                R[i][w] = 0
            elif wt[i-1] <= w: 
                R[i][w] = max(val[i-1] + R[i-1][w-wt[i-1]], R[i-1][w]) 
            else: 
                R[i][w] = R[i-1][w] 
    result = R[n][W]
    print(result)
    w = W
    for i in range(n, 0, -1):
        if result <= 0:
            break
        if result == R[i - 1][w]:
            continue
        else:
            print(wt[i - 1])
            result = result - val[i - 1]
            w = w - wt[i - 1]


# Knapsack space optimized
def knapSack_SpaceOptimize(W, wt, val, n): 
    R = [0]*(W+1)
    for i in range(n): 
        for j in range(W,wt[i],-1): 
            R[j] = max(R[j] , val[i] + R[j-wt[i]])
    return R[W]


N = random.randint(20, 50)
val = Random(N)
wt = Random(N)
W = random.randint(200, 300)
n = len(val) 
print(knapSack_Recursion(W, wt, val, n))
print(knapSack_BottomUp(W, wt, val, n))
print(knapSack_Traceback(W, wt, val, n))
print(knapSack_SpaceOptimize(W, wt, val, n))