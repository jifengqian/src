'''
Created on May 20, 2013

@author: jqian
'''
import FileOverlap
import PathJF
import MetricsComp
import os
import VcfComp
from time import gmtime, strftime
import Configurations_param
class Summary:
    def __init__(self, bpath,npath):
        print "********************\n",strftime("%Y-%m-%d %H:%M:%S", gmtime()),"Start Summary Checking"
        self.bpath=bpath
        self.npath=npath
        self.name='Summary'
        self.testcaseid=[]
    def compare(self):
        [errornum,errormsg]=PathJF.folderchecking(self.bpath,self.npath) #Test if both two folders exist and the total number of folder is the same
        self.testcaseid.append(76303)
        if errornum >0:
            return [errornum,errormsg,76303]
        [errornum,errormsg]=PathJF.filechecking(self.bpath,self.npath) #1. Test if the total number of files is the same. 2. Test if the difference of the filesize beyone tolerance
        self.testcaseid.append(76620)
        self.testcaseid.append(76313)
        if errornum >0:
            return [errornum,errormsg,[76620,76313]]
        [errornum,errormsg]=PathJF.csvchecking(self.bpath,self.npath) #Test if the content in the index.html is the identical or in tolerance range.
        self.testcaseid.append(76691)
        if errornum >0:
            return [errornum,errormsg,76691]
        #[errornum,errormsg]=PathJF.imagechecking(self.bpath,self.npath) #Test if the difference of two set of images are in tolerance range.
        #self.testcaseid.append(77984)
        if errornum >0:
            return [errornum,errormsg,77984]
        return [0, '',list(set(self.testcaseid))]

class DiffExp:
    def __init__(self, bpath,npath):
        print "********************\n",strftime("%Y-%m-%d %H:%M:%S", gmtime()),"Start Differentail Expression Checking"
        self.bpath=bpath
        self.npath=npath
        self.name='DiffExp'
        self.testcaseid=[]
        self.bgenjsonpath=PathJF.getfullname_parent(os.path.join(self.bpath,'differential'),'Genes.json','cuffdiff') # find all the Genes.json file under the diffential folder
        self.btranjsonpath=PathJF.getfullname_parent(os.path.join(self.bpath,'differential'),'Transcripts.json','cuffdiff') # find all the Transcripts.json file under the diffential folder
        self.ngenjsonpath=PathJF.getfullname_parent(os.path.join(self.npath,'differential'),'Genes.json','cuffdiff')
        self.ntranjsonpath=PathJF.getfullname_parent(os.path.join(self.npath,'differential'),'Transcripts.json','cuffdiff')
        #print "bg,bt,ng,nt",self.bgenjsonpath, self.btranjsonpath, self.ngenjsonpath, self.ntranjsonpath
    def compare(self):
        #print "path", self.bgenjsonpath, self.ngenjsonpath
        print len(self.bgenjsonpath), ' Genes.json files needs to be compared'
        print len(self.btranjsonpath), ' Transcripts.json files needs to be compared'
        errornum=0
        errormsg=''
        if len(self.bgenjsonpath) != len(self.ngenjsonpath):
            print "number of Genes.json files are not equal!"
            errornum=1
            errormsg='Differential Expression Error: number of Genes.json files in baseline folder and newly generated folder are different!'
            self.testcaseid.append(84611)
            return [errornum, errormsg,testcaseid]
        elif len(self.btranjsonpath) != len(self.ntranjsonpath):
            print "number of Transcripts.json files are not equal!"
            errornum=1
            errormsg='Differential Expression Error: number of Transcripts.json files in baseline folder and newly generated folder are different!'
            return [errornum, errormsg, 84611]
        else:
            errornum1=0 # if soemthing wrng with gene.json
            errornum2=0 # if something wrong with transcripts.json
            errormsg1=''
            errormsg2=''
            for i in range(len(self.bgenjsonpath)):
                [errornum1, errormsg1]=FileOverlap.CompFiles(Configurations_param.diffexp_toler,self.bgenjsonpath[i],self.ngenjsonpath[i],[1,2],',')
                self.testcaseid.append(79636)
                errornum=errornum+errornum1
                errormsg=errormsg+errormsg1
            for i in range(len(self.btranjsonpath)):
                [errornum2, errormsg2]=FileOverlap.CompFiles(Configurations_param.diffexp_toler,self.btranjsonpath[i],self.ntranjsonpath[i],[1,2],',')
                self.testcaseid.append(79638)
                errornum=errornum+errornum2
                errormsg=errormsg+errormsg2                
            if errornum>0:
                return [1,'Differential Expression Error: '+errormsg1+errormsg2,list(set(self.testcaseid))]
            else:
                return [0, '',list(set(self.testcaseid))]

