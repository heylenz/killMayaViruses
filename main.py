"""
Tools to kill maya script virus
auth: yinhailin
email: hailin.yin@outlook.com
Usage:  python main.py folder path
"""
import os
import re
# import psutil
import shutil

import fire
from loguru import logger
from rich.progress import track


"""
/resources/l10n/
/plug-ins/animImportExport.pres.mel
"""


def fixed_anim_import_export_mel(autodesk_root):
    pass


def check_maya_file(filename):
    find_script_block = []
    with open(filename,encoding='utf-8', errors='ignore') as f:
        line = f.readline()
        while True:
            if not line:
                break 
            else:
                if re.search('createNode script', line):
                    lines = []
                    lines.append(line)
                    while True:                        
                        temp = f.readline()                  
                        if not re.search(r'\t',temp) and not re.search('createNode script', temp):
                            break      
                        else:
                            lines.append(temp)
     

                    find_script_block.append(lines)


            line = f.readline()
    shit_script_block = []
    for x in find_script_block:
        if not [k for k in x if re.search('playbackOptions',k)]:
            shit_script_block.extend(x)

    # for i in shit_script_block:
    #     print(i)
    return shit_script_block


@logger.catch
def fixed_maya_file(filename):
    results = check_maya_file(filename)
    if not results:
        logger.info(f"{filename} 没有中毒.")
        return
    else:
        logger.info(f"{filename} 中毒了， 准备处理中。。。")

    backup = f"{filename}.backup"
    if os.path.exists(backup):
        logger.warning(f"{filename} 文件已经执行过, 如果需要重新执行,请删除backup文件,或者还原重新执行")
        return

    shutil.copy2(filename, backup)

    with open(backup, encoding='utf-8', errors='ignore') as fread:
        with open(filename, "w", encoding='utf-8', errors='ignore') as fwrite:

            line = fread.readline()
            while True:
                if not line:
                    break
                if line not in results:
                    fwrite.write(line)
                line = fread.readline()


    logger.info(f"{filename} 已经删除中毒代码，请检查文件")


def main(root, autodesk_root=r"C:\Program Files\Autodesk"):
    """
    default autodesk_root C:\\Program Files\\Autodesk
    python main.py --root=d: --autodesk_root=c:\Program Files\Autodesk
    """
    if autodesk_root[-8:] != 'Autodesk':
        raise RuntimeError('autodesk_root 参数不正确，参考 C:\Program Files\Autodesk')
    fixed_anim_import_export_mel(autodesk_root)

    all_maya_files = []

    for _root, _dirs, files in os.walk(root):
        for f in files:
            if f.endswith(".ma"):
                maya_file = os.path.join(_root, f)
                all_maya_files.append(maya_file)

    for maya_file in track(all_maya_files):
        fixed_maya_file(maya_file)


if __name__ == "__main__":
    fire.Fire(main)
