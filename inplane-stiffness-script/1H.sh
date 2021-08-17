#!/bin/bash
#
#PBS -l walltime=3:30:00
#PBS -q short
#PBS -l nodes=1:ppn=20
#PBS -N q40-1H
#PBS -e tests.err
#PBS -A cst
#

echo "n=$nodes"
echo "p=$ppn"
nproc=$((n * p))
cd $PBS_O_WORKDIR
mpirun -np $nproc /home/tug11655/bin/vasp-y
