#!/bin/bash
#SBATCH -A p31502               # Allocation
#SBATCH -p short                # Queue
#SBATCH -t 24:00:00             # Walltime/duration of the job
#SBATCH -N 1                    # Number of Nodes
#SBATCH --mem=18G               # Memory per node in GB needed for a job. Also see --mem-per-cpu
#SBATCH --ntasks-per-node=6     # Number of Cores (Processors)
#SBATCH --mail-user=arayavalani@u.northwestern.edu  # Designate email address for job communications
#SBATCH --mail-type=BEGIN,END,NONE,FAIL,REQUEUE     # Events options are job BEGIN, END, NONE, FAIL, REQUEUE
#SBATCH --output=/home/ara5933    # Path for output must already exist
#SBATCH --error=/home/ara5933    # Path for errors must already exist
#SBATCH --job-name="twitter_firehose"       # Name of job

export MODULEPATH='/software/Modules/3.2.9/modulefiles:/software/Modules/spack-modules/linux-rhel7-x86_64'

function module ()
{
    eval '/usr/bin/modulecmd bash $*'
}

# unload any modules that carried over from your command line session
module purge

# load modules you need to use
module load python/anaconda3.6
# activate environment
source /software/anaconda3.6/bin/activate /projects/p31502/projects/twitter_corpus/twitter_env

# runs stream, should be killed every 24 hrs
python3 /projects/p31502/projects/twitter_corpus/stream.py