class Fusioncalling:
    def __init__(self, bpath,npath):
        print "********************\n",strftime("%Y-%m-%d %H:%M:%S", gmtime()),"Start Fusion calling Checking"
        self.bpath=bpath
        self.npath=npath
        self.name='Novel'
        self.testcaseid=[]
        self.brespath=PathJF.getfullname_parent(os.path.join(self.bpath,'samples'),'result.txt','tophat_fusion')
        self.bfuspath=PathJF.getfullname_parent(os.path.join(self.bpath,'samples'),'fusion.out','tophat_main')
        self.nrespath=PathJF.getfullname_parent(os.path.join(self.npath,'samples'),'result.txt','tophat_fusion')
        self.nfuspath=PathJF.getfullname_parent(os.path.join(self.npath,'samples'),'fusion.out','tophat_main')
    def compare(self):
        errornum=0
        errormsg=''
        [filenum,msg]=PathJF.check_pathlist(self.brespath,self.nrespath,'Novel','result.txt')
        if msg !='':
            return [0, msg,self.testcaseid]
        else:
            print str(filenum)+" result.txt file needs to be checked"
            for i in range(len(self.brespath)):
                [errornum1, errormsg1]=FileOverlap.CompFiles(Configurations_param.fusion_overlap_result_toler,self.brespath[i],self.nrespath[i],[0,1,2,3,4,5,6],' ') # result.txt checking
                self.testcaseid.append(76745)
                errornum=errornum+errornum1
                errormsg=errormsg+'\n'+errormsg1
        [filenum,msg]=PathJF.check_pathlist(self.bfuspath,self.nfuspath,'Novel','fusion.out')
        if filenum==0: # if there is no file in baseline
            print msg
            return [0, '',self.testcaseid] 
        elif filenum !=0 and msg !='': # if there is file in baseline but not equal number of file in baseline and run foler
            return [1,msg,self.testcaseid]
        else:
            for i in range(len(self.bfuspath)):
                print "checking the fusion.out file under tophat_main: "+ self.bfuspath[i]+self.nfuspath[i]
                [errornum2, errormsg2]=FileOverlap.CompFiles(Configurations_param.fusion_overlap_fusionout_toler,self.bfuspath[i],self.nfuspath[i],[0,1,2,3,4,5,6],' ') # fusion.out checking
                self.testcaseid.append(76746)
                errornum=errornum+errornum2
                errormsg=errormsg+'\n'+errormsg2
        if errornum>0:
            return [1,'Fusion calling error: '+errormsg1+'\n'+errormsg2,self.testcaseid]
        else:
            return [0, '',list(set(self.testcaseid))]

