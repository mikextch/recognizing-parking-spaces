import cv2
import numpy as np
import pickle
import logging
import sys
import os
from roipoly import MultiRoi
from matplotlib import pyplot as plt


select_image = "frame1.png"

if __name__ == '__main__':
    im = cv2.imread(select_image)

rois = []
font = cv2.FONT_HERSHEY_SIMPLEX

logging.basicConfig(format='%(levelname)s ''%(processName)-10s : %(asctime)s '
                           '%(module)s.%(funcName)s:%(lineno)s %(message)s',
                    level=logging.INFO)

n_arg = len(sys.argv)
# Comprobar que no sea un nuevo
if n_arg==1 and os.path.exists("vidCrs1.mk"):
    #Comprobar si hay puntos anteriores
    with open ('vidCrs1.mk', 'rb') as fp:
        rois = pickle.load(fp)

    print("rois guardados: "+str(rois))
elif n_arg > 1:
    if str(sys.argv[1]) == "--new":
        pass
    else:
        print("Parametros no reconocidos")
        exit()
# Create image
# img = np.ones((100, 100)) * range(0, 100)

# Show the image
fig = plt.figure()
plt.imshow(im, interpolation='nearest', cmap="Greys")
plt.title("Click en el boton new para un nuevo espacio")

# Draw multiple ROIs
multiroi_named = MultiRoi(roi_names=['Primer espacio', 'Segundo espacio'])
# Draw all ROIs
# plt.imshow(im, interpolation='nearest', cmap="Greys")
roi_names = []
for name, roii in multiroi_named.rois.items():
    # roii.display_roi()
    # roi.display_mean(im)
    x = roii.x
    y = roii.y

    rois.append([int(x[0]), int(y[0]),
    int(x[1]),int(y[1]),
    int(x[2]),int(y[2]),
    int(x[3]),int(y[3])])

# plt.legend(roi_names, bbox_to_anchor=(1.2, 1.05))

i = 0
while True:
    for roi in rois:
        # print(len(roi))
        pts = np.array([
        [roi[0], roi[1]],
        [roi[2], roi[3]],
        [roi[4], roi[5]],
        [roi[6], roi[7]]
        ], np.int32)
        cv2.polylines(im, [pts], True, (0, 0, 255), 2)
        i += 1

    cv2.imshow("mk",im)
    key = cv2.waitKey(0) & 0xFF
    if key == ord("q"):
        break

print("rois a guardar: "+str(rois))
with open('vidCrs1.mk', 'wb') as fp:
    pickle.dump(rois, fp)

# with open ('vidCrs1.mk', 'rb') as fp:
#     itemlist = pickle.load(fp)
#
# itemlist = itemlist[:-1]
# print(itemlist)

cv2.waitKey(0)
cv2.destroyAllWindows()
