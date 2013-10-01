#!/usr/bin/python
'''
Created on May 22, 2013
This is the compare if two metrics.csv file from baseline folder and run folder. 
When the content is a string, check if the two strings are the same.
When the content is a number, check if the two number are in **% similarity. 
@author: jqian
'''
import tempfile
import os
import sys
def ClassifyMetrics(fullfilename):
    #filename=fullfilename.lower()
    filename=fullfilename
    if filename.endswith('SampleSheetUsed.csv') :
        return 0 # needs to be exactly the same
    elif filename.endswith("correlations.csv"):
        return 1
    else:
        return 2
    #if filename.endswith ('\assembly\Metrics.csv') or filename.endswith ('cuffdiff\Metrics.csv') or re.search("ead\d_Metrics.csv$",filename) or filename.endswith('combined_Metrics.csv') or filename.endwith('QScoreData.csv') or  re.search("R\d_Metrics.csv$",filename)  or  re.search("R\d_QScoreData.csv$",filename) or filename.endwith('combined_PicardCoverage.csv') :
        #return 1 # two column, seconds should have tolerance if number existance
    
    
def CompMetricsCsv_2column(bfile, nfile, thresh):
    # to compare the baseline metrics.csv file with new run metrics.metrics file. If the content is strings, check if they are the same. If the content is the number, check if they are 95% similar.
    print "comparing file: "+bfile+" and "+nfile
    bf=open(bfile) # open the baseline file
    bdic={}
    for line in bf:
        linecon=line.split(',')
        if len(linecon)==2:# everyline of the csv file should have two element separate by ,
            bdic[linecon[0]]=linecon[1]
        else:
            return [1,'error during parsing the csv file '+bfile+' more then two elements in a line (separate by the comma)']
    ndic={}
    nf=open(nfile) # open the new run file
    for line in nf:
        linecon=line.split(',')
        if len(linecon)==2: # everyline of the csv file should have two element separate by ,
            ndic[linecon[0]]=linecon[1]
        else:
            return [1,'error during parsing the csv file '+bfile+' more then two elements in a line (separate by the comma)']
    if len(bdic) != len(ndic):
        return [1, 'baseline file '+bfile+' and new run file '+nfile+' has different number of lines']
    for k in bdic.keys():
        try:
            num1=float(bdic[k]) 
        except ValueError:
            num1=bdic[k]
        try:
            num2=float(ndic[k]) 
        except ValueError:
            num2=ndic[k]
        if (type(num1) is str) and (type(num2) is str) and num1==num2:
            return [0,'']
        elif (type(num1) is float) and (type(num2) is float):
            if num1==0:
                if num2==0:
                    return [0,'']
                else:
                    return [1,'baselinefile is 0 and newfile is not 0']
            else:
                diff=abs(num1-num2)/num1
                if diff >thresh:
                    return [1,'difference between the baselinefile and the newfile are more than threshhold']
    return [0, '']


def Compidx(bfile, nfile,thresh):
    print "comparing file: "+bfile+" and "+nfile
    errornum=0
    errormsg=''
    tempb =tempfile.mktemp()
    tempn =tempfile.mktemp()
    fb=open (tempb,'w')
    fn=open (tempn,'w')
    commandlineb="samtools idxstats "+bfile+" >>"+tempb
    commandlinen="samtools idxstats  "+nfile+" >>"+tempn
    e1=os.system(commandlineb)
    e2=os.system(commandlinen)
    if e1>0 or e2>0:
        errornum=1
        errormsg='unexpected error happens during running samtools idxstats'
        return [errornum, errormsg]
    fb.close()
    fn.close()
    [errornum, errormsg]=CompMetricsidxstat(tempb,tempn,thresh)
    return [errornum, errormsg]
    
    
    