class Alignment:
    def __init__(self, bpath,npath):
        print "********************\n",strftime("%Y-%m-%d %H:%M:%S", gmtime()),"Start Alignment Checking"
        self.bpath=bpath
        self.npath=npath
        self.name='Alignment'
        self.testcaseid=[]
        self.bsamalignpath=PathJF.getfullname_parent(os.path.join(self.bpath,'samples'),'Metrics.csv','sampled_alignment')
        self.nsamalignpath=PathJF.getfullname_parent(os.path.join(self.npath,'samples'),'Metrics.csv','sampled_alignment')
        self.bfullaligpath=PathJF.getfullname_parent(os.path.join(self.bpath,'samples'),'Metrics.csv','full_alignment')
        self.nfullaligpath=PathJF.getfullname_parent(os.path.join(self.npath,'samples'),'Metrics.csv','full_alignment')
        self.bbampath=PathJF.getfullname(self.npath,'bam') # file all the bam files
        self.nbampath=PathJF.getfullname(self.bpath,'bam') 
    def compare(self):
        print len(self.bsamalignpath), 'sample_alignment metrics.csv files needs to be compared'
        print len(self.bfullaligpath), 'full_alignment metrics.csv files needs to be compared'
        print len(self.nbampath), 'bam files needs to be compared'
        errornum=0
        errormsg=''
        if len(self.bsamalignpath) != len(self.nsamalignpath):
            errornum=1
            errormsg='Alignment error: number of Metrics.csv files in the folder of {Root_folder}/samples/{sample}/replicates/{replicate}/metrics/sampled_alignment is different in baseline folder ['+str(len(self.bsamalignpath))+'] and new test folder ['+str(len(self.nsamalignpath))+']!'
            return [errornum, errormsg,self.testcaseid]
        elif len(self.bfullaligpath) != len(self.nfullaligpath):
            errornum=1
            errormsg='Alignment error: number of Metrics.csv files in the folder of {Root_folder}/samples/{sample}/replicates/{replicate}/metrics/full_alignment is different in baseline folder ['+str(len(self.bfullaligpath))+'] and new test folder ['+str(len(self.nfullaligpath))+']!'
            return [errornum, errormsg,self.testcaseid]
        elif len(self.bbampath) != len(self.nbampath):
            errornum=1
            errormsg='Alignment error: number of bam files in the baseline folder and new test folder  ['+str(len(self.bbampath))+'] and new test folder ['+str(len(self.nbampath))+']!'
            return [errornum, errormsg,self.testcaseid]
        else:
            errornum1=0
            errornum2=0
            errornum3=0
            errormsg1=''
            errormsg2=''
            errornum3=0
            for i in range(len(self.bsamalignpath)):
                [errornum1, errormsg1]=MetricsComp.CompMetricsCsv_2column(self.bsamalignpath[i],self.nsamalignpath[i],Configurations_param.align_metric_toler) # sampled_alignment folder metrics checking
                self.testcaseid.append(76728)
                errornum=errornum+errornum1
                errormsg=errormsg+errormsg1
            for i in range(len(self.bfullaligpath)):
                [errornum2, errormsg2]=MetricsComp.CompMetricsCsv_2column(self.bfullaligpath[i],self.nfullaligpath[i],Configurations_param.align_metric_toler) # full_alignment folder metrics checking
                self.testcaseid.append(76731)
                errornum=errornum+errornum2
                errormsg=errormsg+errormsg2
            for i in range(len(self.bbampath)):
                [errornum3, errormsg3]=MetricsComp.Compidx(self.bbampath[i],self.nbampath[i],Configurations_param.align_metric_toler) # full_alignment folder metrics checking
                self.testcaseid.append(81124)
                errornum=errornum+errornum3
                errormsg=errormsg+errormsg3
            if errornum>0:
                return [1,'Alignment error: '+errormsg,list(set(self.testcaseid))]
            else:
                return [0, '',list(set(self.testcaseid))]

