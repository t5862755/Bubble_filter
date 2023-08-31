import csv

import cv2
import numpy as np

def draw_and_fill_polygon(image_input_path, image_output_path):
    global points, mask_points, drawing

    drawing = False  # 是否正在繪畫
    points = []  # 儲存滑鼠移動的坐標
    mask_points = []  # 儲存全部的點

    # 滑鼠事件的回調函數
    def draw(event, x, y, flags, param):
        global points, drawing

        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            points = [(x, y)]

        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing:
                points.append((x, y))
                for i in range(1, len(points)):
                    cv2.line(img, points[i - 1], points[i], (0, 255, 0), 2)

        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            if len(points) >= 2:
                cv2.fillPoly(img, [np.array(points)], color=(0, 255, 255))
            mask_points.append(points)
            points = []

    img = cv2.imread(image_input_path)
    mask = np.zeros_like(img)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw)

    while True:
        cv2.imshow('image', img)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:  # 按下ESC鍵退出
            break

    cv2.destroyAllWindows()

    # 在遮罩上繪製填充的區域
    for i in range(len(mask_points)):
        cv2.fillPoly(mask, [np.array(mask_points[i])], color=(255, 255, 255))

    # 將填充的區域變成黑色，其他區域變成白色
    output_image = cv2.bitwise_not(mask)

    cv2.imshow('output_image', output_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite(image_output_path, output_image)

    return output_image
def calculate_black_area_size_with_path(image_output_path):
    output_image = cv2.imread(image_output_path)
    black_pixel_count = np.sum(np.all(output_image == [0, 0, 0], axis=-1))  # Count pixels with RGB value [0, 0, 0] (black)

    # # Assuming pixel size of 1 unit, calculate the area in square units
    # resolution = 1  # You may need to adjust this based on your image resolution
    # black_area_size = black_pixel_count * resolution * resolution

    return black_pixel_count

def calculate_black_area_size(image):
    output_image = image
    black_pixel_count = np.sum(np.all(output_image == [0, 0, 0], axis=-1))  # Count pixels with RGB value [0, 0, 0] (black)

    # # Assuming pixel size of 1 unit, calculate the area in square units
    # resolution = 1  # You may need to adjust this based on your image resolution
    # black_area_size = black_pixel_count * resolution * resolution

    return black_pixel_count

if __name__ == "__main__":

    case = '1'
    image_input_path = 'C:/Users/YaoHung/Desktop/Wu/MIRDC/Bubble_Detect/Pictures/Before_processed/original_' + f"{case}.png"
    image_output_path = 'C:/Users/YaoHung/Desktop/Wu/MIRDC/Bubble_Detect/Pictures/After_processed/mask_real_' + f"{case}.png"
    output_man_made_image = draw_and_fill_polygon(image_input_path, image_output_path)

    image_model_input = 'C:/Users/YaoHung/Desktop/Wu/MIRDC/Bubble_Detect/zhe_output/mask_' + f"{case}.png"
    exclusive_or_image = cv2.imread(image_model_input)
    exclusive_or_image = cv2.bitwise_not(exclusive_or_image)

    or_result = cv2.bitwise_or(output_man_made_image, exclusive_or_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    rate_of_detect = calculate_black_area_size(or_result) / calculate_black_area_size(output_man_made_image)

    # print(calculate_black_area_size(output_man_made_image))
    # print(calculate_black_area_size(or_result))
    # print(rate_of_detect)