def CompMetricsidxstat(bfile, nfile, thresh):
    # to compare the baseline idxstats output file, the variation range should be in the 5% difference.
    bf=open(bfile) # open the baseline file
    bdic1={}
    bdic2={}
    bdic3={}
    ndic1={}
    ndic2={}
    ndic3={}
    for line in bf:
        linecon=line.split()
        if len(linecon)==4:# everyline of the idxstats file should have three element separate by ,
            bdic1[linecon[0]]=linecon[1]
            bdic2[linecon[0]]=linecon[2]
            bdic3[linecon[0]]=linecon[3]
        else:
            return [1,'error during parsing the idxstats file generated from the bam file: '+bfile+' more or less then four elements in a line']
    ndic={}
    nf=open(nfile) # open the new run file
    for line in nf:
        linecon=line.split()
        if len(linecon)==4: # everyline of the idxstats file should have three element separate by ,
            ndic1[linecon[0]]=linecon[1]
            ndic2[linecon[0]]=linecon[2]
            ndic3[linecon[0]]=linecon[3]
        else:
            return [1,'error during parsing the idxstats file generated from the bam file: '+bfile+' more or less then four elements in a line']
    if len(bdic1) != len(ndic1) or len(bdic2) != len(ndic2) or len(bdic3) != len(ndic3):
        return [1, 'baseline file '+bfile+' and new run file '+nfile+' has different number of lines']
    listdicn=[ndic1,ndic2,ndic3] # all the dictionary generated from the new run folder
    listdicb=[bdic1,bdic2,bdic3] # all the dictionary generated from the baseline folder
    for i in range(3):
        for k in listdicb[i].keys():
            try:
                num1=float(listdicb[i][k]) 
            except ValueError:
                return [1, 'Something wrong with bam file '+bfile+' generated idxstats file: some value should be a numeric value but it is not']
            try:
                num2=float(listdicn[i][k]) 
            except ValueError:
                return [1, 'Something wrong with bam file '+nfile+' generated idxstats file: some value should be a numeric value but it is not']
            if (type(num1) is float) and (type(num2) is float):
                if num1==0:
                    if num2==0:
                        return [0,'']
                    else:
                        return [1,bfile+' baselinefile is 0 and newfile is not 0']
                else:
                    diff=abs(num1-num2)/num1
                    if diff >thresh:
                        return [1,bfile+'difference between the baselinefile and the newfile are more than threshhold']
    return [0, '']    
    
    
def CompMetricsCsv_3column(bfile, nfile, thresh):
    # to compare the baseline metrics.csv file with new run metrics.metrics file. If the content is strings, check if they are the same. If the content is the number, check if they are 95% similar.
    print "comparing file: "+bfile+" and "+nfile
    bf=open(bfile) # open the baseline file
    bdic={}
    for line in bf:
        linecon=line.split(',')
        if len(linecon)==3:# everyline of the csv file should have three element separate by ,
            bdic[linecon[0]+linecon[1]]=linecon[1]
        else:
            return [1,'error during parsing the csv file '+bfile+' more then three elements in a line (separate by the comma)']
    ndic={}
    nf=open(nfile) # open the new run file
    for line in nf:
        linecon=line.split(',')
        if len(linecon)==3: # everyline of the csv file should have three element separate by ,
            ndic[linecon[0]+linecon[1]]=linecon[2]
        else:
            return [1,'error during parsing the csv file '+bfile+' more then three elements in a line (separate by the comma)']
    if len(bdic) != len(ndic):
        return [1, 'baseline file '+bfile+' and new run file '+nfile+' has different number of lines']
    for k in bdic.keys():
        try:
            num1=float(bdic[k]) 
        except ValueError:
            num1=bdic[k]
        try:
            print k
            num2=float(ndic[k]) 
        except ValueError:
            num2=ndic[k]
        if (type(num1) is str) and (type(num2) is str) and num1==num2:
            return [0,'']
        elif (type(num1) is float) and (type(num2) is float):
            if num1==0:
                if num2==0:
                    return [0,'']
                else:
                    return [1,'baselinefile is 0 and newfile is not 0']
            else:
                diff=abs(num1-num2)/num1
                if diff >thresh:
                    return [1,'difference between the baselinefile and the newfile are more than threshhold']
    return [0, '']

if __name__ == "__main__":
    [errornum,errormsg]=CompMetricsCsv('Metrics1.csv','Metrics2.csv',0.05)
    print errornum,errormsg