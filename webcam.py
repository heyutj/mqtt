import pygame
import pygame.camera

pygame.camera.init()
print(pygame.camera.list_cameras())
cam = pygame.camera.Camera('/dev/video0',(640,480))
cam.start()
img = cam.get_image()
print(pygame.image.tostring(img,"RGB"))
