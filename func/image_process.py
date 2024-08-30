import cv2

# 等比缩放后剩余部分留空
def imageResize(input_image,target_height, target_width):
    h= input_image.shape[0]
    w = input_image.shape[1]
    scale_h, scale_w = float(h/target_height), float(w/target_width)
    scale = max(scale_h,scale_w)
    new_w, new_h = int(w/scale), int(h/scale)
    resize_img = cv2.resize(input_image, (new_w,new_h))
    # 图像上下左右扩充像素
    top = int((target_height-new_h)/2)
    bottom = target_height-new_h-top
    left = int((target_width-new_w)/2)
    right = target_width - new_w - left
    target_img = cv2.copyMakeBorder(resize_img, top,bottom, left,right,cv2.BORDER_CONSTANT,\
                                   value=[0,0] )
    return target_img