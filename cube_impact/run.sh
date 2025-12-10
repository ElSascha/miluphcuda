#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --mem-per-cpu=64gb
#SBATCH --job-name=cube_impact_no_correction
#SBATCH --partition=gpu
## use the a100 or the a30 or the h200
#SBATCH --gres=gpu:h200:1


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

nice -15 ../build/bin/miluphcuda -v -A -f particles.0000 -g -H -I rk2_adaptive -m material.cfg -n 100 -M 0.01 -t 0.01 >> output.txt 2> error.txt