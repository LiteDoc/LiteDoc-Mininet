import matplotlib.pyplot as plt
import numpy as np

latencies2 = [0, 0.1, 1, 10, 100]
latencies = ["0", "0.1", "1", "10", "100"]
algorithm = ["Cass-One-Server", "Cass-ABD-OPT", "Etcd-Raft"]


def get_average(some_list):
    return round(sum(some_list) / len(some_list), 2)


def get_one_file(algo, lat):
    file_path = f'{algo}/{lat}ms'
    tho_list, r_lat_list, w_lat_list = [], [], []
    with open(file_path) as f:
        for line in f.readlines():
            if "[OVERALL], Throughput(ops/sec)," in line:
                tho_list.append(float(line.split()[-1]))
            if "[READ], AverageLatency(us), " in line:
                r_lat_list.append(float(line.split()[-1]))
            if "[WRITE], AverageLatency(us), " in line:
                w_lat_list.append(float(line.split()[-1]))
    # print(tho_list, get_average(tho_list))
    # print(r_lat_list, get_average(r_lat_list))
    # print(w_lat_list, get_average(w_lat_list))
    return (get_average(tho_list),
            round(get_average(r_lat_list) / 1000, 2),
            round(get_average(w_lat_list) / 1000, 2))


def plotting_t():
    plt.figure(figsize=(5.2, 5.2))
    ax = plt.axes()
    ax.grid(color='gray', which="major", axis="both", linestyle='--', linewidth=0.3)
    for algo in algorithm:
        t_list, r_list, w_list = [], [], []
        for lat in latencies2:
            t, r, w = get_one_file(algo, lat)
            t_list.append(t)
            r_list.append(r)
            w_list.append(w)
        ax.plot(np.arange(5), t_list, marker='o', label=algo)

    plt.xlim(0, 4.5)
    ax.set_xlabel("Additional RTT Latency (ms)")
    ax.xaxis.set_ticks(np.arange(5))
    ax.xaxis.set_ticklabels(latencies2)
    plt.ylim(0, 65000)
    ax.legend(loc='upper right', fontsize='small', framealpha=0.5)
    ax.set_ylabel("Throughput (ops/sec)")

    ax.set_title(f"Throughput vs. Additional RTT")
    plt.tight_layout()
    plt.minorticks_on()
    # plt.show()
    plt.savefig("tho.png")


def plotting_r():
    plt.figure(figsize=(5.2, 5.2))
    ax = plt.axes()
    ax.grid(color='gray', which="major", axis="both", linestyle='--', linewidth=0.3)
    for algo in algorithm:
        t_list, r_list, w_list = [], [], []
        for lat in latencies2:
            t, r, w = get_one_file(algo, lat)
            t_list.append(t)
            r_list.append(r)
            w_list.append(w)
        ax.plot(np.arange(5), r_list, marker='o', label=algo)

    plt.xlim(0, 4.5)
    ax.set_xlabel("Additional RTT (ms)")
    ax.xaxis.set_ticks(np.arange(5))
    ax.xaxis.set_ticklabels(latencies2)

    plt.ylim(0, 140)
    plt.yscale("symlog")
    ax.yaxis.set_ticks([0, 1, 2, 4, 10, 100])
    ax.yaxis.set_ticklabels([0, 1, 2, 4, 10, 100])

    ax.legend(loc='upper left', fontsize='small', framealpha=0.5)
    ax.set_ylabel("Average Read Latency (ms)")

    ax.set_title(f"Average Read Latency vs. Additional RTT")
    plt.tight_layout()
    plt.minorticks_on()
    # plt.show()
    plt.savefig("rlat.png")


def plotting_w():
    plt.figure(figsize=(5.2, 5.2))
    ax = plt.axes()
    ax.grid(color='gray', which="major", axis="both", linestyle='--', linewidth=0.3)
    for algo in algorithm:
        t_list, r_list, w_list = [], [], []
        for lat in latencies2:
            t, r, w = get_one_file(algo, lat)
            t_list.append(t)
            r_list.append(r)
            w_list.append(w)
        ax.plot(np.arange(5), w_list, marker='o', label=algo)

    plt.xlim(0, 4.5)
    ax.set_xlabel("Additional RTT (ms)")
    ax.xaxis.set_ticks(np.arange(5))
    ax.xaxis.set_ticklabels(latencies2)

    plt.ylim(0, 140)
    plt.yscale("symlog")
    ax.yaxis.set_ticks([0, 1, 2, 4, 10, 100])
    ax.yaxis.set_ticklabels([0, 1, 2, 4, 10, 100])

    ax.legend(loc='upper left', fontsize='small', framealpha=0.5)
    ax.set_ylabel("Average Write Latency (ms)")

    ax.set_title(f"Average Write Latency vs. Additional RTT")
    plt.tight_layout()
    plt.minorticks_on()
    # plt.show()
    plt.savefig("wlat.png")


def print_table():
    for lat in latencies2[:3]:
        print("\t\t", lat, end="\t")
    print()
    for algo in algorithm:
        print(algo, end="\t")
        t_list, r_list, w_list = [], [], []
        for lat in latencies2[:3]:
            t, r, w = get_one_file(algo, lat)
            t_list.append(t)
            r_list.append(r)
            w_list.append(w)
        print(*w_list, sep="\t\t")

if __name__ == '__main__':
    print_table()
    # plotting_t()
    # plotting_r()
    # plotting_w()
