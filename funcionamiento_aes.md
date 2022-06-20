##  What is the AES algorithm?

>The AES algorithm (also known as the Rijndael algorithm) is a symmetrical block cipher algorithm that takes plain text in blocks of 128 bits and converts them to ciphertext using keys of 128, 192, and 256 bits. Since the AES algorithm is considered secure, it is in the worldwide standard.  
 
 <p align="center">
 <img src="https://i.imgur.com/cAeZXCm.png" width="400" height="300">


# How does AES work?
The AES algorithm uses a substitution-permutation, or SP network, with multiple rounds to produce ciphertext. The number of rounds depends on the key size being used. A 128-bit key size dictates ten rounds, a 192-bit key size dictates 12 rounds, and a 256-bit key size has 14 rounds. Each of these rounds requires a round key, but since only one key is inputted into the algorithm, this key needs to be expanded to get keys for each round, including round 0.

 <p align="center">
 <img src="https://i.imgur.com/EJF7TSe.png" width="400" height="400">

## Steps in each round
Each round in the algorithm consists of four steps.

>### 1. Substitution of the bytes
>In the first step, the bytes of the block text are substituted based >on rules dictated by predefined S-boxes (short for substitution boxes)

 <p align="center">
 <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/AES-SubBytes.svg/1280px-AES-SubBytes.svg.png" width="400" height="300">

>### 2. Shifting the rows
>Next comes the permutation step. In this step, all rows except the >first are shifted by one, as shown below.

 <p align="center">
 <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/AES-ShiftRows.svg/1920px-AES-ShiftRows.svg.png" width="400" height="300">

>### 3. Mixing the columns
>In the third step, the Hill cipher is used to jumble up the message >more by mixing the block’s columns.

 <p align="center">
 <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/AES-MixColumns.svg/1280px-AES-MixColumns.svg.png" width="400" height="300">

 >### 4. Adding the round key
>
>In the final step, the message is XORed with the respective round key.
 <p align="center">
 <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/AES-AddRoundKey.svg/800px-AES-AddRoundKey.svg.png" width="400" height="300">

 >When done repeatedly, these steps ensure that the final ciphertext >is secure.