class ReadFiltering:
    def __init__(self, bpath,npath):
        print "********************\n",strftime("%Y-%m-%d %H:%M:%S", gmtime()),"Start ReadFiltering"
        self.bpath=bpath
        self.npath=npath
        self.name='ReadFiltering'
        self.testcaseid=[]
        self.bfilterpath=PathJF.getfullname_parent(os.path.join(self.bpath,'samples'),'fastq.gz.info','filtered')
        self.nfilternpath=PathJF.getfullname_parent(os.path.join(self.bpath,'samples'),'fastq.gz.info','filtered')
    def compare(self):
        errornum=0
        errormsg=''
        print len(self.bfilterpath), 'fastaq.gz.info files needs to be compared!'
        if len(self.bfilterpath) != len(self.nfilternpath):
            errornum=1
            errormsg='ReadFiltering error: number of fastq.gz.info files in the folder of {Alignment_Folder}/samples/{Group}/replicates/{replicate}/filtered/ is different in baseline folder and new test folder!'
            return [errornum, errormsg,self.testcaseid]
        else:
            errornum1=0
            errormsg1=''
            for i in range(len(self.bfilterpath)):
                [errornum1, errormsg1]=MetricsComp.CompMetricsCsv_2column(self.bfilterpath[i],self.nfilternpath[i],0) # sampled_alignment folder metrics checking
                self.testcaseid.append(76747)
                errornum=errornum+errornum1
                errormsg=errormsg+errormsg1
            if errornum>0:
                return [1,'ReadFiltering error: '+errormsg,self.testcaseid]
            else:
                return [0, '',self.testcaseid]

class Variantcalling:
    def __init__(self,bpath,npath):
        print "********************\n",strftime("%Y-%m-%d %H:%M:%S", gmtime()),"Start Variant calling Checking"
        self.bpath=bpath
        self.npath=npath
        self.name='Variantcalling'
        self.testcaseid=[]
        self.bvcfpath=PathJF.getfullname_parent(os.path.join(self.bpath,'samples'),'genome.vcf.gz','variants')
        self.nvcfpath=PathJF.getfullname_parent(os.path.join(self.npath,'samples'),'genome.vcf.gz','variants')
    def compare(self):
        errornum=0
        errormsg=''
        print len(self.bvcfpath), 'genome.vcf.gz files needs to be compared!'
        if len(self.bvcfpath) != len(self.nvcfpath):
            errornum=1
            errormsg='variant calling error: number of genome.vcf.gz files in baseline folder and new test folder are different!'
            return [errornum, errormsg,self.testcaseid]
        else:
            for i in range(len(self.bvcfpath)):
                print "comparing the vcf files: "+self.bvcfpath[i]+self.nvcfpath[i]
                [bstat,nstat]=VcfComp.getstat(self.bvcfpath[i], self.nvcfpath[i])
                if (not (bstat is  None)) and (not (nstat is  None)): # if both baseline and new test run is validated vcf file
                    obj=VcfComp.vcf_stats_tool()
                    [errornum1,errormsg1]=obj.cmp_main(bstat,nstat,Configurations_param.vcf_stat_toler)
                    self.testcaseid.append(76741)
                else:
                    errornum1=1
                    errormsg1=self.bvcfpath[i]+" or "+self.nvcfpath[i]+' is not validated vcf file'
                errornum=errornum+errornum1
                errormsg=errormsg+errormsg1
            return [errornum,errormsg,list(set(self.testcaseid))]

