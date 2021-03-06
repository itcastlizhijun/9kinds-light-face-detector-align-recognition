import torch
import cv2
import time
import numpy as np
from yoloface_detect_align_module import yoloface
from ultraface_detect_module import ultraface
from ssdface_detect_module import ssdface
from retinaface_detect_align_module import retinaface
from mtcnn_pfld_landmark import mtcnn_detect as mtcnnface
from facebox_detect_module import facebox_pytorch as facebox
from facebox_detect_module import facebox_dnn
from dbface_detect_align_module import dbface_detect as dbface
from centerface_detect_align_module import centerface
from lffd_detect_module import lffdface
import matplotlib.pyplot as plt
import inspect
import argparse

def retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Object Detection using YOLO in OPENCV')
    parser.add_argument('--imgpath', type=str, default='s_l.jpg', help='Path to image file.')
    args = parser.parse_args()
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    align = False

    yoloface_detect = yoloface(device=device, align=align)
    ultraface_detect = ultraface()
    ssdface_detect = ssdface()
    retinaface_detect = retinaface(device=device, align=align)
    mtcnn_detect = mtcnnface(device=device, align=align)
    facebox_detect = facebox(device=device)
    facebox_dnn_detect = facebox_dnn()
    dbface_detect = dbface(device=device, align=align)
    centerface_detect = centerface(align=align)
    lffdface_detect = lffdface(version=1)

    srcimg = cv2.imread(args.imgpath)
    
    a = time.time()
    yolo_result, _ = yoloface_detect.detect(srcimg)
    b = time.time()
    yolo_time = round(b - a,3)
    cv2.putText(yolo_result, 'yoloface waste time:'+str(yolo_time), (20,40), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255))

    a = time.time()
    ultraface_result, _ = ultraface_detect.detect(srcimg)
    b = time.time()
    ultraface_time = round(b - a,3)
    cv2.putText(ultraface_result, 'ultraface waste time:' + str(ultraface_time), (20, 40), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255))

    a = time.time()
    ssdface_result, _ = ssdface_detect.detect(srcimg)
    b = time.time()
    ssdface_time = round(b - a, 3)
    cv2.putText(ssdface_result, 'ssdface waste time:' + str(ssdface_time), (20, 40), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255))

    a = time.time()
    retinaface_result, _ = retinaface_detect.detect(srcimg)
    b = time.time()
    retinaface_time = round(b - a, 3)
    cv2.putText(retinaface_result, 'retinaface waste time:' + str(retinaface_time), (20, 40), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255))

    a = time.time()
    mtcnn_result, _ = mtcnn_detect.detect(srcimg)
    b = time.time()
    mtcnn_time = round(b - a, 3)
    cv2.putText(mtcnn_result, 'mtcnn waste time:' + str(mtcnn_time), (20, 40), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255))

    a = time.time()
    facebox_result, _ = facebox_detect.detect(srcimg)
    b = time.time()
    facebox_time = round(b - a, 3)
    cv2.putText(facebox_result, 'facebox waste time:' + str(facebox_time), (20, 40), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255))

    a = time.time()
    facebox_dnn_result, _ = facebox_dnn_detect.detect(srcimg)
    b = time.time()
    facebox_dnn_time = round(b - a, 3)
    cv2.putText(facebox_dnn_result, 'facebox_dnn waste time:' + str(facebox_dnn_time), (20, 40), cv2.FONT_HERSHEY_DUPLEX, 1,(0, 0, 255))

    a = time.time()
    dbface_result, _ = dbface_detect.detect(srcimg)
    b = time.time()
    dbface_time = round(b - a, 3)
    cv2.putText(dbface_result, 'dbface waste time:' + str(dbface_time), (20, 40), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255))

    a = time.time()
    centerface_result, _ = centerface_detect.detect(srcimg)
    b = time.time()
    centerface_time = round(b - a, 3)
    cv2.putText(centerface_result, 'centerface waste time:' + str(centerface_time), (20, 40), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255))

    a = time.time()
    lffdface_result, _ = lffdface_detect.detect(srcimg)
    b = time.time()
    lffdface_time = round(b - a, 3)
    cv2.putText(lffdface_result, 'lffdface waste time:' + str(lffdface_time), (20, 40), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255))

    results = (yolo_result, ultraface_result, ssdface_result, retinaface_result, mtcnn_result, facebox_result, facebox_dnn_result, dbface_result, centerface_result, lffdface_result)
    waste_times = (yolo_time, ultraface_time, ssdface_time, retinaface_time, mtcnn_time, facebox_time, facebox_dnn_time, dbface_time, centerface_time, lffdface_time)

    line1 = np.hstack(results[:5])
    line2 = np.hstack(results[5:])
    combined = np.vstack([line1, line2])
    cv2.namedWindow('detect-compare', cv2.WINDOW_NORMAL)
    cv2.imshow('detect-compare', combined)
    # cv2.imwrite('out.jpg', combined)

    for i,res in enumerate(results):
        winname = retrieve_name(res)[0]
        cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
        cv2.imshow(winname, res)

    labels = []
    for data in waste_times:
        labels.append(retrieve_name(data)[0].replace('_time', ''))

    plt.rcParams['font.family'] = 'SimHei'
    x = list(range(len(waste_times)))
    plt.bar(x, waste_times, width=0.5, color='red', label='耗时比较', tick_label=labels)
    # for a, b in zip(x, waste_times):
    #     plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=10)  # 添加数据标签
    plt.xlabel("模型")
    plt.ylabel("时间")

    # plt.barh(labels, left=0, height=0.5, width=waste_times, label='耗时比较', color='red')
    # plt.ylabel("模型")
    # plt.xlabel("时间")

    plt.legend()
    plt.show()

    cv2.waitKey(0)
    cv2.destroyAllWindows()