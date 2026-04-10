#LAMPORT ALGORITHM STEP-3 BINDIYA SUDARSUN 22MIC0040
import simpy

class Process:
    def __init__(self, env, pid, processes):
        self.env = env
        self.pid = pid
        self.clock = 0 
        self.processes = processes
        self.replies = 0  
        self.requesting = False

    def send_request(self):
        self.clock += 1
        self.requesting = True
        self.replies = 0

        print(f"{self.env.now}: P{self.pid} sends REQUEST at time {self.clock}")

        for p in self.processes:
            if p.pid != self.pid:
                self.env.process(p.receive_request(self.pid, self.clock))

    def receive_request(self, sender_pid, timestamp):
        yield self.env.timeout(1)

        self.clock = max(self.clock, timestamp) + 1
        print(f"{self.env.now}: P{self.pid} received REQUEST from P{sender_pid} | clock={self.clock}")
        #after receiving a request, the process sends a reply (can enter CS)

        sender = self.processes[sender_pid]
        self.env.process(sender.receive_reply(self.pid))

    def receive_reply(self, sender_pid): 
        yield self.env.timeout(1)

        self.clock += 1
        self.replies += 1

        print(f"{self.env.now}: P{self.pid} received REPLY from P{sender_pid}") 
        #Process waits until it receives replies from all other processes

    def run(self):
        yield self.env.timeout(1)

        self.send_request()

        while self.replies < len(self.processes) - 1:
            yield self.env.timeout(1)

        #once all replies are recieved, process enters CS
        print(f"{self.env.now}: P{self.pid} ENTERS CS")

def simulate():
    env = simpy.Environment()

    processes = []
    for i in range(3):
        p = Process(env, i, [])
        processes.append(p)

    for p in processes:
        p.processes = processes

    for p in processes:
        env.process(p.run())

    env.run()

if __name__ == "__main__":
    simulate()