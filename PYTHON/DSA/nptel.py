'''
What does h(27993) return for the following function definition?

def h(x):
    (d,n) = (1,0)
    while d <= x:
        (d,n) = (d*3,n+1)
    return(n)
10
Yes, the answer is correct.
Score: 2.5
Feedback:
The function computes the smallest power of 3 that is bigger than x. Effectively, it computes the number of digits in the base 3 representation of x.
Accepted Answers:
(Type: Numeric) 10
2.5 points
What is g(60) - g(48), given the definition of g below?

def g(n): 
    s=0
    for i in range(2,n):
        if n%i == 0:
           s = s+1
    return(s)
2
Yes, the answer is correct.
Score: 2.5
Feedback:
g(n) counts the number of factors of n, excluding 1 and n.

Accepted Answers:
(Type: Numeric) 2
2.5 points
2.5 points
Consider the following function f.

def f(n): 
    s=0
    for i in range(1,n+1):
        if n//i == i and n%i == 0:
           s = 1
    return(s%2 == 1)
The function f(n) given above returns True for a positive number n if and only if:

 n is an odd number.
 n is a prime number.
 n is a perfect square.
 n is a composite number.
Yes, the answer is correct.
Score: 2.5
Feedback:
f(n) sets s to 1 if there is a number i such that i*i == n.
Accepted Answers:
n is a perfect square.
2.5 points
Consider the following function foo.

def foo(m):
    if m == 0:
      return(0)
    else:
      return(m+foo(m-1))
Which of the following is correct?

 The function always terminates with foo(n) = factorial of n
 The function always terminates with foo(n) = n(n+1)/2
 The function terminates for non­negative n with foo(n) = factorial of n
 The function terminates for non­negative n with foo(n) = n(n+1)/2
Yes, the answer is correct.
Score: 2.5
Feedback:
If m is negative, the function does not terminate. Otherwise, it computes 1+2+..+m = m(m+1)/2.

Accepted Answers:
The function terminates for non­negative n with foo(n) = n(n+1)/2


week-2
One of the following 10 statements generates an error. Which one? (Your answer should be a number between 1 and 10.)

x = [[3,5],"mimsy",2,"borogove",1]  # Statement 1
y = x[0:50]                          # Statement 2
z = y                                # Statement 3
w = x                                # Statement 4
x[1] = x[1][:5] + 'ery'              # Statement 5
y[1] = 4                             # Statement 6
w[1][:3] = 'fea'                     # Statement 7
z[4] = 42                            # Statement 8
x[0][0] = 5555                       # Statement 9
a = (x[3][1] == 1)                   # Statement 10
7
Yes, the answer is correct.
Score: 2.5
Feedback:
At statement 7, w[1] is the string "mimsy", which cannot be updated in place.

Accepted Answers:
(Type: Numeric) 7
2.5 points
2.5 points
Consider the following lines of Python code.

b = [43,99,65,105,4]
a = b[2:]
d = b[1:]
c = b
d[1] = 95
b[2] = 47
c[3] = 73
Which of the following holds at the end of this code?

 a[0] == 47, b[3] == 73, c[3] == 73, d[1] == 47
 a[0] == 65, b[3] == 105, c[3] == 73, d[1] == 95
 a[0] == 65, b[3] == 73, c[3] == 73, d[1] == 95
 a[0] == 95, b[3] == 73, c[3] == 73, d[1] == 95
Yes, the answer is correct.
Score: 2.5
Feedback:
a[0] == 65, b[3] == 73, c[3] == 73, d[1] == 95
b and c refer to the same list, while a and d are two independent slices. The update to d[1] does not affect any other list. The update to b[2] does not affect a or d. The update to c[3] is also reflected in b[3].

Accepted Answers:
a[0] == 65, b[3] == 73, c[3] == 73, d[1] == 95
What is the value of endmsg after executing the following lines?
startmsg = "anaconda"
endmsg = ""
for i in range(1,1+len(startmsg)):
  endmsg = endmsg + startmsg[-i]
adnocana
No, the answer is incorrect.
Score: 0
Feedback:
"adnocana"
The loop copies each letter in startmsg from right to left to the end of endmsg, so the resulting string is the reverse of the original string.

Accepted Answers:
(Type: Regex Match) \s*\'adnocana\'\s*
(Type: Regex Match) \s*\"adnocana\"\s*
2.5 points
What is the value of mylist after the following lines are executed?
def mystery(l):
  l = l[2:]
  return(l)

mylist = [7,11,13,17,19,21]
mystery(mylist)
[7,11,13,17,19,21]
Yes, the answer is correct.
Score: 2.5
Feedback:
[7,11,13,17,19,21]
The update l = l[2:] inside the function creates a new list, so the list passed as the argument is not changed.

Accepted Answers:
(Type: Regex Match) \s*\[\s*7,\s*11,\s*13,\s*17,\s*19,\s*21\s*]\s*

assignment :

Write a function intreverse(n) that takes as input a positive integer n and returns the integer obtained by reversing the digits in n.

Here are some examples of how your function should work.

>>> intreverse(783)
387
>>> intreverse(242789)
987242
>>> intreverse(3)
3
Write a function matched(s) that takes as input a string s and checks if the brackets "(" and ")" in s are matched: that is, every "(" has a matching ")" after it and every ")" has a matching "(" before it. Your function should ignore all other symbols that appear in s. Your function should return True if s has matched brackets and False if it does not.

Here are some examples to show how your function should work.

 
>>> matched("zb%78")
True
>>> matched("(7)(a")
False
>>> matched("a)*(?")
False
>>> matched("((jkl)78(A)&l(8(dd(FJI:),):)?)")
True
Write a function sumprimes(l) that takes as input a list of integers l and retuns the sum of all the prime numbers in l.

Here are some examples to show how your function should work.

>>> sumprimes([3,3,1,13])
19
>>> sumprimes([2,4,6,9,11])
13
>>> sumprimes([-3,1,6])
0
Private Test cases used for evaluation	Input	Expected Output	Actual Output	Status
Test Case 1	
intreverse(31511)
 11513
11513\n
Passed
Test Case 2	
intreverse(4)
 4
4\n
Passed
Test Case 3	
intreverse(15135324234235)
 53243242353151
53243242353151\n
Passed
Test Case 4	
matched("a3qw3;4w3(aasdgsd)((agadsgdsgag)agaga)")
 True
True\n
Passed
Test Case 5	
matched("(ag(Gaga(agag)Gaga)GG)a)33)cc(")
 False
False\n
Passed
Test Case 6	
matched("(adsgdsg(agaga)a")
 False
False\n
Passed
Test Case 7	
matched("15ababa.agaga[][[[")
 True
True\n
Passed
Test Case 8	
sumprimes([101,93,97,44])
 198
198\n
Passed
Test Case 9	
sumprimes([1001,393,743,59])
 802
802\n
Passed
Test Case 10	
sumprimes([11,11,11,13,11,-11])
 57
57\n
Passed

The due date for submitting this assignment has passed.
10 out of 10 tests passed.
You scored 100.0/100.

Assignment submitted on 2024-08-03, 22:34 IST
Your last recorded submission was :
1
def intreverse(n):
2
 
3
  reversed_n = 0
4
  while n > 0:
5
    digit = n % 10
6
    reversed_n = reversed_n * 10 + digit
7
    n //= 10
8
  return reversed_n
9
def matched(s):
10
 
11
  count = 0
12
  for char in s:
13
    if char == '(':
14
      count += 1
15
    elif char == ')':
16
      count -= 1
17
    if count < 0:
18
      return False
19
  return count == 0
20
def sumprimes(l):
21
 
22
  sum = 0
23
  for num in l:
24
    if num > 1 and is_prime(num):
25
      sum += num
26
  return sum
27
def is_prime(num):
28
  """Checks if a number is prime."""
29
  if num <= 1:
30
    return False
31
  for i in range(2, int(num**0.5) + 1):
32
    if num % i == 0:
33
      return False
34
  return True
35
import ast
36
​
37
def tolist(inp):
38
  inp = "["+inp+"]"
39
  inp = ast.literal_eval(inp)
40
  return (inp[0],inp[1])
41
​
42
def parse(inp):
43
  inp = ast.literal_eval(inp)
44
  return (inp)
45
​
46
fncall = input()
47
lparen = fncall.find("(")
48
rparen = fncall.rfind(")")
49
fname = fncall[:lparen]
50
farg = fncall[lparen+1:rparen]
51
​
52
if fname == "intreverse":
53
   arg = parse(farg)
54
   print(intreverse(arg))
55
elif fname == "matched":
56
   arg = parse(farg)
57
   print(matched(arg))
58
elif fname == "sumprimes":
59
   arg = parse(farg)
60
   print(sumprimes(arg))

else:

   print("Function", fname, "unknown")
Sample solutions (Provided by instructor)


//original by nptel
def intreverse(n):

  ans = 0

  while n > 0:

    (d,n) = (n%10,n//10)

    ans = 10*ans + d

  return(ans)

​

def matched(s):

  nested = 0

  for i in range(0,len(s)):

    if s[i] == "(":

       nested = nested+1

    elif s[i] == ")":

       nested = nested-1

       if nested < 0:

          return(False)    

  return(nested == 0)

​

def factors(n):

  factorlist = []

  for i in range(1,n+1):

    if n%i == 0:

      factorlist = factorlist + [i]

  return(factorlist)

​

def isprime(n):

  return(factors(n) == [1,n])

​

​

def sumprimes(l):

  sum = 0

  for i in range(0,len(l)):

    if isprime(l[i]):

      sum = sum+l[i]

  return(sum)

import ast

​

def tolist(inp):

  inp = "["+inp+"]"

  inp = ast.literal_eval(inp)

  return (inp[0],inp[1])

​

def parse(inp):

  inp = ast.literal_eval(inp)

  return (inp)

​

fncall = input()

lparen = fncall.find("(")

rparen = fncall.rfind(")")

fname = fncall[:lparen]

farg = fncall[lparen+1:rparen]

​

if fname == "intreverse":

   arg = parse(farg)

   print(intreverse(arg))

elif fname == "matched":

   arg = parse(farg)

   print(matched(arg))

elif fname == "sumprimes":

   arg = parse(farg)

   print(sumprimes(arg))

else:

   print("Function", fname, "unknown")

Your last saved code is :
def intreverse(n):

 

  reversed_n = 0

  while n > 0:

    digit = n % 10

    reversed_n = reversed_n * 10 + digit

    n //= 10
  return reversed_n

def matched(s):
  count = 0

  for char in s:
    if char == '(':

      count += 1

    elif char == ')':

      count -= 1

    if count < 0:

      return False

  return count == 0

def sumprimes(l):

 

  sum = 0

  for num in l:

    if num > 1 and is_prime(num):

      sum += num

  return sum

def is_prime(num):
  """Checks if a number is prime."""

  if num <= 1:

    return False

  for i in range(2, int(num**0.5) + 1):

    if num % i == 0:

      return False

  return True

import ast

​
def tolist(inp):

  inp = "["+inp+"]"

  inp = ast.literal_eval(inp)

  return (inp[0],inp[1])

​

def parse(inp):

  inp = ast.literal_eval(inp)

  return (inp)

​

fncall = input()

lparen = fncall.find("(")

rparen = fncall.rfind(")")

fname = fncall[:lparen]

farg = fncall[lparen+1:rparen]

​

if fname == "intreverse":

   arg = parse(farg)

   print(intreverse(arg))

elif fname == "matched":

   arg = parse(farg)

   print(matched(arg))

elif fname == "sumprimes":

   arg = parse(farg)

   print(sumprimes(arg))

else:

   print("Function", fname, "unknown")

week 3

assig : 
Write a function contracting(l) that takes as input a list of integer l and returns True if the absolute difference between each adjacent pair of elements strictly decreases.

Here are some examples of how your function should work.

  >>> contracting([9,2,7,3,1])
  True

  >>> contracting([-2,3,7,2,-1]) 
  False

  >>> contracting([10,7,4,1])
  False
In a list of integers l, the neighbours of l[i] are l[i-1] and l[i+1]. l[i] is a hill if it is strictly greater than its neighbours and a valley if it is strictly less than its neighbours.
Write a function counthv(l) that takes as input a list of integers l and returns a list [hc,vc] where hc is the number of hills in l and vc is the number of valleys in l.

Here are some examples to show how your function should work.

 
>>> counthv([1,2,1,2,3,2,1])
[2, 1]

>>> counthv([1,2,3,1])
[1, 0]

>>> counthv([3,1,2,3])
[0, 1]

A square n×n matrix of integers can be written in Python as a list with n elements, where each element is in turn a list of n integers, representing a row of the matrix. For instance, the matrix

  1  2  3
  4  5  6
  7  8  9
would be represented as [[1,2,3], [4,5,6], [7,8,9]].

Write a function leftrotate(m) that takes a list representation m of a square matrix as input, and returns the matrix obtained by rotating the original matrix counterclockwize by 90 degrees. For instance, if we rotate the matrix above, we get

  3  6  9
  2  5  8    
  1  4  7
Your function should not modify the argument m provided to the function rotate().

Here are some examples of how your function should work.

 
  >>> leftrotate([[1,2],[3,4]])
  [[2, 4], [1, 3]]

  >>> leftrotate([[1,2,3],[4,5,6],[7,8,9]])
  [[3, 6, 9], [2, 5, 8], [1, 4, 7]]

  >>> leftrotate([[1,1,1],[2,2,2],[3,3,3]])
  [[1, 2, 3], [1, 2, 3], [1, 2, 3]]

  def contracting(l):
  
  if len(l) <= 2:
    return True
  for i in range(1,len(l)-1):
    
    diff1 = abs(l[i] - l[i - 1])
    diff2 = abs(l[i + 1] - l[i])
    if diff2 >= diff1:
      return False
  return True


def counthv(l):
 
  hc = 0
  vc = 0
  for i in range(1, len(l) - 1):
    if l[i] > l[i - 1] and l[i] > l[i + 1]:
      hc += 1
    elif l[i] < l[i - 1] and l[i] < l[i + 1]:
      vc += 1
  return [hc, vc]

def leftrotate(m):
    size = len(m)
    rotated_m = []
    for i in range(size):
        rotated_m.append([])
    for c in range(size-1,-1,-1):
        for r in range(size):
            rotated_m[size-(c+1)].append(m[r][c])
    return(rotated_m)
import ast

def parse(inp):
  inp = ast.literal_eval(inp)
  return (inp)

fncall = input()
lparen = fncall.find("(")
rparen = fncall.rfind(")")
fname = fncall[:lparen]
farg = fncall[lparen+1:rparen]

if fname == "contracting":
  arg = parse(farg)
  print(contracting(arg))

if fname == "counthv":
  arg = parse(farg)
  print(counthv(arg))

if fname == "leftrotate":
  arg = parse(farg)
  savearg = arg
  ans = leftrotate(arg)
  if savearg == arg:
    print(ans)
  else:
    print("Side effect")

    week - 4

    
Consider the following Python function.
def mystery(l):
    if l == []:
        return(l)
    else:
        return(mystery(l[1:])+l[:1])
What does mystery([22,14,19,65,82,55]) return?
[55,82,65,19,14,22]
Yes, the answer is correct.
Score: 2.5
Feedback:
Elements are moved from the beginning of the list to the end, so the list gets reversed.
Accepted Answers:
(Type: Regex Match) [ ]*[[ ]*55[ ]*,[ ]*82[ ]*,[ ]*65[ ]*,[ ]*19[ ]*,[ ]*14[ ]*,[ ]*22[ ]*][ ]*
2.5 points
What is the value of pairs after the following assignment?
pairs = [ (x,y) for x in range(4,1,-1) for y in range(5,1,-1) if (x+y)%3 == 0 ]
[(4,5),(4,2),(3,3),(2,4)]
Yes, the answer is correct.
Score: 2.5
Feedback:
All pairs (i,j) with i ∈ {4,3,2}, j ∈ {5,4.3,2} such that i + j is a multiple of 3,
Accepted Answers:
(Type: Regex Match) [ ]*[[ ]*\([ ]*4[ ]*,[ ]*5[ ]*\)[ ]*,[ ]*\([ ]*4[ ]*,[ ]*2[ ]*\)[ ]*,[ ]*\([ ]*3[ ]*,[ ]*3[ ]*\)[ ]*,[ ]*\([ ]*2[ ]*,[ ]*4[ ]*\)[ ]*][ ]*
2.5 points
2.5 points
Consider the following dictionary.
wickets = {"Tests":{"Bumrah":[3,5,2,3],"Shami":[4,4,1,0],"Ashwin":[2,1,7,4]},"ODI":{"Bumrah":[2,0],"Shami":[1,2]}}
Which of the following statements does not generate an error?
 wickets["ODI"]["Ashwin"][0:] = [4,4]
 wickets["ODI"]["Ashwin"].extend([4,4])
 wickets["ODI"]["Ashwin"] = [4,4]
 wickets["ODI"]["Ashwin"] = wickets["ODI"]["Ashwin"] + [4,4]
Yes, the answer is correct.
Score: 2.5
Feedback:
Direct assignment to a new key adds a value. All other updates result in KeyError.
Accepted Answers:
wickets["ODI"]["Ashwin"] = [4,4]
2.5 points
Assume that hundreds has been initialized as an empty dictionary:
hundreds = {}
Which of the following generates an error?
 hundreds["Tendulkar, international"] = 100
 hundreds["Tendulkar"] = {"international":100}
 hundreds[("Tendulkar","international")] = 100
 hundreds[["Tendulkar","international"]] = 100
Yes, the answer is correct.
Score: 2.5
Feedback:
Dictionary keys must be immutable values.
Accepted Answers:
hundreds[["Tendulkar","international"]] = 100

assignment : 

Write a Python function frequency(l) that takes as input a list of integers and returns a pair of the form (minfreqlist,maxfreqlist) where

minfreqlist is a list of numbers with minimum frequency in l, sorted in ascending order
maxfreqlist is a list of numbers with maximum frequency in l, sorted in ascending order
Here are some examples of how your function should work.

>>> frequency([13,12,11,13,14,13,7,11,13,14,12])
([7], [13])

>>> frequency([13,12,11,13,14,13,7,11,13,14,12,14,14])
([7], [13, 14])

>>> frequency([13,12,11,13,14,13,7,11,13,14,12,14,14,7])
([7, 11, 12], [13, 14])
An airline has assigned each city that it serves a unique numeric code. It has collected information about all the direct flights it operates, represented as a list of pairs of the form (i,j), where i is the code of the starting city and j is the code of the destination.

It now wants to compute all pairs of cities connected by one intermediate hope — city i is connected to city j by one intermediate hop if there are direct flights of the form (i,k) and (k,j) for some other city k. The airline is only interested in one hop flights between different cities — pairs of the form (i,i) are not useful.

Write a Python function onehop(l) that takes as input a list of pairs representing direct flights, as described above, and returns a list of all pairs (i,j), where i != j, such that i and j are connected by one hop. Note that it may already be the case that there is a direct flight from i to j. So long as there is an intermediate k with a flight from i to k and from k to j, the list returned by the function should include (i,j). The input list may be in any order. The pairs in the output list should be in lexicographic (dictionary) order. Each pair should be listed exactly once.

Here are some examples of how your function should work.

 
>>> onehop([(2,3),(1,2)])
[(1, 3)]

>>> onehop([(2,3),(1,2),(3,1),(1,3),(3,2),(2,4),(4,1)])
[(1, 2), (1, 3), (1, 4), (2, 1), (3, 2), (3, 4), (4, 2), (4, 3)]

>>> onehop([(1,2),(3,4),(5,6)])
[]

def frequency(l):
    freq_dict = {}
    for num in l:
        if num in freq_dict:
            freq_dict[num] += 1
        else:
            freq_dict[num] = 1
    
    min_freq = min(freq_dict.values())
    max_freq = max(freq_dict.values())
    
    minfreqlist = [num for num, freq in freq_dict.items() if freq == min_freq]
    maxfreqlist = [num for num, freq in freq_dict.items() if freq == max_freq]
    
    return (sorted(minfreqlist), sorted(maxfreqlist))
  

  
def onehop(l):
    direct = {}
    for (i,j) in l:
        if i in direct.keys():
            direct[i].append(j)
        else:
            direct[i] = [j]
    hopping = []
    for src in direct.keys():
        for dest in direct[src]:
            if dest in direct.keys():
                for remote in direct[dest]:
                    if src != remote:
                        hopping.append((src,remote))
    return(remdup(sorted(hopping)))
  
def remdup(l):
    if len(l) < 2:
        return(l)
    if l[0] != l[1]:
        return(l[0:1]+remdup(l[1:]))
    else:
        return(remdup(l[1:]))
import ast

def parse(inp):
  inp = ast.literal_eval(inp)
  return (inp)

fncall = input()
lparen = fncall.find("(")
rparen = fncall.rfind(")")
fname = fncall[:lparen]
farg = fncall[lparen+1:rparen]

if fname == "frequency":
  arg = parse(farg)
  print(frequency(arg))

if fname == "onehop":
  arg = parse(farg)
  print(onehop(arg))


  week 5 

  Suppose u and v both denote sets in Python. What is the most general condition that guarantees that u - (v - u) == u?
 The sets u and v should be disjoint.
 The set v should be a subset of the set u.
 The set u should be a subset of the set v.
 This is true for any u and v.
No, the answer is incorrect.
Score: 0
Feedback:
v - u, by definition, has no elements from u. Hence u - (v - u) does not remove any elements from u.
Accepted Answers:
This is true for any u and v.
2.5 points
Suppose u and v both denote sets in Python. What is the most general condition that guarantees that u|v == u^v?
 The sets u and v should be disjoint.
 The set u should be a subset of the set v.
 The set v should be a subset of the set u.
 This is true for any u and v.
No, the answer is incorrect.
Score: 0
Feedback:
u^v has all elements that are in exactly one of u or v. This is the same as u|v - u&v. Since u^v = u|v, we have u&v is empty, so u and v are disjoint.
Accepted Answers:
The sets u and v should be disjoint.
Suppose we insert 19 into the min heap [17,25,42,67,38,89,54,98,89]. What is the resulting heap?
No, the answer is incorrect.
Score: 0
Feedback:

WEEK 6

The original heap is
             17
          /       \
      25            42
     /  \          /  \
  67      38    89      54
 /  \
98  89
After inserting 19, the new heap is
             17
          /      \
      19            42
     /  \          /  \
  67      25    89      54
 /  \    /  
98  89  38
Accepted Answers:
(Type: Regex Match) [ ]*[[ ]*17[ ]*,[ ]*19[ ]*,[ ]*42[ ]*,[ ]*67[ ]*,[ ]*25[ ]*,[ ]*89[ ]*,[ ]*54[ ]*,[ ]*98[ ]*,[ ]*89[ ]*,[ ]*38[ ]*][ ]*
2.5 points
Suppose we execute delete-min twice on the min-heap [13,29,24,67,52,89,45,98,79,58]. What is the resulting heap?
No, the answer is incorrect.
Score: 0
Feedback:
The original heap is:

             13
          /      \
      29            24
    /    \        /    \
  67      52    89      45
 /  \    /  
98  79  58
After one delete-min, we have:

             24
          /      \
      29            45
    /    \        /    \
  67      52    89      58
 /  \  
98  79
After the second delete-min, we have:

             29
          /      \
      52            45
    /    \        /    \
  67      79    89      58
 / 
98
Accepted Answers:
(Type: Regex Match) [ ]*[29[ ]*,[ ]*52[ ]*,[ ]*45[ ]*,[ ]*67[ ]*,[ ]*79[ ]*,
[ ]*89[ ]*,[ ]*58[ ]*,[ ]*98[ ]*][ ]*


WEEK 7 

Given the following permutation of a,b,c,d,e,f,g,h,i,j, what is the next permutation in lexicographic (dictionary) order? Write your answer without any blank spaces between letters.
    fjadbihgec
fjadcbeghi
Yes, the answer is correct.
Score: 2.5
Feedback:
The prefix to change is bihgec. This becomes cbeghi
Accepted Answers:
(Type: Regex Match) [ ]*fjadcbeghi[ ]*
(Type: Regex Match) [ ]*\"fjadcbeghi\"[ ]*
(Type: Regex Match) [ ]*\'fjadcbeghi\'[ ]*
2.5 points
2.5 points
We want to add a function length() to the class Node that implements user defined lists which will compute the length of a list. An incomplete implementation of length() given below. You have to provide expressions to put in place of XXX, YYY. and ZZZ.

    
def length(self):
  if self.value == None:
     return(XXX)
  elif self.next == None:
     return(YYY)
  else:
     return(ZZZ)
 XXX: 0, YYY: 0, ZZZ: self.next.length()
 XXX: 0, YYY: 0, ZZZ: 1 + self.next.length()
 XXX: 0, YYY: 1, ZZZ: self.next.length()
 XXX: 0, YYY: 1, ZZZ: 1 + self.next.length()
Yes, the answer is correct.
Score: 2.5
Feedback:
Inductive definition: if empty, return 0, if singleton return 1, else add 1 to the length of the list starting at self.next.
Accepted Answers:
XXX: 0, YYY: 1, ZZZ: 1 + self.next.length()
2.5 points
Suppose we add this function foo() to the class Tree that implements search trees. For a name mytree with a value of type Tree, what would mytree.foo() compute?

    def foo(self):
        if self.isempty():
            return(0)
        elif self.isleaf():
            return(1)
        else:
            return(self.left.foo() + self.right.foo()))
 The number of nodes in mytree
 The largest value in mytree.
 The length of the longest path from root to leaf in mytree.
 The number of leaves in mytree.
Yes, the answer is correct.
Score: 2.5
Feedback:
This computes the number of leaves in the tree. An empty tree has no leaves. A tree with just one node has a single leaf. Otherwise, compute the number of leaves in left and right subtrees and add them.

This does not compute the number of nodes in the tree. For that, we need to add 1 in the inductive case, to account for the current node. So the else: expression would be return(1 + self.left.foo() + self.right.foo())).

Accepted Answers:
The number of leaves in mytree.
Inorder traversal of a binary tree has been defined in the lectures. A preorder traversal lists the vertices of a binary tree (not necessarily a search tree) as follows:
Print the root.
Print the left subtree in preorder.
Print the right subtree in preorder.
Suppose we have a binary tree with 10 nodes labelled a, b, c, d, e, f, g, h, i, j, with preorder traversal gbhecidajf and inorder traversal ehbicgjafd. What is the right child of the root node?
d
Hint
Yes, the answer is correct.
Score: 2.5
Feedback:
From the preorder traversal, g is the root. The inorder traversal tells us that jafd lie to the right of the root. The preorder traversal of this segment says d is the root of this subtree, so d is the right child of the root.
Accepted Answers:
(Type: Regex Match) [ ]*d[ ]*
(Type: Regex Match) [ ]*"d"[ ]*
(Type: Regex Match) [ ]*'d'[ ]*

week - 8 

IOI Training Camp 20xx
(INOI 2011)

We are well into the 21st century and school children are taught dynamic programming in class 4. The IOI training camp has degenerated into an endless sequence of tests, with negative marking. At the end of the camp, each student is evaluated based on the sum of the best contiguous segment (i.e., no gaps) of marks in the overall sequence of tests.

Students, however, have not changed much over the years and they have asked for some relaxation in the evaluation procedure. As a concession, the camp coordinators have agreed that students are allowed to drop upto a certain number of tests when calculating their best segment.

For instance, suppose that Lavanya is a student at the training camp and there have been ten tests, in which her marks are as follows.

Test	  1  	   2  	  3  	   4  	  5  	   6  	   7  	   8  	   9  	  10  
Marks	  6  	  -5  	  3  	  -7  	  6  	  -1  	  10  	  -8  	  -8  	  8  
In this case, without being allowed to drop any tests, the best segment is tests 5–7, which yields a total of 15 marks. If Lavanya is allowed to drop upto 2 tests in a segment, the best segment is tests 1–7, which yields a total of 24 marks after dropping tests 2 and 4. If she is allowed to drop upto 6 tests in a segment, the best total is obtained by taking the entire list and dropping the 5 negative entries to get a total of 33.

You will be given a sequence of N test marks and a number K. You have to compute the sum of the best segment in the sequence when upto K marks may be dropped from the segment.

Solution hint
For 1 ≤ i ≤ N, 1 ≤ j ≤ K, let Best[i][j] denote the maximum segment ending at position i with at most j marks dropped. Best[i][0] is the classical maximum subsegment or maximum subarray problem. For j ≥ 1; inductively compute Best[i][j] from Best[i][j-1].

Input format
The first line of input contains two integers N and K, where N is the number of tests for which marks will be provided and K is the limit of how many entries may be dropped from a segment.

This is followed by N lines of input each containing a single integer. The marks for test i, i ∈ {1,2,…,N} are provided in line i+1.

Output format
The output is a single number, the maximum marks that can be obtained from a segment in which upto K values are dropped.

Constraints
You may assume that 1 ≤ N ≤ 104 and 0 ≤ K ≤ 102. The marks for each test lie in the range [-104 … 104]. In 40% of the cases you may assume N ≤ 250.

Example:
We now illustrate the input and output formats using the example described above.
Sample input:
10 2
6
-5
3
-7
6
-1
10
-8
-8
8
Sample output:
24

N,K = list(map(int,input().split()))
f = [0]
output = 0
for a in range(N):
    f.append(int(input()))
score = [[0 for i in range(K+1)] for j in range(N+1)]
for i in range(1, N+1):
    score[i][0] = max(score[i-1][0]+f[i], f[i])
    for j in range(1, min(i+1, K+1)):
        score[i][j] = max(score[i-1][j]+f[i], score[i-1][j-1])
for i in range(1, N+1):
    output = max(output, score[i][K])
print(output, end='')


'''