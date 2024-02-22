while True:
    p = int(input("enter p as a prime no.: "))
    if p > 1:
    	for i in range(2, int(p/2)+1):
    		if (p % i) == 0:
    			print(p, "is not a prime number")
    			break
    	else:
    		print(p, "accepted");break
    else:
    	print(p, "is not a prime number")

while True:
    q = int(input("enter q as a prime no.: "))
    if q > 1:
    	for i in range(2, int(q/2)+1):
    		if (q % i) == 0:
    			print(q, "is not a prime number")
    			break
    	else:
    		print(q, "accepted");break
    else:
    	print(q, "is not a prime number")

while True:
    A_K = int(input("enter A.key as a no.: "))
    if A_K > 1:
	    print(A_K, "accepted");break
    else:
    	print(p, "is not valid")  
        
while True:
    B_K = int(input("enter B.key as a no.: "))
    if B_K > 1:
	    print(B_K, "accepted");break
    else:
    	print(B_K, "is not valid")  
    
alice = q**A_K % p
bob = q**B_K % p
FAK = bob**A_K % p
FBK = alice**B_K % p

print("The Secret Key of Alice",FAK)
print("The Secret Key of BOB",FBK)

print("Is the secret key is the same?\n",FAK==FBK)