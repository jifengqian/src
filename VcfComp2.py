#compare only two files/text out of vcf-stats
from __future__ import division
import sys,os,re
import subprocess
import sys

#adding path for lib/ -- bad including
#real full name
#scriptDir=os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
#real full path
#scriptName=os.path.basename(__file__)


#libexecDir=os.path.join(scriptDir,'..','..' ,'libexec')
#sys.path.append(libexecDir)
#@author: Jingtao Liu
#@author: Jifeng Qian changed in 5/28/2013

import demjson


class vcf_stats_tool:
    def perl2json(self,perl_string):
        return perl_string.replace('$VAR1 = ','').replace('=>',':').replace(';','')
    def json2python(self, json_string):
        return demjson.decode(str(json_string))
    def changed_in_range(self,num1, num2,THRESH): #to check if the num1 and num2 are varied in a considerable range
        if (not (type(num1) in [int, float])) or (not (type(num2) in [int, float])):
            return False
        num1=int(num1)    
        num2=int(num2)
        if (abs(num1)+abs(num2) ) ==0 : return True
        bias=abs(num1-num2)/abs(num1) 
        if bias>THRESH: 
            return False
        else:
            return True
    def valchange(self, d1, d2, parent=''):
        changes=[]
        for k in d1.keys():
            if type(d1[k])==type({}) and d2.has_key(k):
                changes.extend(self.valchange(d1[k], d2[k], str(parent+"."+k)))
            else:
                if d2.has_key(k):       
                    if d1[k]<>d2[k]: # if the value is different
                        changes.append( ( str(parent+"."+k), d1[k], d2[k]) )
                else:
                    changes.append( (  str(parent+"."+k), d1[k], None   ))
        return changes    
    def cmp_main(self, p1, p2, thresh):
        errornum=0 # this is a indicator to show if p1 an p2 are different in a tolerate range
        errormsg=''
        j1=self.perl2json(p1)
        j2=self.perl2json(p2)
        d1=self.json2python(j1)
        d2=self.json2python(j2)
        if (type(d1)==unicode):
            d1=demjson.decode(d1)    
        if (type(d2)==unicode):
            d2=demjson.decode(d2)   
        for k, n1, n2 in self.valchange(d1,d2):
            if not (self.changed_in_range(n1,n2,thresh)):
                errormsg=errormsg+'\n'+k+' difference is beyond tolerance in baseline and new test run!'
                errornum=errornum+1
        return [errornum,errormsg]

def getstat(bfile,nfile):
    os.system("export PERL5LIB=/home/jqian/tools/vcftools_0.1.10/perl")
    bp = subprocess.Popen(["perl","/home/jqian/tools/vcftools_0.1.10/perl/vcf-validator", bfile], stdout=subprocess.PIPE)
    bv=bp.stdout.readlines()    
    np = subprocess.Popen(["perl","/home/jqian/tools/vcftools_0.1.10/perl/vcf-validator", nfile], stdout=subprocess.PIPE)
    nv=np.stdout.readlines()
    bp = subprocess.Popen(["perl","/home/jqian/tools/vcftools_0.1.10/perl/vcf-stats", bfile], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    boutput3, berr3 = bp.communicate()
    np = subprocess.Popen(["perl","/home/jqian/tools/vcftools_0.1.10/perl/vcf-stats", nfile], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    noutput4, nerr4 = np.communicate()
    #print bv,nv,type(berr3),boutput3, berr3, type(nerr4), noutput4, nerr4
    if ((len(bv)==0) and (len(nv)==0)) and ((berr3=='') and (nerr4=='')): # if the vcf file is valid and no error msg show up during the statistics generation
        return [boutput3,noutput4]


if __name__=="__main__":
    o=vcf_stats_tool()
    #print demjson.decode(u'[1,2,3]')
    p1="""
    $VAR1 = {
          'samples' => {
                 'CancerID_COLO-829C_S1' => {
                                  'missing' => 43968
                                },
                 'NormalID_COLO829BL_S1' => {
                                  'missing' => 43968
                                }
                   },
          'all' => {
                 'shared' => {
                       '0' => 43968
                     },
                 'snp_count' => 43968,
                 'count' => 43968,
                 'nalt_0' => 43968,
                 'snp' => {
                    'A>C' => 1108,
                    'A>G' => 1881,
                    'T>G' => 1216,
                    'T>A' => 1127,
                    'T>C' => 2025,
                    'C>A' => 2573,
                    'A>T' => 1178,
                    'G>T' => 2762,
                    'C>G' => 777,
                    'G>C' => 832,
                    'G>A' => 14506
                      }
               }
        };
    """
    p2="""
    $VAR1 = {
          'samples' => {
                 'NormalID_NORMAL' => {
                            'missing' => 15437
                              },
                 'CancerID_TUMOR' => {
                               'missing' => 15437
                             }
                   },
          'all' => {
                 'shared' => {
                       '0' => 15437
                     },
                 'snp_count' => 15437,
                 'count' => 15437,
                 'nalt_0' => 15437,
                 'snp' => {
                    'A>C' => 655,
                    'A>G' => 1653,
                    'T>G' => 703,
                    'T>A' => 911,
                    'C>T' => 2171,
                    'T>C' => 1704,
                    'C>A' => 1339,
                    'G>T' => 1404,
                    'A>T' => 826,
                    'C>G' => 1006,
                    'G>C' => 937,
                    'G>A' => 2144
                      }
               }
        };
    """
    print o.cmp_main(sys.argv[1],sys.argv[2],0.05)
    #r=getstat('/home/jqian/RNA-SEQ/2013-05-17_100111_nonovel/samples/uhr2/replicates/uhr2/variants/uhr2.genome.vcf.gz', '/home/jqian/RNA-SEQ/2013-05-17_100111_nonovel/samples/uhr2/replicates/uhr2/variants/uhr2.genome.vcf.gz')
    #print r, type(r)