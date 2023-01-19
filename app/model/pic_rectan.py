""" add rectangle to image """
import cv2


def rectan(image, pic_location):
    for i in range(len(pic_location)):
        # Start coordinate, here (5, 5)
        # represents the top left corner of rectangle
        start_point = (int(pic_location[i][0]), int(pic_location[i][1]))

        # Ending coordinate, here (220, 220)
        # represents the bottom right corner of rectangle
        end_point = (int(pic_location[i][2]), int(pic_location[i][3]))

        # Blue color in BGR
        color = (0, 255, 0)

        # Line thickness of 2 px
        thickness = 15

        # Using cv2.rectangle() method
        # Draw a rectangle with blue line borders of thickness of 2 px
        image = cv2.rectangle(image, start_point, end_point, color, thickness)
    return image


if __name__ == '__main__':
    pic_location = [[5, 5, 500, 200], [5, 400, 700, 300]]
    path = "model/image.jpeg"
    # Reading an image in default mode
    image = cv2.imread(path)
    # Window name in which image is displayed
    window_name = 'Image'
