def Money(N):
  count = 0
  for i500 in range( int((N / 500000) + 1)):
    temp = i500 * 500000
    for i200 in range(int(((N-temp)/ 200000) +1)):
      temp = i500*500000 + i200* 200000
      for i100 in range( int(((N-temp)/100000 )+1 )):
        temp = i500*500000 + i200* 200000 + i100*100000
        for i50 in range( int(((N-temp)/50000 )+1 )):
          temp = i500*500000 + i200* 200000 + i100*100000 + i50*50000
          for i20 in range( int(((N-temp)/20000)+1)):
            temp = i500*500000 + i200* 200000 + i100*100000 + i50*50000 + i20*20000
            if (temp == N):
              count = count + 1
              x = i500 + i200 + i100 +i50 + i20
  print(count," ",x)
N = int(input())
Money(N)