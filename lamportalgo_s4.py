#LAMPORT ALGORITHM STEP-4 BINDIYA SUDARSUN 22MIC0040
import simpy

class Process:
    def __init__(self, env, pid, processes):
        self.env = env
        self.pid = pid
        self.clock = 0 
        self.processes = processes
        self.replies = 0  
        self.requesting = False
        self.request_queue = [] #process maintains a queue of all requests(maintains ordering)

    def send_request(self):
        self.clock += 1
        self.requesting = True
        self.replies = 0

        self.request_queue.append((self.clock, self.pid)) #request is added to queue

        print(f"{self.env.now}: P{self.pid} sends REQUEST at time {self.clock}")

        for p in self.processes:
            if p.pid != self.pid:
                self.env.process(p.receive_request(self.pid, self.clock))

    def receive_request(self, sender_pid, timestamp):
        yield self.env.timeout(1)

        self.clock = max(self.clock, timestamp) + 1

        self.request_queue.append((timestamp, sender_pid)) #sender request is added to queue
        self.request_queue.sort()

        print(f"{self.env.now}: P{self.pid} received REQUEST from P{sender_pid} | clock={self.clock}")

        sender = self.processes[sender_pid]
        self.env.process(sender.receive_reply(self.pid))

    def receive_reply(self, sender_pid): 
        yield self.env.timeout(1)

        self.clock += 1
        self.replies += 1

        print(f"{self.env.now}: P{self.pid} received REPLY from P{sender_pid}") 

    def run(self):
        yield self.env.timeout(1)

        self.send_request()

        while True:
            yield self.env.timeout(1)

            if (self.replies == len(self.processes) - 1 and
                self.request_queue[0][1] == self.pid):

                print(f"{self.env.now}: P{self.pid} ENTERS CS") #process enters only if toq and all replies are received
                yield self.env.timeout(2)

                self.release()
                break

    def release(self):
        self.clock += 1

        print(f"{self.env.now}: P{self.pid} RELEASES CS")
        #After exe, process sends RELEASE message, processes remove that request from their queue
        self.request_queue = [req for req in self.request_queue if req[1] != self.pid]

        for p in self.processes:
            if p.pid != self.pid:
                self.env.process(p.receive_release(self.pid))

    def receive_release(self, sender_pid):
        yield self.env.timeout(1)

        #sender request is removed
        self.request_queue = [req for req in self.request_queue if req[1] != sender_pid]

        print(f"{self.env.now}: P{self.pid} updated queue after RELEASE from P{sender_pid}")

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