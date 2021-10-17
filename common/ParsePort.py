def ParsePort(ports):
    scanPorts =[]
    if ports == "":
        return []
    slices = ports.split(",")
    for port in slices:
        port = port.strip()
        upper = port
        if "-" in port:
            ranges = port.split("-")
            if len(ranges)<2 :
                continue
            startPort = int(ranges[0])
            endPort = int(ranges[1])
            if startPort < endPort:
                port=ranges[0]
                upper=ranges[1]
            else:
                port = ranges[1]
                upper = ranges[0]
        start = int(port)
        end = int(upper)
        for i in range(start,end+1):
            scanPorts.append(i)
    scanPorts = removeDuplicate(scanPorts)
    return scanPorts





def removeDuplicate(old):
    return list(set(old))

if __name__ == "__main__":
    ret=ParsePort("1-10,11,12,1")
    print(ret)