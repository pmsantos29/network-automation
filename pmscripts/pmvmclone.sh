#!/bin/bash

snaptx=$3

function usage () {
    echo
    echo "  - create virtual machines"
    echo "    ./pmvectl.sh create {template-id} {first-clone-id} {last-clone-id}"
    echo "  - destroy virtual machines"
    echo "    ./pmvectl.sh destroy {first-vm-id} {last-vm-id}"
    echo "  - start virtual machines"
    echo "    ./pmvectl.sh start {first-vm-id} {last-vm-id}"
    echo "  - stop virtual machines"
    echo "    ./pmvectl.sh stop {first-vm-id} {last-vm-id}"
    echo "  - rollback virtual machines"
    echo "    ./pmvectl.sh rollback {first-vm-id} {last-vm-id}"
    echo "  - get IP addresses of virtual machines"
    echo "    ./pmvectl.sh get-ip {first-vm-id} {last-vm-id}"
    echo 
}

case $1 in
    create)
        echo
        echo -n "Creating virtual machines:"
        for i in $(seq $3 $4); do
            hostname=$(grep -w ${i} pmvmhosts.txt | cut -d ' ' -f 2)
            qm clone $2 ${i} --name ${hostname} --full > /dev/null
            echo -n "."

            # Set memory
            qm set ${i} --memory 4096

            # Set CPUs
            qm set ${i} --sockets 1 --cores 2 --cpu cputype=kvm64

            # Set disk size
            qm resize ${i} scsi0 32G

            # Enable QEMU Guest Agent
            qm set ${i} --agent enabled=1

            # Set networking
            qm set ${i} --net0 virtio,bridge=vmbr0,firewall=1
        done
        echo " done."

        echo -n "Snapshotting virtual machines:"
        for i in $(seq $3 $4); do
            qm snapshot ${i} snap01 --description "Initial snapshot."
            echo -n "."
        done
        echo " done."
        ;;
    destroy)
        echo
        echo -n "Destroying virtual machines:"
        for i in $(seq $2 $3); do
            qm destroy ${i} > /dev/null
            echo -n "."
        done
        echo " done."
        ;;
    start)
        echo
        echo -n "Starting virtual machines:"
        for i in $(seq $2 $3); do
            qm start ${i}
            echo -n "."
        done
        echo " done."
        ;;
    stop)
        echo
        echo -n "Stopping virtual machines:"
        for i in $(seq $2 $3); do
            qm stop ${i}
            echo -n "."
        done
        echo " done."
        ;;
    rollback)
        echo
        echo -n "Rolling back virtual machines:"
        for i in $(seq $2 $3); do
            qm rollback ${i} snap01 > /dev/null
            echo -n "."
        done
        echo " done."
        ;;
    get-ip)
        echo
        echo -n "Getting IP addresses:"
        for i in $(seq $2 $3); do
            hostname=$(qm config ${i} | grep -i name | awk -F ": " '{print $2}')
            ip=$(qm guest exec ${i} -- ip -4 addr show ens18 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
            echo "${i} ${hostname} ${ip}" >> pmvmips.txt
            echo -n "."
        done
        echo " done. IP addresses saved to pmvmips.txt."
        ;;
    *)
        usage
        ;;
esac