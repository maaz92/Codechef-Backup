#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

Keywords: python, tools, codechef ,algorithms, solution, download,

Copyright (C) 2003-2004 Free Software Foundation, Inc.


Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.
    * Neither the name of the Secret Labs AB nor the names of its contributors
      may be used to endorse or promote products derived from this software
      without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''
#Dependencies:
#mechanize
#beautifulsoup

import os
import sys
import getpass
import optparse

try:
    from BeautifulSoup import BeautifulSoup, SoupStrainer
except ImportError:
    print "beautifulSoup required but missing"
    sys.exit(1)
try:
    from mechanize import Browser
except ImportError:
    print "mechanize required but missing"
    sys.exit(1)
    
    
if __name__=="__main__":
    proxy = raw_input("Enter the Proxy for your connection or type '-1' (without quotes) if your connection does not require a proxy\n")
    
    #handle no proxy
    if proxy == "-1":
        proxy = ""

    #for determining file extensions fromm language
    FILE_EXTENSION = { "ADA" : ".ads", "ASM" : ".asm", "BASH" : ".sh", "BF" : ".bf", "C" : ".c", "C99 strict" : ".c","C++ 4.3.2" : ".cpp", "C++ 4.9.2" : ".cpp" ,"C++14" : ".cpp", "C++ 4.0.0-8" : ".cpp",
    "JAVA" : ".java" , "SCALA" : ".scala", "TEXT" : ".txt", "RUBY" : ".rb", "PYTH 3.1.2": ".py", "PYTH": ".py", "PHP": ".php", "PERL" : ".pl", "PERL6" : ".pl", 
    "NODEJS" : ".js", "HASK" : ".hs", "C#" : ".cs" }
    
    # create a browser object
    br = Browser()

    # add proxy support to browser
    if len(proxy) != 0: 
        protocol,proxy = options.proxy.split("://")
        br.set_proxies({protocol:proxy})
    
    # let browser fool robots.txt
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; \
              rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.set_handle_robots(False)

    print "Enter your Codechef username :",
    username = raw_input()
    password = getpass.getpass()

    # authenticate the user
    print "Authenticating " + username
    br.open ("http://codechef.com")
    br.select_form (nr=0)
    br["name"] = username
    br["pass"] = password
    br.form.action = "http://www.codechef.com"
    response = br.submit()
    
    # grab the signed submissions list
    print "Grabbing siglist for " + username
    br.open("http://www.codechef.com/users/" + username)
    solved_list=[]
    questions=[]
    for link in br.links():
        if 'status' in link.url.split('/'):
            solved_list.append('http://www.codechef.com'+link.url+'?sort_by=All&sorting_order=asc&language=All&status=15&Submit=GO')
            questions.append(link.url.split(',')[0].split('/')[-1])
    for solved,question_id in zip(solved_list,questions):
        accepted_list=br.open(solved)
        soup = BeautifulSoup(accepted_list)
        
        solution_ids = soup.findAll("td", { "width" : "60" })
        solution_langs = soup.findAll("td", { "width" : "70" })
        print 'Downloading solution for question_id: '+ question_id
        for solution_id,lang in zip(solution_ids,solution_langs):
            sol=str(solution_id)
            sol = sol[15:-5]
            language = str(lang)
            language = language[32:-5]
            solution = br.open('http://www.codechef.com/viewplaintext/'+sol)
            soup = BeautifulSoup(solution)
            solution = soup.findAll("pre")[0]
            solution = str(solution)
            solution = solution[5:-6]
            solution = BeautifulSoup(solution, convertEntities=BeautifulSoup.XML_ENTITIES).contents[0]
            solution = solution.strip()

            dir = username+'_codechef_accepted_solutions/'
            try:
                os.stat(dir)
            except:
                os.mkdir(dir) 
            ext=""
            if language in FILE_EXTENSION.keys():
                ext+= FILE_EXTENSION[language]
            else:
                ext='.cpp'  
            f = open(dir+question_id+'-'+sol+ext,"w") 
            f.write(solution)
            f.close()
    
    print 'imported all files'