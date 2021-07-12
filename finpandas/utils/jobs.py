"""
Utility for multiprocessing finpandas jobs
"""

from typing import Callable, Any, Iterable

from multiprocessing import Process, Pipe


def spawn(f:Callable) -> Callable:
    """
    [summary]

    Args:
        f (Callable): function to spawn a pipe for

    Returns:
        Callable: a function that executes the spawning of the pipe
    """
    def fun(pipe:Pipe, x:Iterable[Any]) -> None:
        pipe.send(f(x))
        pipe.close()
    return fun


def parmap(f:Callable, X:Iterable[Any]) -> Iterable[Any]:
    """
    parralelized mapping function

    Args:
        f (Callable): function to parallelize operation over
        X (Iterable): the arguments to the function, over N 
            function calls.

    Returns:
        Iterable: the N function outputs
    """
    pipe = [Pipe() for _ in X]
    proc = [Process(target=spawn(f), args=(c, x)) for x, (_, c) in zip(X, pipe)]
    [p.start() for p in proc]
    [p.join() for p in proc]
    return [p.recv() for (p, _) in pipe]


class Jobs:
    def __init__(self) -> None:
        self.jobs = []


    def add_job(self, f:Callable, *args) -> None:
        """
        add a job to be executed

        Args:
            f (Callable): the function to execute with the job,
                followed in-order by any arguments.
        """
        self.jobs.append((f, args))


    def execute(self) -> Iterable[Any]:
        """
        execute all jobs

        Returns:
            Iterable: the output of each job
        """
        def run(job):
            f, args = job
            return f(*args)

        return parmap(run, self.jobs)
