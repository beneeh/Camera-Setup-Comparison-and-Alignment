import json

if __name__ == "__main__":
    cameras = []
    n = int(input("Number of cameras: "))
    for i in range(n):
        print("Camera %i" % (i + 1))
        camera = {'x': input("x: "),
                  'y': input("y: "),
                  'alignment_angle': input("alignment_angle: ")}
        cameras.append(camera)
    d = {'cameras': cameras,
         'max_distance': input('max distance:'),
         'angle_of_view': input('angle of view: '),
         'field_len_x': input('field len x: '),
         'field_len_y': input('field len y:'),
         'field_origin_x': input('field origin x: '),
         'field_origin_y': input('field origin y: ')}

    dest = input('save as: ')
    with open(dest, 'w+') as f:
        f.write(json.dumps(d, indent=4))