class Novel:
    def __init__(self, bpath,npath):
        print "********************\n",strftime("%Y-%m-%d %H:%M:%S", gmtime()),"Start Novel Transcript Checking"
        self.bpath=bpath
        self.npath=npath
        self.testcaseid=[]
        self.name='Novel assemblies'
        self.bisopath=PathJF.getfullname_parent(os.path.join(self.bpath,'samples'),'isoforms.fpkm_tracking','novel')
        self.bgenepath=PathJF.getfullname_parent(os.path.join(self.bpath,'samples'),'genes.fpkm_tracking','novel')
        self.bgtfpath=PathJF.getfullname_parent(os.path.join(self.bpath,'samples'),'merged.gtf','cuffmerge')
        self.nisopath=PathJF.getfullname_parent(os.path.join(self.npath,'samples'),'isoforms.fpkm_tracking','novel')
        self.ngenepath=PathJF.getfullname_parent(os.path.join(self.npath,'samples'),'genes.fpkm_tracking','novel')
        self.ngtfpath=PathJF.getfullname_parent(os.path.join(self.npath,'samples'),'merged.gtf','cuffmerge')
    def compare(self):
        print len(self.bisopath), 'isoforms.fpkm_tracking files needs to be compared'
        print len(self.bgenepath), 'genes.fpkm_tracking files needs to be compared'
        print len(self.bgtfpath), 'merged.gtf files needs to be compared'
        errornum=0
        errormsg=''
        if len(self.bisopath) != len(self.nisopath):
            errornum=1
            errormsg='Novel transcription error: number of isoforms.fpkm_tracking files in baseline folder and newly generated folder are different!'
            return [errornum, errormsg]
        elif len(self.bgenepath) != len(self.ngenepath):
            errornum=1
            errormsg='Novel transcription error: number of genes.fpkm_tracking files in baseline folder and newly generated folder are different!'
            return [errornum, errormsg]
        elif len(self.bgtfpath) != len(self.bgtfpath):
            errornum=1
            errormsg='Novel transcription error: number of merged.gtf files in baseline folder and newly generated folder are different!'
            return [errornum, errormsg]
        else:
            errornum1=0
            errornum2=0
            errornum3=0
            errormsg1=''
            errormsg2=''
            errormsg3=''
            for i in range(len(self.bisopath)):
                [errornum1, errormsg1]=FileOverlap.CompFiles(5,self.bisopath[i],self.nisopath[i],[6],' ')
                self.testcaseid.append(79647)
                errornum=errornum+errornum1
                errormsg=errormsg+errormsg1
            for i in range(len(self.bgenepath)):
                [errornum2, errormsg2]=FileOverlap.CompFiles(5,self.bgenepath[i],self.ngenepath[i],[1],' ')
                self.testcaseid.append(79650)
                errornum=errornum+errornum2
                errormsg=errormsg+errormsg2
            for i in range(len(self.bgtfpath)):
                [errornum3, errormsg3]=FileOverlap.CompFiles(5,self.bgtfpath[i],self.ngtfpath[i],[0,3,4],' ')
                self.testcaseid.append(79651)
                errornum=errornum+errornum3
                errormsg=errormsg+errormsg3
            if errornum>0:
                return [1,'Novel transcription error: '+errormsg1+'\n'+errormsg2+'\n'+errormsg3]
            else:
                return [0, '',list(set(self.testcaseid))]


if __name__ == "__main__":
    #bpath='C:\\Users\\jqian\\Documents\\My Box Files\\RNA-SEQ\\Data\\2013-04-26_093340'
    #npath='C:\\Users\\jqian\\Documents\\My Box Files\\RNA-SEQ\\Data\\2013-04-26_093340'
    #s=Summary(bpath, npath)
    #[errornum, errormsg,testid]=s.compare()
    #stest=Alignment(bpath,npath)
    #[errornum, errormsg,testcaseid]=stest.compare()
    #stest=ReadFiltering(bpath,npath)
    #[errornum, errormsg,testcaseid]=stest.compare()
    #print errornum
    #print errormsg
    #print testcaseid
    npath='/illumina/scratch/Ste/Data_Analysis/Baselines/RNAseq/130320_M00836_0049_Aa2uf7-16plex/Isis_2.4.19/2013-06-18_102955'
    bpath='/illumina/scratch/Ste/Data_Analysis/Baselines/RNAseq/130320_M00836_0049_Aa2uf7-16plex/Isis_2.4.19/2013-06-14_131553'
    [errornum, errormsg,testcaseid]=Alignment(bpath,npath).compare()
    print "The number of error is", errornum, ", errormsg is ", errormsg, ", these testcases are tested:", testcaseid

