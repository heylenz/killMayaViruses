"""
莫名其妙的普天同庆,这个是嫌TD不够忙嘛！
auth: yinhailin
email: hailin.yin@outlook.com
用法: python main.py 
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
    with open(filename) as f:
        for line in f:
            if re.search("PuTianTongQing", line) or re.search(
                "this script is machine generated", line
            ):
                return True


@logger.catch
def fixed_maya_file(filename):
    if not check_maya_file(filename):
        logger.info(f"{filename} 没有中毒.")
        return
    else:
        logger.info(f"{filename} 中毒了， 准备处理中。。。")

    backup = f"{filename}.backup"
    if os.path.exists(backup):
        logger.warning(f"{filename} 文件已经执行过, 如果需要重新执行,请删除backup文件,或者还原重新执行")
        return

    shutil.copy2(filename, backup)

    with open(backup) as fread:
        with open(filename, "w") as fwrite:
            for line in fread:
                if re.search('createNode script -n "MayaMelUIConfigurationFile', line):
                    while True:
                        temp = fread.readline()
                        if re.search("createNode", temp):
                            fwrite.write(temp)
                            break
                else:
                    fwrite.write(line)
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
