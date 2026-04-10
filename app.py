#LAMPORT ALGORITHM STREAMLIT APPLICATION - BINDIYA SUDARSUN 22MIC0040
import streamlit as st
import simpy
from lamport import Process

def simulate(n):
    env = simpy.Environment()
    logs = []

    def log(msg):
        logs.append(msg)

    processes = []

    for i in range(n):
        p = Process(env, i, [], log)
        processes.append(p)

    for p in processes:
        p.processes = processes

    for p in processes:
        env.process(p.run())

    env.run()

    return logs


# UI
st.title("Lamport Distributed Mutual Exclusion Algorithm")

st.write("Simulating mutual exclusion using Lamport timestamps")

n = st.slider("Number of Processes", 2, 10, 2)

if st.button("Run Simulation"):
    logs = simulate(n)

    st.subheader("Simulation Output")
    st.text_area("Logs", "\n".join(logs), height=400)