'''
Created on DEC 29, 2017

@author: NNA
'''

import cast.analysers.jee
import cast.application
import uuid
import tempfile
import cast.analysers.log as LOG
import os , sys
from cast.analysers import Member,Bookmark
from setuptools.sandbox import _file
import xml.etree.ElementTree as ET
from Cython.Compiler.Options import annotate


def get_overriden(_type, member):
    """
    Get the ancestor's member this member overrides
    """
    member_name = member.get_name()
    
    result = []
    setfilter = False
    
    for parent in _type.get_inherited_types():
        
        for child in parent.get_children():
            if child.get_name() == member_name:
                result.append(child)
        
        result += get_overriden(parent, member)
        
    return result

class search(cast.analysers.jee.Extension):
    def __init__(self):
        self.result = None
        temp_file = None
        tempfilename = None
        self.count = 0
        self.jmstext=""
        self.jmsmetamodeltext =""
        
               
    def start_analysis(self,options):
        LOG.debug('Successfully JEE DTD Logger analyzer Started')
        #options.handle_xml_with_xpath('/beans')
        options.handle_xml_with_xpath('/')
        self.temp_file = "C:\ProgramData\CAST\CAST\Extensions\com.castsoftware.labs.jeeXMLDTDinternallogger.1.3.0\summarydtd"+str(uuid.uuid4())+".txt"
        
  
   
    
    
    def start_xml_file(self, file):
        LOG.debug('Scanning XML  file :' )
        setfilter = False
        #filepath = os.path.realpath('XmlFilter.txt')
        #filepath= cwd.replace("8.2", "Extensions\com.castsoftware.labs.jeeXMLDTDinternallogger.1.1.0\XmlFilter.txt")
        filepath = "C:\ProgramData\CAST\CAST\Extensions\com.castsoftware.labs.jeeXMLDTDinternallogger.1.3.0\XmlFilter.txt"
        if (os.path.isfile(filepath)):
            #LOG.info("path--->"+ str(filepath))
            with open(filepath,'r' ) as fp:  
               filterlist=[]
               filterlist =  fp.readlines()
            if file.get_name().endswith('.xml'):
                if (os.path.isfile(file.get_path())):
                    tree = ET.parse(file.get_path(), ET.XMLParser(encoding="UTF-8"))
                    root=tree.getroot()
                    result = os.path.basename(file.get_name())
                    resultclean = ''.join([i for i in result if not i.isdigit()])
                    resultclean = resultclean.replace('-', '')
                    for x in filterlist:
                        if x.lower().strip() == resultclean.lower().strip():
                            setfilter = True
                            break
                    if setfilter == False:
                        if len(root.attrib) > 0:
                            sumattrvalue =file.get_name() + str(root.attrib)
                            with open(self.temp_file, 'a+') as fd:
                                fd.write(sumattrvalue + '\n')
                                fd.close()
                         #LOG.warning(file.get_name() +str(root.attrib))
                           
                
                
   
    def end_analysis(self):
        LOG.info("search JEEXMLDTDinternal logger Summary start")
        if (os.path.isfile(self.temp_file)):
            with open(self.temp_file, 'r') as fd:
                for line in fd.readlines():
                    line = line.replace('\n', ' $ ')
                    LOG.warning(line)
                fd.close()
            if (os.path.isfile(self.temp_file)):
                os.remove(self.temp_file)
        self.result
        LOG.info("search JEEXMLDTDinternal logger summary ended")
        
        

   
