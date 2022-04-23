def Sum_Cube(k):
  if ((k - 4) % 9 != 0) and ((k - 5) % 9 != 0) and abs(k) <= 10000:
    if k == -1:
      print(-1, " ", 1, " ", -1)
      return
    for i in range(1,abs(k) + 1):
      if ((i*i*i) <= k) or ((-(i*i*i)) >= k):
        for i_ele in [-i, i]:
          temp = i_ele*i_ele*i_ele
          for j in range(1,(abs(k) - temp) + 1):
            if ((j*j*j) <= (k - temp)) or (-(j*j*j) >= (k-temp)):
              for j_ele in [-j,j]:
                temp_2 = j_ele*j_ele*j_ele
                for m in range(1,(abs(k) - temp - temp_2) + 1):
                  if ((m*m*m) == (k- temp - temp_2)):
                    print(i_ele,' ',j_ele,' ',m)
                    return
                  elif (-(m*m*m) == (k-temp-temp_2)):
                    print(i_ele,' ',j_ele,' ',-m)
                    return
    print(0, " ", 0, " ", 0)
  else:
    print(0," ", 0, " ", 0)
k = int(input())
Sum_Cube(k)