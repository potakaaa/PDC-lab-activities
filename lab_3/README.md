# PDC-task-and-data-parallelism
1. Differentiate Task and Data Parallelism. Identify which part of the lab demonstrates each and justify the workload division.
   Task parallelism is explicitly demonstrated in the parallel_compute function of the lab. In this section, the workload is divided by functionality, where a single data point, the employee's salary in this case, is processed by four distinct functions: compute_sss, compute_philhealth, compute_pagibig, and compute_tax. This division is justified because each deduction is a logically independent "task." Since the calculation for health insurance does not depend on the result of the income tax calculation, they can be executed concurrently using a ThreadPoolExecutor. Data parallelism, on the other hand, is showcased in the process_payroll_batch function. Here, the workload is divided by data partitioning rather than by the type of task performed. The system applies the exact same payroll logic, encapsulated in the calculate_employee_payroll function, to a collection of different data elements simultaneously. This division is justified by the need to handle high volumes of data efficiently. By utilizing a ProcessPoolExecutor, the program can distribute individual employee records across multiple CPU cores, allowing the system to process a large batch of payroll entries in parallel, which is significantly faster than processing each employee one after another.

2. Explain how concurrent.futures managed execution, including submit(), map(), and Future objects. Discuss the purpose of with when creating an Executor.
   Concurrent.futures is a module that manages execution primarily through its Executor classes, which are best utilized within a “with” statement to act as a context manager, that ensures the Executor shuts down properly by automatically calling “shutdown(wait=True)”, which means that the program won’t progress until all threads and processes in the pool have finished their work, which prevents resource leaks. Submit() schedules a single callable to be executed and then returns a “Future” object. Future objects are essentially promises of a result, representing an asynchronous operation that hasn’t finished yet. You then use “.result()” to block execution until the value is ready. Lastly, “map()” applies a function to an iterable of data. It’s best for task parallelism where tasks are unique.

3. Analyze ThreadPoolExecutor execution in relation to the GIL and CPU cores. Did true parallelism occur?
   ThreadPoolExecutor actually didn’t show true parallelism. Because of Python’s GIL, only one thread can execute code. ThreadPoolExecutor actually provides concurrency, which is great for I/O-bound tasks, but for CPU-bound math like tax deductions, the threads actually take turns on a single CPU core.

4. Explain why ProcessPoolExecutor enables true parallelism, including memory
   space separation and GIL behavior.
5. Evaluate scalability if the system increases from 5 to 10,000 employees. Which
   approach scales better and why?
6. Provide a real-world payroll system example. Indicate where Task Parallelism and
   Data Parallelism would be applied, and which executor you would use.
