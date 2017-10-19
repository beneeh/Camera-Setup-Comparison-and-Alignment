from app.components.camera import Camera
from PIL import Image, ImageDraw


class Rectangle(object):
    def __init__(self, x_dim, y_dim):
        self.x_dim = x_dim
        self.y_dim = y_dim


class Room(Rectangle):
    """
    this class represents the whole room, including the space the cameras can be placed in
    """
    def __init__(self, x_dim, y_dim, field_x_dim, field_y_dim, scale=10):
        super(Room, self).__init__(x_dim * scale, y_dim * scale)
        self.cameras = []
        self.scale = scale
        field_origin_x = ((x_dim - field_x_dim)/2) * self.scale
        field_origin_y = ((y_dim - field_y_dim)/2) * self.scale
        self.field = Field(field_x_dim * scale, field_y_dim * scale, field_origin_x, field_origin_y)

    def add_camera(self, angle_of_view, max_distance, x, y, direction):
        self.cameras.append(Camera(angle_of_view, max_distance*self.scale, x*self.scale, y*self.scale, direction))

    def draw(self):
        im = Image.new('RGB', (self.x_dim, self.y_dim), 'white')
        drawer = ImageDraw.Draw(im)
        self.draw_field(drawer)
        for camera in self.cameras:
            self.draw_camera(drawer, camera)
        im.show()

    def draw_field(self, drawer):
        drawer.line([(self.field.origin_x, self.field.origin_y),
                     (self.field.origin_x + self.field.x_dim, self.field.origin_y),
                     (self.field.origin_x + self.field.x_dim, self.field.origin_y + self.field.y_dim),
                     (self.field.origin_x, self.field.origin_y + self.field.y_dim),
                     (self.field.origin_x, self.field.origin_y)], fill='black')

    def draw_camera(self, drawer, camera):
        """
        :type camera: Camera
        """
        drawer.line([(camera.x, camera.y), camera.point_a(), camera.point_b(),
                     (camera.x, camera.y)], fill='red')


class Field(Rectangle):
    """
    this class represents the space to observe (no cameras can be placed here)
    """
    def __init__(self, x_dim, y_dim, origin_x, origin_y):
        super(Field, self).__init__(x_dim, y_dim)
        self.origin_x = origin_x
        self.origin_y = origin_y