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
mpirun -np $nproc vasp-relax-only-ions #for inplane stiffness
#mpirun -np $nproc vasp-relax-along-y (if x is strained, keep z fixed for poisson's ratio)
