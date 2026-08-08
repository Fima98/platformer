from os import listdir
from os.path import join

import pygame


def import_image(*path, format='png', alpha=True):
    full_path = join(*path) + f'.{format}'
    return (
        pygame.image.load(full_path).convert_alpha()
        if alpha
        else pygame.image.load(full_path).convert()
    )


def import_folder(*path):
    folder_path = join(*path)
    frames = []

    for file_name in sorted(listdir(join(*path))):
        full_path = join(folder_path, file_name)
        frames.append(pygame.image.load(full_path).convert_alpha())

    return frames
