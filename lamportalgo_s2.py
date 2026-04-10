#LAMPORT ALGORITHM STEP-2 BINDIYA SUDARSUN 22MIC0040
import simpy

class Process:
    def __init__(self, env, pid, processes):
        self.env = env
        self.pid = pid
        self.clock = 0 #each process has a logical clock
        self.processes = processes

    def send_request(self):
        self.clock += 1 #incremented before msg is sent
        print(f"{self.env.now}: P{self.pid} sends REQUEST at time {self.clock}")

        for p in self.processes: #processes send request to all other processes with timestamp
            if p.pid != self.pid:
                self.env.process(p.receive_request(self.pid, self.clock))

    def receive_request(self, sender_pid, timestamp):
        yield self.env.timeout(1)

        self.clock = max(self.clock, timestamp) + 1 #on receiving, clock is updated
        print(f"{self.env.now}: P{self.pid} received REQUEST from P{sender_pid} | clock={self.clock}")

    def run(self):
        yield self.env.timeout(1)

        self.send_request()

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