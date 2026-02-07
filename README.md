# PDC-python-calculator

# PDC=multithreading-multiprocessing
1. Which approach demonstrates true parallelism in Python? Explain.
   The multiprocessing approach demonstrates true parallelism because it uses separate memory and CPU cores for each task through the "multiprocessing" module, which bypasses the GIL by giving each process its own Python interpeter and memory space.

2. Compare execution times between multithreading and multiprocessing.
   | Method | Execution Pattern | GWA Output | Time |
   | :--- | :--- | :--- | :--- |
   | **Multithreading** | Interleaved | 90.00 | 0.0007s |
   | **Multiprocessing** | Sequential* | 90.00 | 0.0186s |
   This table highlights the speed difference, where threading is much faster for smaller tasks. 

3. Can Python handle true parallelism using threads? Why or why not?
   No, Python cannot handle true parallelism using threads. Python has a mechanism called the GIL (Global Interpreter Lock), which is essentially a physical lock that only allows one thread to hold control of the interpreter for Python at a time.

4. What happens if you input a large number of grades (e.g., 1000)? Which method is faster and why?
   Multithreading is faster in the case if you inputted a large number of grades as the low complexity of calculating the average for the GWA makes it the best option in terms of startup and management overhead. For startup, using multithreading is better because it simply calls to create a new execution path in the current process. In terms of management overhead, since multithreading shares memory, threads have zero overhead for data transfer since they can communicate by modifying a global variable or shared object. 

5. Which method is better for CPU-bound tasks and which for I/O-bound tasks?
   For CPU-bound tasks, multiprocessing is significantly faster as each core works simultaneously. Multithreading is equal to or slower than running a single thread, but the overhead of having to switch between threads can increase the total execution time versus a sequential loop. For I/O-bound tasks, multithreading is faster and lightweight as while one thread is "sleeping"  (waiting for a response), the next thread immediately starts its work. Multiprocessing can be slower as it requires each new process to create a new interpreter and allocate separate memory, which can lead to a slower total time of execution. For short I/O tasks, the time taken for this startup can be longer than the task itself.

6. How did your group apply creative coding or algorithmic solutions in this lab?
   Our group applied data chunking by using math.ceil(len/num), which efficiently balances load across the cores. We applied locking through with pting_lock: which keeps the console output readable and organized. We also applied queueing through q.put()/q.get() which manages data flow between isolated environments. Lastly, we even implemented error handling by adding try except blocks in our code to prevent single thread failures from crashing the app. 