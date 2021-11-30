import time
from functools import partial
import numpy as np
import ray
from PIL import Image

IMGPATH = r'tst.jpg'


@ray.remote
def mandelbrot(width_px: int, height_px: int, location_re: np.float128, location_im: np.float128,
               zoom_level: np.float128, max_iterations: int, width_px_min: int, width_px_max: int) -> np.ndarray:
    std_dtype = np.float128  # datatype to be used for calculations
    mandelbrot_size_re = std_dtype(3.5) / zoom_level  # horizontal (real) extent of the image in the complex plane
    # vertical (imaginary) extent of the image in the complex plane
    mandelbrot_size_im = mandelbrot_size_re * std_dtype(height_px)/std_dtype(width_px)
    # Initialize result array. Only the first of the values in fill_value (the hue) will be changed later.
    # The other two (saturation and brightness) remain constant.
    color = np.full(shape=(width_px_max - width_px_min, height_px, 3), dtype=np.uint8, fill_value=[0, 255, 255])

    c_re_min = std_dtype(location_re - 0.5*mandelbrot_size_re)
    c_im_min = std_dtype(location_im - 0.5*mandelbrot_size_im)
    c_re_increment = std_dtype(mandelbrot_size_re/width_px)
    c_im_increment = std_dtype(mandelbrot_size_im/height_px)

    for screen_x in range(width_px_min, width_px_max):
        for screen_y in range(height_px):
            c_re = c_re_min + c_re_increment*screen_x
            c_im = c_im_min + c_im_increment*screen_y
            z_re = 0
            z_im = 0
            i = 0
            while (z_re * z_re + z_im * z_im <= 2) and (i < max_iterations):
                tmp = z_re * z_re - z_im * z_im + c_re
                z_im = 2 * z_re * z_im + c_im
                z_re = tmp
                i += 1
            # Use the smooth color algorithm for nice fluid color effects.
            # The result is a color angle in the HSL color system. For later processing with pillow, this angle is
            # expressed as a value from 0 to 255.
            if z_re*z_re + z_im*z_im > 1:
                color[screen_x - width_px_min, screen_y, 0] = np.uint8((i + 1 - np.log2(abs(np.log2(z_re*z_re + z_im*z_im,
                                                                                     dtype=std_dtype))) *
                                                                       255/max_iterations))
            else:
                color[screen_x - width_px_min, screen_y, 0] = np.uint8(i * 255 / max_iterations)
            if 10 >= (color[screen_x - width_px_min, screen_y, 0] % 245):
                color[screen_x - width_px_min, screen_y, 2] = color[screen_x - width_px_min, screen_y, 0] % 245
    return color


def start_px(width_px: int, no_workers: int, worker_index: int) -> int:
    (factor, remainder) = np.divmod(width_px, no_workers)
    return worker_index*factor + min(worker_index, remainder)


@ray.remote
def mandelbrot_parallel(width_px: int, height_px: int, location_re: np.float128, location_im: np.float128,
                        zoom_level: np.float128, max_iterations: int, no_slices: int) -> np.ndarray:
    mandelbrot_preconf = partial(mandelbrot.remote, width_px=width_px, height_px=height_px, location_re=location_re,
                                 location_im=location_im, zoom_level=zoom_level, max_iterations=max_iterations)
    slices_start = [start_px(width_px=width_px, no_workers=no_slices, worker_index=i) for i in range(no_slices + 1)]

    workload = [mandelbrot_preconf(width_px_min=slices_start[i], width_px_max=slices_start[i + 1])
                for i in range(no_slices)]
    results = ray.get(workload)
    return np.concatenate(results, axis=0)


if __name__ == '__main__':
    num_cpus = 8
    ray.init(num_cpus=num_cpus)
    location_re = -0.743643887037158704752191506114774
    location_im = 0.131825904205311970493132056385139
    start = time.time()
    img_asarray = ray.get(mandelbrot_parallel.remote(width_px=900, height_px=600, location_re=location_re,
                                                     location_im=location_im, zoom_level=100, max_iterations=400,
                                                     no_slices=450))
    print(f'execution with Ray: {time.time() - start:.1f} seconds.')
    ray.shutdown()
    img = Image.fromarray(obj=img_asarray.transpose(1, 0, 2), mode='HSV').convert(mode='RGB', colors=32768)
    img.save(IMGPATH)

