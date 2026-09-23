#!/bin/bash
#SBATCH --job-name=spinning_cube_basalt
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --gres=gpu:1
#SBATCH --time=20:00:00
#SBATCH --output=%x_%j.out   # Separates Log pro Job-Ausführung
#SBATCH --error=%x_%j.err    # Separates Error-Log pro Job-Ausführung




echo $HOSTNAME >> output.txt
echo "Switching to $SLURM_SUBMIT_DIR"
cd $SLURM_SUBMIT_DIR

nvidia-smi >> output.txt
 

# before running spheres_ini 
#source ~/.bashrc
echo "Loading modules"
echo "cuda"
module load devel/cuda/12.6 
echo "hdf5"
module load lib/hdf5/1.12-gnu-11.4 

# run the code

../build/miluphcuda -A -f data/particles.0000 -g -H -I rk2_adaptive -m materials/material.cfg -n 300 -M 1e-5 -t 0.033
