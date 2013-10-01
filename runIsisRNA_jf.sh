#!/bin/bash
## Author:  Josh Tietjen

# Enter the run folder path as the input parameter for the script ($1)
run=/bioinfoSD/ryankelley/IsisRNA/Runs/130320_M00836_0049_Aa2uf7-16plex

export cmd_dir=`echo $PWD`
echo $cmd_dir
export mono=/illumina/development/Isis/packages/bin/mono
export ISIS_DIR=/illumina/scripts/IsisRNA/latest
source ${ISIS_DIR}/UpdateEnvironment

export isis=${ISIS_DIR}/Isis/Isis.exe
export version=`$mono $isis grep |grep Isis|cut -f2 -d " "`
echo version $version

time=`date +%F_%T | sed -s "s/\://g"`

export out_dir="$cmd_dir/$time"
export cmd=`echo $mono $isis -r $run -a $out_dir`
echo $cmd
mkdir -pv $out_dir

# run the analysis command
echo $cmd

eval $cmd 2>&1 | tee $out_dir/log.txt
