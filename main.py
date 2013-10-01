#!/usr/bin/python
'''
Created on May 22, 2013

@author: jqian
'''
import os
import sys, getopt
import Rauto
import PathJF
import time
def getio(argv):
    baselinefolder =''
    newfolder = ''
    testresultfolder = ''
    if argv == None or len(argv) == 0:
        print 'main.py -b <baseline run folder> -n <new run folder> -o <test result folder>'
        sys.exit(1)
    try:
        opts, args = getopt.getopt(argv,"hb:n:o:",["baselinefolder=","newfolder=","testresultfolder="])
    except getopt.GetoptError:
        print 'main.py -b <baseline run folder> -n <new run folder> -o <test result folder>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'main.py -b <baseline run folder> -n <new run folder) -o <test result folder>'
            sys.exit(3)
        if opt in ("-b", "--baselinefolder"):
            baselinefolder = arg
        if opt in ("-n", "--newfolder"):
            newfolder = arg
        if opt in ("-o", "--testresultfolder"):
            testresultfolder = PathJF.namebytime(arg)
    if not os.path.isdir(testresultfolder):
        try:
            os.makedirs(testresultfolder)
        except OSError:
            print "can't make the test result folder"
            sys.exit(4)
    if os.path.exists(baselinefolder) and os.path.exists(newfolder):
        print 'baseline run folder is ', baselinefolder
        print 'new run folder is ', newfolder
        print 'test result folder is ', testresultfolder
        return [baselinefolder,newfolder,testresultfolder]
    else:
        print 'can not find the input baseline folder or new run folder!'
        print 'Usage: main.py -b <baseline run folder> -n <new run folder>'
        sys.exit(5)
if __name__ == "__main__":
    #bpath='C:\\Users\\jqian\\Documents\\My Box Files\\RNA-SEQ\\Data\\2013-07-21_235954'
    #npath='C:\\Users\\jqian\\Documents\\My Box Files\\RNA-SEQ\\Data\\2013-07-29_134220'
    #opath='C:\\Users\\jqian\\Documents\\My Box Files\\RNA-SEQ\\Data\\output'
    [baselinefolder,newfolder,testresultfolder]=getio(sys.argv[1:]) # get the input folder, -b is the baseline folder, and -n is the new test run folder
    #[baselinefolder,newfolder,testresultfolder]=[bpath,npath,opath]
    logfile=os.path.join(testresultfolder,'log.txt')
    resultfile=os.path.join(testresultfolder,'result.txt')
    fl=open(logfile,'a') # this is the log file
    fr=open(resultfile, 'a') # this is the result file
    saveout=sys.stdout # save the console output to tempary file
    sys.stdout = fl # all the output on the screen is redirect to the log
    starttime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    print "Start RNA-SEQ baseline comparision checking, ", "Current time: ", starttime
    [errornum, errormsg,testcaseid]=Rauto.Summary(baselinefolder,newfolder).compare()
    print "The number of error is", errornum, ", errormsg is ", errormsg, ", these testcases are tested:", testcaseid
    print >>fr, "Summary error:", errornum,'\n\r'
    [errornum, errormsg,testcaseid]=Rauto.ReadFiltering(baselinefolder,newfolder).compare()
    print "The number of error is", errornum, ", errormsg is ", errormsg, ", these testcases are tested:", testcaseid
    print >>fr, "ReadFiltering error:", errornum,'\n\r'
    print Rauto.Alignment(baselinefolder,newfolder).compare()
    [errornum, errormsg,testcaseid]=Rauto.Alignment(baselinefolder,newfolder).compare()
    print "The number of error is", errornum, ", errormsg is ", errormsg, ", these testcases are tested:", testcaseid
    print >>fr, "Alignment error:", errornum,'\n\r'
    [errornum, errormsg,testcaseid]=Rauto.Fusioncalling(baselinefolder,newfolder).compare()
    print "The number of error is", errornum, ", errormsg is ", errormsg, ", these testcases are tested:", testcaseid
    print >>fr, "Fusioncalling error:", errornum,'\n\r'
    print "enter-1" 
    [errornum, errormsg,testcaseid]=Rauto.Variantcalling(baselinefolder,newfolder).compare()
    print "The number of error is", errornum, ", errormsg is ", errormsg, ", these testcases are tested:", testcaseid
    print >>fr, "Variantcalling error:", errornum,'\n\r'
    [errornum, errormsg,testcaseid]=Rauto.DiffExp(baselinefolder,newfolder).compare()
    print "The number of error is", errornum, ", errormsg is ", errormsg, ", these testcases are tested:", testcaseid
    print >>fr, "Differential Expression error:", errornum,'\n\r'
    [errornum, errormsg,testcaseid]=Rauto.Novel(baselinefolder,newfolder).compare()
    print "The number of error is", errornum, ", errormsg is ", errormsg, ", these testcases are tested:", testcaseid
    print >>fr, "Novel assemblies error:", errornum,'\n\r'
    #print "enter0" 
    endtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    #print "enter1"
    #t1=PathJF.Timeformat(starttime)
    #t2=PathJF.Timeformat(endtime)
    #d = t1.check_diff_time(t1.time_string, t2.time_string) # this is the time cost
    print "Finish RNA-SEQ baseline comparision checking, ", "Current time: ", endtime
    #print "Total time Cost: :%syear%smonth%sday%shour%sminute%ssecond" %(d["year"], d["month"], d["day"], d["hour"], d["min"], d["sec"]) 
    fr.close()
    fl.close()
    sys.sdout=saveout
