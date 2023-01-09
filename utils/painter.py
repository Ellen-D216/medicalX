import matplotlib.pyplot as plt
import PIL.Image as PIL
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
        self.spacing = spacing
        
    def plot(self, **fig_args):
        plt.figure(**fig_args)
        plt.imshow(self.image)
        plt.axis('off')
        plt.show()

    def slice_plot(
        self,
        slice_index: Sequence[int] = None,
        is_label: bool = False,
        save_path: str = None,
        **fig_args
    ):
        '''
            image: D H W [C]
        '''
        if slice_index is None:
            slice_index = np.asarray(self.image.shape[:3]) // 2
        k, j, i = slice_index
        sl, sp, ss = self.spacing
        cmap = 'cubehelix' if is_label else 'gray'

        fig, axes = plt.subplots(1, 3, **fig_args)
        axi_axis, cor_axis, sag_axis = axes
        axi_axis.imshow(self.image[k, ...], aspect=sp/sl, cmap=cmap)
        axi_axis.axis('off')
        axi_axis.set_title("Axial")
        cor_axis.imshow(self.image[:, j, ...], aspect=ss/sl, cmap=cmap)
        cor_axis.axis('off')
        cor_axis.set_title("Coronal")
        sag_axis.imshow(self.image[:, :, i, ...], aspect=ss/sp, cmap=cmap)
        sag_axis.axis('off')
        sag_axis.set_title("Sagittal")
        if save_path is not None:
            fig.savefig(save_path)
        plt.show()


    def dynamic_plot(
        self,
        show_axis: int,
        is_label: bool = False,
    ):
        '''
            image: D H W [C]
        '''
        from IPython.display import clear_output
        cmap = 'cubehelix' if is_label else 'gray'
        plt.figure(dpi=100)
        for i in range(self.image.shape[show_axis]):
            if show_axis == 0:
                plt.imshow(
                    self.image[i, ...], cmap=cmap, vmin=self.image.min(), vmax=self.image.max(),
                    aspect=self.spacing[2]/self.spacing[1]
                )
            elif show_axis == 1:
                plt.imshow(
                    self.image[:, i, ...], cmap=cmap, vmin=self.image.min(), vmax=self.image.max(),
                    aspect=self.spacing[2]/self.spacing[0]
                )
            elif show_axis == 2:
                plt.imshow(
                    self.image[:, :, i, ...], cmap=cmap, vmin=self.image.min(), vmax=self.image.max(),
                    aspect=self.spacing[1]/self.spacing[0]
                )
            plt.axis('off')
            clear_output(True)
            plt.show()


    def grid_plot(
        self,
        n_cols: int,
        show_axis: int,
        padding: int = 2,
        padding_value: int = -1024,
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

        cmap = 'gray' if channels == 1 else None
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
        image = ((image - image.min()) / image.max() * 255).astype(np.uint8)
        mode = "P" if single_channel else "RGB"
        duration_ms = duration / image.shape[0] * 1000
        images = [PIL.fromarray(i).convert(mode) for i in image]
        images[0].save(
            save_path, save_all=True, append_images=images[1:], optimize=optimize,
            duration=duration_ms, loop=loop
        )