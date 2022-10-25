# Pipe-Based multi-pool processing

Framework to make handling multiple intertwined large tasks easier. 

### img headline
![alt text](imgs/Concept_unfinished.png)

### Performance

There are several demos located in the demos directory also here's a table for single tasks that do not interfere with
each other, note that this isn't the keypoint of this implementation:

| Algorithm                           | easy_multiprocessing: listmode              | easy_multiprocessing: dictmode | multiprocessing.pool().map                 | single thread |
|:------------------------------------|:--------------------------------------------|:-------------------------------|:-------------------------------------------|:--------------|
| time - prime calculator n = 200_000 | 10.34s                                      | 10.43s                         | <span style="color:red">**10.13s** </span> | 56.14s        |
| relative speed of fastest test      | 97.9%                                       | 97.1%                          | <span style="color:red">**100%**   </span> | 18.0%         |
| time - big factorials n = 50_000    | <span style="color:red">**90.6s**  </span>  | 102.4s                         | 110.7s                                     | 576.64s       |
| relative speed of fastest test      | <span style="color:red">**100%**   </span>  | 92,5%                          | 81,8%                                      | 15,76%        |
|                                     |                                             |                                |                                            |               |

All times have been measured on an i5-12600k with 32GB of Memory and the managers and pool got 8 processes.
The concept of this implementation is not to split the whole dataset and let each process work, but to send data just-in-time
to remove the need of shared memory and the likes.
Additionally the Manager returns a somehow ordered dictionary containing the results. Each result gets mapped to the entered data/key.
I noticed this implementation to be more efficient, the longer the given task runs.
