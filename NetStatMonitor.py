import subprocess
import os
import psutil

def get_processes():
    """ Get all processes and their PIDs """
    processes = {}
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        processes[proc.info['pid']] = proc.info['name']
    return processes

def get_netstat_snapshot():
    """ Get a snapshot of netstat -ano """
    netstat_output = subprocess.check_output(['netstat', '-ano'], text=True)
    return netstat_output

def parse_netstat_output(netstat_output):
    """ Parse netstat -ano output """
    connections = []
    for line in netstat_output.splitlines()[4:]:  # Skipping headers
        parts = line.split()
        if len(parts) < 5:
            continue  # Malformed line
        protocol, local_address, foreign_address, state, pid = parts[0], parts[1], parts[2], parts[3], parts[4]
        connections.append({
            'protocol': protocol,
            'local_address': local_address,
            'foreign_address': foreign_address,
            'state': state,
            'pid': int(pid)
        })
    return connections

def main():
    # Get all processes and their PIDs
    processes = get_processes()
    
    # Get a snapshot of netstat -ano
    netstat_output = get_netstat_snapshot()
    
    # Parse the netstat output
    connections = parse_netstat_output(netstat_output)
    
    # Compare PIDs from netstat to the list of running processes
    with open('log.txt', 'a') as f:  # Open log file in append mode
        for conn in connections:
            pid = conn['pid']
            if pid in processes:
                process_name = processes[pid]
            else:
                process_name = 'Unknown'
            string = (f"Protocol: {conn['protocol']}   |   Local Address: {conn['local_address']}   |   "
                      f"Foreign Address: {conn['foreign_address']}   |   State: {conn['state']}   |   "
                      f"PID: {pid}   |   Process: {process_name}")
            print(string)
            f.write(f"{string}\n")  # Write log entry to file

if __name__ == '__main__':
    main()
