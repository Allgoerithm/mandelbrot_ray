import ray
import time


@ray.remote
def do_some_work(x):
    time.sleep(1)  # Replace this is with work you need to do.
    return x


ray.init(num_cpus=4)  # Specify this system has 4 CPUs.
start = time.time()
results = ray.get([do_some_work.remote(x) for x in range(4)])
print("duration =", time.time() - start)
print("results = ", results)