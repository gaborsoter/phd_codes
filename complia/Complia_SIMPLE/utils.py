import numpy as np

def crop(frame, x_min, x_max, y_min, y_max):
    """
        relative crop
    """
    width, height, _ = frame.shape
    
    width_min = int(width*x_min)
    width_max = int(width*x_max)

    height_min = int(height*y_min)
    height_max = int(height*y_max)

    return frame[height_min:height_max, width_min:width_max, :]


def triangle_angles(p1, p2, p3):
    """
        angles of the triangle given the points
    """

    perms = [
        [p1, p2, p3],
        [p3, p1, p2],
        [p2, p3, p1]
    ]

    angles = []
    for perm in perms:
        line1 = perm[1] - perm[0]
        line2 = perm[2] - perm[0]

        angle = np.arccos(line1.dot(line2)/(np.linalg.norm(line1)*np.linalg.norm(line2)))
        angles.append(angle)

    return angles

def triangle_area(p1, p2, p3):
    """
        Area of triangle given three points
        Thanks: https://en.wikipedia.org/wiki/Shoelace_formula
    """
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    return 0.5*np.abs(x1*y2 + x2*y3 + x3*y1 - x2*y1 - x3*y2 - x1*y3)

def triangle_lengths(p1, p2, p3):
    """
        Lengths of all the edges of a triangle 
    """
    edges = [
        p1 - p2,
        p2 - p3,
        p3 - p1
    ]

    return np.linalg.norm(edges, axis=1)

def triangle_centroid(p1, p2, p3):
    """
        Centroid
    """

    return np.mean([p1, p2, p3], axis=0)


if __name__ == '__main__':
    p1 = [0,0]
    p2 = [1,0]
    p3 = [0,1]

    print(triangle_centroid(p1,p2,p3))

