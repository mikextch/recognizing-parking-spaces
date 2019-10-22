import numpy as np
import cv2
import pickle

cap = cv2.VideoCapture('testmk.mp4')

vacant = []
with open ('vidCrs1.mk', 'rb') as fp:
    coordinates = pickle.load(fp)

coordinates = coordinates
coordinatesToShow = coordinates


def drop_irregular_image(image_, roi_corners):
    # original image
    rowAshow = coordinates
    i = 0
    # -1 loads as-is so if it will be 3 or 4 channel as the original
    # image = cv2.imread('frame1.png', -1)
    # image_ = cv2.Canny(image, 100, 200)
    # mask defaulting to black for 3-channel and transparent for 4-channel
    # (of course replace corners with yours)
    mask = np.zeros(image_.shape, dtype=np.uint8)
    # roi_corners = np.array([[
    #     (rowAshow[i][0], rowAshow[i][1]),
    #     (rowAshow[i][2], rowAshow[i][3]),
    #     (rowAshow[i][4], rowAshow[i][5]),
    #     (rowAshow[i][6], rowAshow[i][7])]], dtype=np.int32)
    # fill the ROI so it doesn't get wiped out when the mask is applied
    channel_count = frame.shape[2]  # i.e. 3 or 4 depending on your image
    ignore_mask_color = (255,)*channel_count
    # print("chanel coint, "+str(channel_count))
    cv2.fillPoly(mask, roi_corners, ignore_mask_color)


    # apply the mask
    masked_image = cv2.bitwise_and(image_, mask)
    x,y,w,h = cv2.boundingRect(roi_corners)

    imgcroped = masked_image[y:y+h, x:x+w].copy()
    # save the result
    # cv2.imshow('image_masked.png', imgcroped)

    return imgcroped
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # exit()

def crop_image_white_back():
    # load the image
    rowAshow = coordinates
    i = 0
    # -1 loads as-is so if it will be 3 or 4 channel as the original
    image = cv2.imread('frame1.png')


    mask = np.ones(image.shape, dtype=np.uint8)
    mask.fill(255)

    roi_corners = np.array([[
        (rowAshow[i][0], rowAshow[i][1]),
        (rowAshow[i][2], rowAshow[i][3]),
        (rowAshow[i][4], rowAshow[i][5]),
        (rowAshow[i][6], rowAshow[i][7])]], dtype=np.int32)

    # fill the ROI into the mask
    cv2.fillPoly(mask, roi_corners, 0)

    # The mask image
    # cv2.imwrite('image_masked.png', mask)

    # applying th mask to original image
    masked_image = cv2.bitwise_or(image, mask)
    # save the result
    cv2.imshow('image_masked.png', masked_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    exit()


while(cap.isOpened()):
    ret, frame = cap.read()

    #out.write(frame)

    img_canny = cv2.Canny(frame, 100, 200)

    img_gray = cv2.cvtColor(img_canny, cv2.COLOR_BAYER_BG2GRAY)

    (thresh, img) = cv2.threshold(img_canny, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    spots = []
    rowAshow = coordinatesToShow

    i = 0
    for item in coordinates:
        row = "A"
        pts = np.array([[
            (rowAshow[i][0], rowAshow[i][1]),
            (rowAshow[i][2], rowAshow[i][3]),
            (rowAshow[i][4], rowAshow[i][5]),
            (rowAshow[i][6], rowAshow[i][7])]], dtype=np.int32)
        # print(img[(item[0]+item[1]) : (item[2]+item[3]), (item[4]+item[5]) : (item[6]+item[7]) ])
        imgCrop = drop_irregular_image(img, pts)
        non = cv2.countNonZero(imgCrop)
        if non < 200:
            cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
        else:
            cv2.polylines(frame, [pts], True, (0, 0, 255), 2)

        i += 1

    cv2.imshow('frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
