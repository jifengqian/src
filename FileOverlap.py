'''
Created on May 20, 2013

@author: jqian
'''
from __future__ import division # this is for real divison, but integar division. 
import os
def File2set(filename,wantlist,sep): 
# extract the valuable column out of the original file
# filename is the input filename
# wantlist is the index of the valuable columns
# sep is separator of the columns
    f=open(filename)
    tmp=f.readline()# this first line is for naming purpose, not needed
    keyset=set()
    for line in f:
        linew=''
        if sep ==' ': # if the seperator is a space, treat several space together as one space separator
            linecon=line.split()
        else:
            linecon=line.split(sep)
        for wanti in wantlist:
            if wanti >=len(linecon):
                return keyset
            else:
                linew=linew+linecon[wanti]
        keyset.add(linew)
    f.close()
    print filename, ' has ', len(keyset), ' results in it' 
    return keyset
    


def FilesDiff(bfile, nfile,wantlist,sep):
    bset=File2set(bfile, wantlist,sep)
    nset=File2set(nfile, wantlist,sep)
    num_overlap=len(bset&nset)
    num_b=len(bset)
    if num_b==0 and num_overlap ==0:
        print 'no valuable content for both baseline and new file'
        return 0 # when both baseline and new files are empty
    elif num_b ==0:
        return 300 # when the baseline is empty but something in the new files
    else:
        diff=abs(num_b-num_overlap)/num_b
    return diff

def CompGson(bfile,nfile): # compare the Genes.json file
    CompFiles(5,bfile,nfile,[1,2],',')

def CompFiles(tolerance,bfile,nfile,wantlist,sep): 
    # working on file comparision, 'bfile' is the baseline file,
    #'nfile' is the newly generated file, 'wantlist' is list of numbers, which indicate the clolumn number of the target file are extracted
    # to generate the sets '''
    print "comparing file: "+bfile+" and "+nfile
    errornum=0
    errormsg=''
    if os.path.isfile(bfile) and os.path.isfile(nfile):
        diff=FilesDiff(bfile, nfile,wantlist,sep)
        perct=diff*100
        print "difference perct is:",perct
        if perct >100:
            errornum=0
            errormsg=bfile+' is empty while'+nfile+' is not empty!'
        elif perct>float(tolerance*100):
            errornum=1
            errormsg=bfile+' '+nfile+' difference is '+str(perct)+'%, not tolerate!'
    else:
        errornum=1
        errormsg=bfile+' or '+nfile+' can not be found!'
    return [errornum, errormsg]

if __name__ == "__main__":
    #[errornum,errormsg]=CompFiles(5, 'merged.genes.fpkm_tracking','merged.genes2.fpkm_tracking',[1],' ')
    File2set('Genes.json',[1,2],',')
