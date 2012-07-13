#!/usr/bin/python
#coding=utf-8


import re
import sys
import os

def help():
    print """
##################################################
#
#       此脚本用于扫描 .c 文件，列出其中的所有函数
#       并以头文件函数声明的方式输出
#       注意：所扫描的函数，定义时 函数名，返回值及所有参数
#            必须在同一行内，否则扫描结果会出错
#
##################################################
          """

def main():
    if not(os.path.exists('/usr/bin/ctags')):
        print 'ctags is not installed in /usr/bin/ctags !'
        print 'we need ctags to analysis C files , please install it first !'
        quit()
    #获取命令行参数
    argv = sys.argv
    argc = len(argv)
    #print argv
    #print argc

    InputFileName = ''
    OutputFileName = ''

    #检查参数个数
    if argc < 2:
        print "not enough parameters !"
        print "usage: python -u " + argv[0] + " InputFileName [OutputFileName]"
        quit()

    #获取输入文件名
    InputFileName  = argv[1]

    #获取输出文件名
    if argc >= 3:
        OutputFileName = argv[2]

    #print "input  file name :" + InputFileName
    #print "output file name :" + OutputFileName

    tmp = os.popen('ctags -u -f - ' + InputFileName).read()

    # 正则表达式
    regex_func_str = r'(?<=/\^).*(?=\$/;\"\tf)'    # 提取 ctags 找到的函数的条目
    regex_decomment_str = r'.*?(?=\\.*)'    # 用于去除注释

    # 编译正则表达式
    function_lexer  = re.compile(regex_func_str)
    decomment_regex = re.compile(regex_decomment_str)

    # 提取属于函数的条目
    match_list = function_lexer.findall(tmp)

    function_list = []
    if len(match_list) != 0:

        for i in match_list:
            #print i
            if 'static' in i : #以static修饰的不公开函数，不提取到输出文件
                continue
            if r'\/' in i :    #去除注释
                function_text = decomment_regex.match(i).group()
                function_text = function_text.strip()
            else:
                function_text = i
            # 组合输出字符串
            #function_text = 'extern ' + function_text + ';\n'
            function_text = 'extern ' + function_text + ';'
            function_list.append(function_text)
            #print function_text

        # 如果给出了输出文件名称，则输出到文件
        if OutputFileName != '':
            OutputFile = open(OutputFileName,'w')
            for i in function_list:
                OutputFile.write(function_text + '\n')
            OutputFile.close()
        else:
            for i in function_list:
                print i


help()
main()
