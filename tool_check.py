import tools.general_data_collect_and_execution import ssh_into_devices  


if __name__ == "__main__":
    search='{"query":"what is he name of the capital of rome"}'
    test=ssh_into_devices.query()
    print(test.query(search))
