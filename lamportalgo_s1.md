# LAMPORT ALGORITHM STEP-1 BINDIYA SUDARSUN 22MIC0040
import simpy

class Process: #approximately equal to an independent node in the distributed system

    def __init__(self, env, pid): #Each process has a unique ID and runs its own execution logic
        self.env = env
        self.pid = pid

    def run(self): #defines the lifecycle of a process- start,wait,or complete exec
        print(f"Process {self.pid} started at time {self.env.now}") 
        yield self.env.timeout(2) #simulates delay in execution
        print(f"Process {self.pid} finished at time {self.env.now}")

def simulate(): #runner function- creates the simulation environment
    env = simpy.Environment()

    processes = []
    for i in range(3):
        p = Process(env, i)
        processes.append(p)
        env.process(p.run()) #processes can run concurrently

    env.run() #process start execution

if __name__ == "__main__":
    simulate()
