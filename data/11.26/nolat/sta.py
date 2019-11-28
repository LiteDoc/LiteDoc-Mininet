import matplotlib.pyplot as plt
import numpy as np

latency_tag = "\n(~0ms RTT)"


def read_file_tho(f_name):
    with open(f_name) as f:
        threads = []
        threads_rw = []
        threads_r0 = []
        throughput = []

        for line in f.readlines():
            if 'Num readWrite Thread = ' in line:
                threads_rw.append(int(line.split()[-1]))
            elif 'Num readOnly Thread = ' in line:
                threads_r0.append(int(line.split()[-1]))
            elif '[OVERALL], Throughput(ops/sec), ' in line:
                throughput.append(float(line.split()[-1]))
        for i in range(len(threads_rw)):
            threads.append(threads_rw[i] + threads_r0[i])
        print(threads)
        print(throughput)
        return threads, throughput
        # return threads[1:], throughput[1:]


def read_file_r_lat(f_name):
    with open(f_name) as f:
        threads = []
        threads_rw = []
        threads_r0 = []
        throughput = []

        for line in f.readlines():
            if 'Num readWrite Thread = ' in line:
                threads_rw.append(int(line.split()[-1]))
            elif 'Num readOnly Thread = ' in line:
                threads_r0.append(int(line.split()[-1]))
            elif '[READ], AverageLatency(us), ' in line:
                throughput.append(round(float(line.split()[-1]) / 1000, 2))
        for i in range(len(threads_rw)):
            threads.append(threads_rw[i] + threads_r0[i])
        print(threads)
        print(throughput)
        return threads, throughput
        # return threads[1:], throughput[1:]


def read_file_w_lat(f_name):
    with open(f_name) as f:
        threads = []
        threads_rw = []
        threads_r0 = []
        throughput = []

        for line in f.readlines():
            if 'Num readWrite Thread = ' in line:
                threads_rw.append(int(line.split()[-1]))
            elif 'Num readOnly Thread = ' in line:
                threads_r0.append(int(line.split()[-1]))
            elif '[WRITE], AverageLatency(us), ' in line:
                throughput.append(round(float(line.split()[-1]) / 1000, 2))
        for i in range(len(threads_rw)):
            threads.append(threads_rw[i] + threads_r0[i])
        print(threads)
        print(throughput)

        return threads, throughput
        # return threads[1:], throughput[1:]


def tho_figure():
    plt.figure(figsize=(4.5, 4.5))

    ax = plt.axes()
    ax.grid(color='gray', which="major", axis="both", linestyle='--', linewidth=0.3)
    ax.plot(*read_file_tho('cassOne'), marker='o', label='Cass-One-Server')
    ax.plot(*read_file_tho('abdOpt'), marker='o', label='Cass-ABD-OPT')
    ax.plot(*read_file_tho('raft'), marker='o', label='Etcd')
    ax.set_ylabel("Throughput (ops/sec)")
    ax.set_xlabel("Num of Clients")
    ax.xaxis.set_ticks([10, 20, 30, 40, 50, 60])
    plt.xlim(10, 55)
    ax.yaxis.set_ticks(np.arange(0, 70000, 10000))
    ax.set_title(f"Throughput vs. Num of Clients {latency_tag}")
    ax.legend(loc='upper left', fontsize='small', framealpha=0.2)
    # plt.show()
    plt.tight_layout()
    plt.savefig("tho.png")


def r_lat_figure():
    plt.figure(figsize=(4.5, 4.5))

    ax = plt.axes()
    ax.grid(color='gray', which="major", axis="both", linestyle='--', linewidth=0.3)
    ax.plot(*read_file_r_lat('cassOne'), marker='o', label='Cass-One-Server')
    ax.plot(*read_file_r_lat('abdOpt'), marker='o', label='Cass-ABD-OPT')
    ax.plot(*read_file_r_lat('raft'), marker='o', label='Etcd')
    ax.set_ylabel("Average Read Latency (ms)")
    ax.set_xlabel("Num of Clients")
    ax.xaxis.set_ticks([10, 20, 30, 40, 50, 60])
    plt.xlim(10, 55)
    ax.yaxis.set_ticks(np.arange(0, 5.5, 0.5))
    ax.set_title(f"Average Read Latency vs. Num of Clients {latency_tag}")
    ax.legend(loc='upper left', fontsize='small', framealpha=0.2)
    # plt.show()
    plt.tight_layout()
    plt.savefig("rlat.png")


def w_lat_figure():
    plt.figure(figsize=(4.5, 4.5))
    ax = plt.axes()
    ax.grid(color='gray', which="major", axis="both", linestyle='--', linewidth=0.3)
    ax.plot(*read_file_w_lat('cassOne'), marker='o', label='Cass-One-Server')
    ax.plot(*read_file_w_lat('abdOpt'), marker='o', label='Cass-ABD-OPT')
    ax.plot(*read_file_w_lat('raft'), marker='o', label='Etcd')
    ax.set_ylabel("Average Write Latency (ms)")
    ax.set_xlabel("Num of Clients")
    ax.xaxis.set_ticks([10, 20, 30, 40, 50, 60])
    plt.xlim(10, 55)
    ax.yaxis.set_ticks(np.arange(0, 5.5, 0.5))
    ax.set_title(f"Average Write Latency vs. Num of Clients {latency_tag}")
    ax.legend(loc='upper left', fontsize='small', framealpha=0.2)
    # plt.show()
    plt.tight_layout()
    plt.savefig("wlat.png")


if __name__ == '__main__':
    tho_figure()
    r_lat_figure()
    w_lat_figure()
