#!/bin/bash
# Launch JupyterLab with SysML v2 kernel

# Set up environment
source ~/anaconda3/etc/profile.d/conda.sh
conda activate sysml

# Set Java 21 path
export JAVA_HOME=/Users/jmarwell/Desktop/Projects/drip/acoustic-sysml-v2/jdk-21.0.2.jdk/Contents/Home
export PATH=$JAVA_HOME/bin:$PATH

# Verify Java version
echo "Java version:"
java -version

# Launch JupyterLab
echo "Launching JupyterLab..."
jupyter lab