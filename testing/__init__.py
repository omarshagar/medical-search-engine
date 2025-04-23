# import concurrent.futures
# import time
#
# from multiprocessing import Pool
#
# def f(x):
#     print(x)
#     time.sleep(3)
#     return x*x
#
#
# with Pool(5) as p:
#     print(p.map(f, [1, 2, 3]))
# def func():
#     print('dd')
#     time.sleep(3)
#
#
# with concurrent.futures.ProcessPoolExecutor(max_workers=4) as exexutor:
#     exexutor.map(func,[None,None,None])
#     exexutor.submit(func())
#     exexutor.submit(func())
#     exexutor.submit(func())
#     print('done 1 ')
# x=concurrent.futures.ProcessPoolExecutor()
# x.submit(func())
# print('done 3')
# print('done 2')
# Importing the threading module
import threading

deposit=0
# Function to add profit to the deposit
def add_profit():
    global deposit
    for i in range(100000):
        deposit = deposit + 10
# Function to deduct money from the deposit
def pay_bill():
    global deposit
    for i in range(100000):
        deposit= deposit - 10
def main():
    # Creating threads
    thread1 = threading.Thread(target = add_profit, args = ())
    thread2 = threading.Thread(target = pay_bill, args = ())
    # Starting the threads
    thread1.start()
    thread2.start()
    # Waiting for both the threads to finish executing
    thread1.join()
    thread2.join()
    # Displaying the final value of the deposit
for _ in range(200):
    main()
print(deposit)
