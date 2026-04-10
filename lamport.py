#LAMPORT ALGORITHM final BINDIYA SUDARSUN 22MIC0040
import simpy
import random

class Process:
    def __init__(self, env, pid, processes, log):
        self.env = env
        self.pid = pid
        self.clock = 0
        self.processes = processes
        self.log = log

        self.request_queue = []
        self.replies = 0
        self.requesting = False

    def send_request(self):
        self.clock += 1
        self.requesting = True
        self.replies = 0

        self.request_queue.append((self.clock, self.pid))
        self.request_queue.sort()

        self.log(f"{self.env.now}: P{self.pid} sends REQUEST at time {self.clock}")

        for p in self.processes:
            if p.pid != self.pid:
                self.env.process(p.receive_request(self.pid, self.clock))

    def receive_request(self, sender_pid, timestamp):
        yield self.env.timeout(random.randint(1, 2))

        self.clock = max(self.clock, timestamp) + 1
        self.request_queue.append((timestamp, sender_pid))
        self.request_queue.sort()

        self.log(f"{self.env.now}: P{self.pid} received REQUEST from P{sender_pid} | clock={self.clock}")

        sender = self.processes[sender_pid]
        self.env.process(sender.receive_reply(self.pid))

    def receive_reply(self, sender_pid):
        yield self.env.timeout(random.randint(1, 2))

        self.clock += 1
        self.replies += 1

        self.log(f"{self.env.now}: P{self.pid} received REPLY from P{sender_pid}")

    def release(self):
        self.clock += 1

        self.log(f"{self.env.now}: P{self.pid} RELEASES CS")

        self.request_queue = [req for req in self.request_queue if req[1] != self.pid]

        for p in self.processes:
            if p.pid != self.pid:
                self.env.process(p.receive_release(self.pid))

    def receive_release(self, sender_pid):
        yield self.env.timeout(1)

        self.request_queue = [req for req in self.request_queue if req[1] != sender_pid]

        self.log(f"{self.env.now}: P{self.pid} updated queue after RELEASE from P{sender_pid}")

    def run(self):
        yield self.env.timeout(random.randint(1, 3))

        self.send_request()

        while True:
            yield self.env.timeout(1)

            if (self.replies == len(self.processes) - 1 and
                self.request_queue[0][1] == self.pid):

                self.log(f"{self.env.now}: P{self.pid} ENTERS CS")

                yield self.env.timeout(2)

                self.release()
                break