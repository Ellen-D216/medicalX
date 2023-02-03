import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from typing import Sequence


class Painter:
    def __init__(self, image:np.ndarray, spacing: Sequence[float] = [1., 1., 1.]) -> None:
        self.set_image(image, spacing)

    def set_image(self, image:np.ndarray, spacing: Sequence[float] = [1., 1., 1.]):
        if image.shape[-1] not in (3, 4):
            self.image = image[..., np.newaxis]
        else:
            self.image = image
        self.spacing = np.asarray(spacing)
        if len(self.spacing) == 3:
            self.aspect = np.asarray(spacing[1]/spacing[0], spacing[2]/spacing[0], spacing[2]/spacing[1])
        else:
            self.aspect = spacing[1]/spacing[0]
        
    def imshow(self, cmap=None, title=None, vmin=None, vmax=None, **fig_args):
        plt.figure(**fig_args)
        plt.imshow(self.image, cmap=cmap, vmin=vmin, vmax=vmax)
        if cmap is not None: plt.colorbar()
        if title is not None: plt.title(title)
        plt.axis('off')
        plt.show()

    def slice_plot(
        self,
        slice_index: Sequence[int] = None,
        cmap = None,
        save_path: str = None,
        **fig_args
    ):
        '''
            image: D H W [C]
        '''
        if slice_index is None:
            slice_index = np.asarray(self.image.shape[:3]) // 2
        k, j, i = slice_index

        fig, axes = plt.subplots(1, 3, **fig_args)
        axi_axis, cor_axis, sag_axis = axes
        axi_axis.imshow(self.image[k, ...], aspect=self.aspect[0], cmap=cmap)
        axi_axis.axis('off')
        axi_axis.set_title("Axial")
        cor_axis.imshow(self.image[:, j, ...], aspect=self.aspect[1], cmap=cmap)
        cor_axis.axis('off')
        cor_axis.set_title("Coronal")
        sag_axis.imshow(self.image[:, :, i, ...], aspect=self.aspect[2], cmap=cmap)
        sag_axis.axis('off')
        sag_axis.set_title("Sagittal")
        if save_path is not None:
            fig.savefig(save_path)
        plt.show()


    def dynamic_plot(
        self,
        show_axis: int,
        cmap = None,
        **fig_kwargs
    ):
        '''
            image: D H W [C]
        '''
        from IPython.display import clear_output
        plt.figure(**fig_kwargs)
        plt.axis('off')
        image = self.image.swapaxes(0, show_axis)
        for i in range(image.shape[0]):
            plt.imshow(
                self.image[i, ...], cmap=cmap, vmin=image.min(), vmax=image.max(),
                aspect=self.aspect[show_axis]
            )
            clear_output(True)
            plt.show()


    def grid_plot(
        self,
        n_cols: int,
        show_axis: int,
        padding: int = 2,
        padding_value: int = -1024,
        cmap = None,
        save_path: str = None,
        **fig_args
    ):
        '''
            image: D H W [C]
        '''
        n_maps = self.image.shape[show_axis]
        n_rows = int(np.ceil(n_maps / n_cols))
        image = self.image.swapaxes(0, show_axis)
        channels = image.shape[-1]
        
        height, width = int(image.shape[1] + padding), int(image.shape[2] + padding)

        grid = np.full((height*n_rows+padding, width*n_cols+padding, channels), padding_value)
        k = 0
        for y in range(n_rows):
            for x in range(n_cols):
                if k >= n_maps:
                    break
                grid[y*height:(y+1)*height-padding, x*width:(x+1)*width-padding, :] = image[k]
                k += 1

        plt.figure(**fig_args)
        plt.imshow(grid, cmap=cmap, vmin=image.min(), vmax=image.max())
        plt.axis('off')
        if save_path is not None:
            plt.savefig(save_path)
        plt.show()


    def to_gif(
        self,
        show_axis: int,
        duration: float,
        save_path: str = None,
        loop: int = 0,
        optimize: bool = True
    ):
        '''
            image D H W [C]
        '''
        single_channel = self.image.shape[-1] == 1
        image = self.image.swapaxes(0, show_axis)
        if single_channel:
            image = np.squeeze(image, axis=-1)
        image -= image.min(); image /= image.max(); image *= 255
        image = image.astype(np.uint8)
        mode = "P" if single_channel else "RGB"
        duration_ms = duration / image.shape[0] * 1000
        images = [Image.fromarray(i, mode=mode) for i in image]
        images[0].save(
            save_path, save_all=True, append_images=images[1:], optimize=optimize,
            duration=duration_ms, loop=loop
        )


def get_colormap(cmap:str, category:int=None):
    return plt.cm.get_cmap(cmap, category)