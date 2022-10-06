import subprocess
import shutil
import sys
import re

def pull_extract_framework_res():
    subprocess.call("adb pull /system/framework/framework-res.apk",shell=True)
    subprocess.run(["aapt dump resources framework-res.apk | grep resource |grep android:bool/ |tee framework-resource.txt"],shell=True)

    with open("framework-resource.txt","r") as f:
        counter = 0
        fileout = open("framework-systemui-res.html", "w")
        table = "<table border=2>\n"
        table += " <tr>\n"
        table += "  <th>No</th>"
        table += "  <th>Framework Resource</th>"
        table += "  <th>value</th>"
        table += " </tr>\n"
        
        lines = f.readlines()
        for line in lines:  
            c = line.split()
            if 'spec ' in line:
                table += " <tr>\n"
                counter = counter + 1
                table += "  <td>"+ str(counter) +"</td>"
                
                cmd = "adb shell cmd overlay lookup android "+c[3][:-1]
                
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                out, err = p.communicate()
                   
                table += "  <td>"+c[3][:-1]+"</td>"
                table += "  <td>"+out.decode()+"</td>"
                table += " </tr>\n"
            else:
                table += " <tr>\n"
                counter = counter + 1
                table += "  <td>"+str(counter) +"</td>"
                cmd = "adb shell cmd overlay lookup android "+c[2][:-1]
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                out, err = p.communicate()
                table += "  <td>"+c[2][:-1]+"</td>"
                table += "  <td>"+out.decode()+"</td>"
                table += " </tr>\n"
                
        fileout.writelines(table)
        fileout.close()

def pull_extract_systemui_res():
    subprocess.call("adb pull /system_ext/priv-app/SystemUI/SystemUI.apk",shell=True)
    subprocess.run(["aapt dump resources SystemUI.apk | grep com.android.systemui:bool |tee systemui-resource.txt"],shell=True)

    with open("systemui-resource.txt","r") as f:
        counter = 0
        fileout = open("framework-systemui-res.html", 'a')
        table = '\n'
        table = "<table border=2>\n"
        table += " <tr>\n"
        table += "  <th>No</th>"
        table += "  <th>SystemUI</th>"
        table += "  <th>value</th>"
        table += " </tr>\n"
        lines = f.readlines()
        for line in lines:  
            c = line.split()
            if 'spec ' in line:
                table += " <tr>\n"
                counter = counter + 1
                table += "  <td>"+ str(counter) +"</td>"
                
                cmd = "adb shell cmd overlay lookup com.android.systemui "+c[3][:-1]
                
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                out, err = p.communicate()
                   
                table += "  <td>"+c[3][:-1]+"</td>"
                table += "  <td>"+out.decode()+"</td>"
                table += " </tr>\n"
            else:
                table += " <tr>\n"
                counter = counter + 1
                table += "  <td>"+str(counter) +"</td>"
                cmd = "adb shell cmd overlay lookup com.android.systemui "+c[2][:-1]
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                out, err = p.communicate()
                table += "  <td>"+c[2][:-1]+"</td>"
                table += "  <td>"+out.decode()+"</td>"
                table += " </tr>\n"
                
        fileout.writelines(table)
        fileout.close()

def capture_bugreport():
    subprocess.call("rm -rf bugreport* sysprop*",shell=True)
    subprocess.call("adb bugreport ./bugreport.zip",shell=True)
    shutil.unpack_archive("bugreport.zip", ".")
    subprocess.call("mv bugreport-* bugreport.txt",shell=True)
    p = subprocess.Popen("cat bugreport.txt | grep -n 'SYSTEM PROPERTIES'", shell=True, stdout=subprocess.PIPE)
    sys.stdout.flush()
    lintes = p.stdout.readline()
    start_line = lintes.decode().split(':')[0]
    lintes = p.stdout.readline()
    end_line = lintes.decode().split(':')[0]    
    print(start_line)
    print(end_line)
    
    cmd= f"sed '1,{start_line}d;{end_line},$d' bugreport.txt > sysprop.txt"
    p = subprocess.call(cmd, shell=True,stdout=subprocess.PIPE)
    
    with open("sysprop.txt", "r+") as f:
        counter = 0
        fileout = open("sysprop.html", 'a')
        table = '\n'
        table = "<table border=2>\n"
        table += " <tr>\n"
        table += "  <th>No</th>"
        table += "  <th>System Property</th>"
        table += "  <th>value</th>"
        table += " </tr>\n"
        
        lines = f.readlines()
        myiter = iter(lines)
        
        while True:
            try:
                line = myiter.__next__()
                if line[:-1].endswith(']'):
                    print(line)
                    table += " <tr>\n"
                    counter = counter + 1
                    table += "  <td>"+ str(counter) +"</td>"
                    table += "  <td>"+line.split(':')[0]+"</td>"
                    table += "  <td>"+line.split(':')[1]+"</td>"
                    table += " </tr>\n"
                else:      
                    s1 = line
                    s2 = s1.strip()+ "," + myiter.__next__()
                    print(s2)
                    table += " <tr>\n"
                    counter = counter + 1
                    table += "  <td>"+ str(counter) +"</td>"
                    table += "  <td>"+s2.split(':')[0]+"</td>"
                    table += "  <td>"+s2.split(':')[1]+"</td>"
                    table += " </tr>\n"
            except StopIteration:
                break    

        fileout.writelines(table)
        fileout.close()
        	 
def main():
    print("++++++++++++++++START++++++++++++++++++++++")
    pull_extract_framework_res()
    pull_extract_systemui_res()
    capture_bugreport()
    print("++++++++++++++++FINISH+++++++++++++++++++++")
    

if __name__ == "__main__":
    main()
