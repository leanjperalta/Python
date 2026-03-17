for num in range(50, 101):  # Added missing colon
    if num < 2:
        continue
    is_prime = True
    for i in range(2, int(num ** 0.5) + 1):  # Check divisors up to the square root of num
        if (num % i) == 0:
            is_prime = False
            break
    if is_prime:
        print(num)