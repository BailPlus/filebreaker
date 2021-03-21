#!/usr/bin/python3
#Copyright Bail 2021
#com.Bail.filebreaker 文件碎片化 v1.0_1
#2021.2.6

CMDHELP = '''Usage:稍后更新'''

import base64,sys,os,tarfile,shutil

def iscmd():
    res = False
    if len(sys.argv) == 4:
        if sys.argv[1] in ('+','+d','+f','-','-d','-f'):
            res = True
    return res
def getcmd():
    do = sys.argv[1]
    fromfile = sys.argv[2]
    tofile = sys.argv[3]
    return do,fromfile,tofile
def ende(s):
    '''返回值:(模式:str,是否文件:bool)'''
    if s == '+' or s == '+f':
        return ('en',True)
    elif s == '+d':
        return ('en',False)
    elif s == '-' or s == '-f':
        return ('de',True)
    elif s == '-d':
        return ('de',False)
    else:
        raise NameError(s)
def encode(filename,bs):
    file = open(filename,'rb')
    code = base64.b16encode(file.read())    #待优化
##    with open('en.base64','wb') as file:    #调试，暂存结果
##        file.write(code)
    nowfc = nowbs = 0
    nowcode = ''
    lenth = len(code)
    for a in range(lenth):
        i = code[a]
        nowbs += 1
        nowcode += chr(i)
        if nowbs == bs or a+1 == lenth:
            nowfc += 1
            nowbs = 0
            res = ('%04d' % nowfc,nowcode)
            nowcode = ''
            yield res
def save(isfile,lst,name,isempty):
    try:
        os.mkdir(name)
    except:
        pass
    for i in lst:
        nowfile = ' '.join(i)
        nowpath = f'{name}/{nowfile}'
        with open(nowpath,'wb') as file:
            if not isempty:
                file.write('\000')
    if isfile:
        tar(name)
def tar(dir):
    tar = tarfile.open(dir+'.bfb','w')
    for root,dirs,files in os.walk(dir):
        for file in files:
            fullpath = os.path.join(root,file)
            tar.add(fullpath)
    tar.close()
    os.rename(dir+'.tar',dir+'.bfb')
    shutil.rmtree(dir)
def en(isfile,f,t,bs=32,isempty=True):
    lst = encode(f,bs)
    save(isfile,lst,t,isempty)
def decode(dir,filename):
    lst = iter(sorted(os.listdir(dir))) #sorted待优化
    codes = []
    for i in lst:
        codes.append(i.split()[1].encode())
    code = b''.join(codes)
##    with open('de.base64','wb') as file:    #调试
##        file.write(code)
    src = base64.b16decode(code)
##    print(src)    #调试
    with open(filename,'wb') as file:
        file.write(src)
def detar(file):
    tar = tarfile.open(filename+'.bfb')
    os.mkdir(file)
    tar.extractall(file)
    tar.close()
def de(isfile,f,t):
    if isfile:
        detar(f)
    decode(f,t)
def main():
    if not iscmd():
        print(CMDHELP)
        exit()
    cmdlst = getcmd()
    opt = ende(cmdlst[0])
    if opt[0] == 'en':
        en(opt[1],cmdlst[1],cmdlst[2])
    elif opt[0] == 'de':
        de(opt[1],cmdlst[1],cmdlst[2])
    else:
        raise RuntimeError(opt[0])
    return

if __name__ == '__main__':
    main()
