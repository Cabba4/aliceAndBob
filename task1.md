## TASK 1: What is the keyspace for the Caesar Cipher. Is it possible to implement a brute force attack on this cipher or not?

Answer 1:  Keyspace of caesar cipher is {0..25} ie all the alphabets. Yes it can be brute forced.

## TASK 2: Whay is considered an invalid K?

Answer 2: Non integer values are considered invalid K

Answer 3: Our observations are that for small text both encryption and decryption are quite fast, typically in miliseconds. Caesar cipher time complexity is O(n) so bigger n means more time will be taken. Also change in value of key doesnt change much for the time taken in encryption and decryption. 

## TASK 3: What is original message and what is key?

Answer 3: The original message is "HAVE DONE WELL TO LEARN THIS TECHNIQUE. BUT THING WILL GETMORE DIFFICULT - ADMIN" and the key is 10. Time taken was around 0.0025 seconds.