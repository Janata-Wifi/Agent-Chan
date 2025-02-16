import tools.general_data_collect_and_execution
   


if __name__ == "__main__":
    data={"hostname":"172.16.0.100", "command":"ip address print", "device_type":"mikrotik_routeros"}
    #print(tools.general_data_collect_and_execution.read_data_from_any_device(data))
    #print(tools.general_data_collect_and_execution.traceroute("1.1.1.1"))""
    print(tools.general_data_collect_and_execution.read_data_from_any_device({"hostname":"172.16.0.100", "command":"ip address print", "device_type":"mikrotik_routeros"}))

